#!/usr/bin/env perl
use Mojolicious::Lite;
use JSON::PP;
use Time::Piece;
use DBD::mysql;
use Redis::Fast;
use Data::Dumper;
use Carp qw/carp confess/;

my $debug = 0;
my $session_name     = "session_id";

# php
my $lobby_host1 = $ENV{LOGIN_ADDR1} || "127.0.0.1";
my $lobby_port1 = $ENV{LOGIN_PORT1} || '8080';

# perl
my $lobby_host2 = $ENV{LOGIN_ADDR2} || "127.0.0.1";
my $lobby_port2 = $ENV{LOGIN_PORT2} || '8081';

# go
my $lobby_host3 = $ENV{LOGIN_ADDR3} || "127.0.0.1";
my $lobby_port3 = $ENV{LOGIN_PORT3} || '8082';


app->config(
  hypnotoad => {
    listen => ['http://*:3000'],
    workers => 20,
  },
);

get '/' => sub {
  my $c = shift;
  #warn $c->dumper($c);
  # get cookie
  my $sid = get_sid($c);
  #warn $sid;
  #warn get_cookie_value($c, "session_id");
  $c->stash('sid' => $sid);
  $c->render(template => 'index');
};

# phpapi

get '/new_user' => sub {
  # for debug
  my $c = shift;
  my $user  = $c->param('user');
  my $pass  = $c->param('pass');
  my $nname = $c->param('nick_name');
  my $cmd = 'curl -s -X POST -H "Content-Type: application/json" -d \'{"user_name":"%s", "password":"%s", "nick_name":"%s"}\' http://%s:%d/new_user.php';
  $cmd = sprintf($cmd, $user, $pass, $nname, $lobby_host1, $lobby_port1);
  my $res = `$cmd`;
  $c->render(json => decode_json($res));
};

get '/login' => sub {
  # for debug
  my $c = shift;
  my $user = $c->param('user');
  my $pass = $c->param('pass');
  my $cmd = 'curl -s -X POST -H "Content-Type: application/json" -d \'{"user_name":"%s", "password":"%s"}\' http://%s:%d/login.php';
  $cmd = sprintf($cmd, $user, $pass, $lobby_host1, $lobby_port1);
  my $res = `$cmd`;
  $c->render(json => decode_json($res));
};

get '/user_id' => sub {
  # for debug
  my $c = shift;
  my $sid = get_sid($c);
  my $cmd = 'curl -s -X POST -H "Content-Type: application/json" -H "Cookie: session_id=%s" http://%s:%d/get_user_id.php';
  $cmd = sprintf($cmd, $sid, $lobby_host1, $lobby_port1);
  my $res = `$cmd`;
  $c->render(json => decode_json($res));
};

post '/upload' => sub {
  # for debug
  my $c = shift;
  my $sid = get_sid($c);
  my $file_name = $c->param('file_name');
  my $file_data = $c->param('file_data');
  my $cmd = 'curl -s -X POST -H "Content-Type: application/json" -H "Cookie: session_id=%s" -d \'{"file_name":"%s","file_data":"%s"}\' http://%s:%d/upload.php';
  $cmd = sprintf($cmd, $sid, $file_name, $file_data, $lobby_host1, $lobby_port1);
  my $res = `$cmd`;
  $c->render(json => decode_json($res));
};

get '/delete_user' => sub {
  # for debug
  my $c = shift;
  my $sid = get_sid($c);
  my $cmd = 'curl -s -X POST -H "Content-Type: application/json" -H "Cookie: session_id=%s" http://%s:%d/delete.php';
  $cmd = sprintf($cmd, $sid, $lobby_host1, $lobby_port1);
  my $res = `$cmd`;
  $c->render(json => decode_json($res));
};

# perlapi

