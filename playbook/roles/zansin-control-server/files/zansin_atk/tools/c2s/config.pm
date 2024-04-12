package config {

  #my $parent = '8.8.8.8';
  my $parent = '127.0.0.1';
  my $sweep  = 1;

  my $record = {
    'foo.example.com' => '10.1.1.1',
    'bar.example.com' => '10.2.2.2',
    'baz.example.com' => '10.3.3.3',
  };

  sub new {
    my $c = shift;
    my $self = {
      record => $record,
      parent => $parent,
      sweep  => $sweep,
    };
    bless($self, $c);
    return $self;
  }

  sub sweep_off {
    my $c = shift;
    $c->{sweep} = 0;
    return 1;
  }

  sub sweep_on {
    my $c = shift;
    $c->{sweep} = 1;
    return 1;
  }

  sub sweep {
    my $c = shift;
    return $c->{sweep};
  }

  sub domain {
    return 'mini.loacl';
  }

  1;
}
