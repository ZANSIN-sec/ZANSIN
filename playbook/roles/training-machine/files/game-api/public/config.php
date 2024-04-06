<?php
$config_yaml = yaml_parse_file('/var/www/config/config.yaml');
$_ENV["database"] = $config_yaml['mysql'];
$_ENV["redis"] = $config_yaml['redis'];
$_ENV["stamina"] = $config_yaml['stamina'];
# PLEASE DELETE THIS FILE.