get '/courseget' => sub {
  # for debug
  my $c = shift;
  my $sid = get_sid($c);
  #my $cmd = 'curl -v -H "Content-Type: application/json" -b \'session_id=%s\' http://%s:%d/course';
  my $cmd = 'curl -s -H "Content-Type: application/json" -b \'session_id=%s\' http://%s:%d/course.php';
  $cmd = sprintf($cmd, $sid, $lobby_host2, $lobby_port2);
  warn $cmd;
  my $res = `$cmd`;
  $c->render(json => decode_json($res));
};

get '/coursepost' => sub {
  # for debug
  my $c = shift;
  my $sid = get_sid($c);
  my $course_id = $c->param('course_id');
  #my $cmd = 'curl -v -H "Content-Type: application/json" -b \'session_id=%s\' -d \'{"id":%s}\' http://%s:%d/course';
  my $cmd = 'curl -s -X POST -H "Content-Type: application/json" -b \'session_id=%s\' -d \'{"id":%s}\' http://%s:%d/course.php';
  $cmd = sprintf($cmd, $sid, $course_id, $lobby_host2, $lobby_port2);
  #$cmd = sprintf($cmd, $sid, $course_id, $lobby_host2);
  my $res = `$cmd`;
  #$c->render(json => decode_json($res));
  $c->render(text => $res);
};

post '/battle' => sub {
  # for debug
  my $c = shift;
  my $sid = get_sid($c);
  my $req_json = $c->req->json;
  my $data = json_canonical_encode($req_json); 
  #my $cmd = 'curl -v -X POST -H "Content-Type: application/json" -b \'session_id=%s\' -d \'%s\' http://%s:%d/battle';
  my $cmd = 'curl -s -X POST -H "Content-Type: application/json" -b \'session_id=%s\' -d \'%s\' http://%s:%d/battle.php';
  $cmd = sprintf($cmd, $sid, $data, $lobby_host2, $lobby_port2);
  my $res = `$cmd`;
  #$c->render(json => decode_json($res));
  $c->render(text => $res);
};

# goapi

get '/recovery' => sub {
  # for debug
  my $c = shift;
  my $sid = get_sid($c);
  my $price  = $c->param('price');
  #my $cmd = 'curl -s -X POST -H "Content-Type: application/json" -b \'session_id=%s\' -d \'{"price":%s}\' http://%s:%d/api/recovery';
  my $cmd = 'curl -s -X POST -H "Content-Type: application/json" -b \'session_id=%s\' -d \'{"price":%s}\' http://%s:%d/recovery.php';
  #$cmd = sprintf($cmd, $sid, $price, $lobby_host3, $lobby_port3);
  $cmd = sprintf($cmd, $sid, $price, $lobby_host2, $lobby_port2);
  warn $cmd;
  my $res = `$cmd`;
  #$c->render(json => decode_json($res));
  $c->render(text => $res);
};

get '/gatya' => sub {
  # for debug
  my $c = shift;
  my $sid = get_sid($c);
  my $gold  = $c->param('gold');
  #my $cmd = 'curl -s -X POST -H "Content-Type: application/json" -b \'session_id=%s\' -d \'{"gold":%s}\' http://%s:%d/api/gatya';
  my $cmd = 'curl -s -X POST -H "Content-Type: application/json" -b \'session_id=%s\' -d \'{"gold":%s}\' http://%s:%d/gacha.php';
  #$cmd = sprintf($cmd, $sid, $gold, $lobby_host3, $lobby_port3);
  $cmd = sprintf($cmd, $sid, $gold, $lobby_host2, $lobby_port2);
  my $res = `$cmd`;
  #$c->render(json => decode_json($res));
  $c->render(text => $res);
};

# pythonapi -> PHP

get '/player' => sub {
  # for debug
  my $c = shift;
  my $sid = get_sid($c);
  my $cmd = 'curl -s -X GET -H "Content-Type: application/json" -b \'session_id=%s\' http://%s:%d/player.php';
  $cmd = sprintf($cmd, $sid, $lobby_host1, $lobby_port1);
  print
  my $res = `$cmd`;
  $c->render(json => decode_json($res));
};

get '/charge' => sub {
  # for debug
  my $c = shift;
  my $sid = get_sid($c);
  my $price  = $c->param('price');
  my $cmd = 'curl -s -X POST -H "Content-Type: application/json" -b \'session_id=%s\' -d \'{"price":%s}\' http://%s:%d/charge.php';
  $cmd = sprintf($cmd, $sid, $price, $lobby_host1, $lobby_port1);
  my $res = `$cmd`;
  $c->render(json => decode_json($res));
};




app->start;

#=========#
#  subs   #
#=========#

#
# get value of session_id.
#
# return params:
# sid : client's session id.
#
sub get_sid {
  my $c = shift;
  my $sid = "";
  if(ref($c->req->cookie($session_name)) eq "Mojo::Cookie::Request"){
    # cookie: sesison_id was exists
    $sid = $c->req->cookie($session_name)->value;
  }
  return $sid;
}

#
# promise in order for hash and translate json
#
sub json_canonical_encode {
  my $href = shift || {};
  my $json = JSON::PP->new->utf8->canonical->encode($href);
  return $json;
}

__DATA__

@@ index.html.ep
% layout 'default';
% title 'Welcome';
<h1>Welcome to the Mojolicious real-time web framework!</h1>

<p><%= $sid %></p>

<script>
<!--
function doGet(url, ta) {
   console.log(url);
   var xhr = new XMLHttpRequest();
   xhr.open("GET", url);
   xhr.withCredentials = true;
   xhr.onload = () => {
     console.log(xhr.status);
     console.log("success!");
     var elm = document.getElementById(ta);
     elm.value = xhr.responseText;
     var result = JSON.parse(xhr.responseText);
     if(result.session_id !== undefined){
       document.cookie='session_id=' + result.session_id + '; path=/;';
     }
   };
   xhr.onerror = () => {
     console.log(xhr.status);
     console.log("error!");
   };
   xhr.send();
}

function jsonPost(url, data, ta) {
   console.log(url);
   var xhr = new XMLHttpRequest();
   xhr.open("POST", url);
   xhr.withCredentials = true;
   xhr.setRequestHeader("Content-Type", "application/json");
   xhr.onload = () => {
     console.log(xhr.status);
     console.log("success!");
     var elm = document.getElementById(ta);
     elm.value = xhr.responseText;
   };
   xhr.onerror = () => {
     console.log(xhr.status);
     console.log("error!");
   };
   xhr.send(data);
}

function doPost(url, data, ta) {
   console.log(url);
   var xhr = new XMLHttpRequest();
   xhr.open("POST", url);
   xhr.withCredentials = true;
   xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
   xhr.onload = () => {
     console.log(xhr.status);
     console.log("success!");
     var elm = document.getElementById(ta);
     elm.value = xhr.responseText;
   };
   xhr.onerror = () => {
     console.log(xhr.status);
     console.log("error!");
   };
   postdata = data
   xhr.send(postdata);
}

function newuserGet() {
  var user  = document.getElementById('cuser').value;
  var pass  = document.getElementById('cpass').value;
  var nname = document.getElementById('nname').value;
  var url = 'new_user?user=' + user + '&pass=' + pass + '&nick_name=' + nname;
  doGet(url, 'newuser_result');
}

function loginGet() {
  var user = document.getElementById('user').value;
  var pass = document.getElementById('pass').value;
  var url = 'login?user=' + user + '&pass=' + pass;
  doGet(url, 'login_result');
}

function uidGet() {
  var url = 'user_id';
  doGet(url, 'uid_result');
}

function uploadGet() {
  var fname = document.getElementById('file_name').value;
  var fdata = document.getElementById('file_data').value;
  var data = 'file_name=' + encodeURI(fname) + '&file_data=' + encodeURI(fdata);
  var url = 'upload';
  doPost(url, data, 'upload_result');
}

function deleteGet() {
  var url = 'delete_user';
  doGet(url, 'delete_result');
}

function recoveryGet() {
  var price = document.getElementById('price').value;
  var url = 'recovery?price=' + price;
  doGet(url, 'recovery_result');
}

function gatyaGet() {
  var gold = document.getElementById('gold').value;
  var url = 'gatya?gold=' + gold;
  doGet(url, 'gatya_result');
}

function playerGet() {
  var url = 'player';
  doGet(url, 'player_result');
}

function chargeGet() {
  var price = document.getElementById('cprice').value;
  var url = 'charge?price=' + price;
  doGet(url, 'charge_result');
}

function courseGet() {
  var url = 'courseget';
  doGet(url, 'course_result');
}

function coursePost() {
  var course_id = document.getElementById('course_id').value;
  var url = 'coursepost?course_id=' + course_id;
  doGet(url, 'coursepost_result');
  document.getElementById('ta2').value = "";
}

function battlePost() {
  var param = document.getElementById('ta2').value;
  if(param.length === 0) {
    param = document.getElementById('coursepost_result').value
  }
  jsonPost('battle', param, 'ta2');
}

-->
</script>

<h3>Create user</h3>
<div>
user: <input type="text" id="cuser" value="hogex"><br>
pass: <input type="text" id="cpass" value="password"><br>
nick_name: <input type="text" id="nname" value="hogex"><br>
<button onclick="newuserGet()">create</button>
<br>
<textarea id="newuser_result" rows="1" cols="80"></textarea><br>
</div>

<h3>Login</h3>
<div>
user: <input type="text" id="user" value="mahoyaya"><br>
pass: <input type="text" id="pass" value="password"><br>
<button onclick="loginGet()">login</button>
<br>
<textarea id="login_result" rows="1" cols="80"></textarea><br>
</div>

<h3>Get user id</h3>
<div>
<button onclick="uidGet()">check user_id</button>
<br>
<textarea id="uid_result" rows="1" cols="80"></textarea><br>
</div>

<h3>Upload image</h3>
<div>
file_name: <input type="text" id="file_name" value=""><br>
file_data: <textarea id="file_data" rows="1" cols="80"></textarea>
<br>
<button onclick="uploadGet()">upload</button>
<br>
<textarea id="upload_result" rows="1" cols="80"></textarea><br>
</div>

<h3>Withdrawal</h3>
<div>
<button onclick="deleteGet()">delete</button>
<br>
<textarea id="delete_result" rows="1" cols="80"></textarea><br>
</div>


<h3>Restore stamina</h3>
<div>
price: <input type="text" id="price" value="100"><br>
<button onclick="recoveryGet()">recover</button>
<br>
<textarea id="recovery_result" rows="1" cols="80"></textarea><br>
</div>

<h3>Gacha</h3>
<div>
gold: <input type="text" id="gold" value="100"><br>
<button onclick="gatyaGet()">gatya</button>
<br>
<textarea id="gatya_result" rows="5" cols="80"></textarea><br>
</div>


<h3>Get player info</h3>
<div>
<button onclick="playerGet()">get status</button>
<br>
<textarea id="player_result" rows="5" cols="80"></textarea><br>
</div>

<h3>Buy gold</h3>
<div>
price: <input type="text" id="cprice" value="100"><br>
<button onclick="chargeGet()">charge</button>
<br>
<textarea id="charge_result" rows="1" cols="80"></textarea><br>
</div>


<h3>Get course list</h3>
<div>
<button onclick="courseGet()">get course</button>
<br>
<textarea id="course_result" rows="5" cols="80"></textarea><br>
</div>

<h3>Select a course</h3>
<div>
course_id: <input type="text" id="course_id" value="1"><br>
<button onclick="coursePost()">set course</button>
<br>
<textarea id="coursepost_result" rows="16" cols="80"></textarea>
</div>

<h3>Battle</h3>
<div>
<button onclick="battlePost()">battle</button>
<br>
<textarea id="ta2" rows="16" cols="80"></textarea>
</div>


@@ layouts/default.html.ep
<!DOCTYPE html>
<html>
  <head><title><%= title %></title></head>
  <body><%= content %></body>
</html>


