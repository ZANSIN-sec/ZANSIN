<?php

header('content-type: application/json; charset=utf-8');
if(array_key_exists("HTTP_ORIGIN", $_SERVER)){
    header("Access-Control-Allow-Origin: " . $_SERVER['HTTP_ORIGIN'] . "");
    header('Access-Control-Allow-Credentials: true');
    header('Access-Control-Allow-Headers: X-Requested-With');
}

function get_request_json(){
    $request_json = json_decode(file_get_contents("php://input"));
    if(is_null($request_json)){
        echo json_encode(array(
            "result" => "ng",
            "msg" => "Invalid params."));
        exit();
    }
    return $request_json;

}

function check_required_params($request_json, $params)
{
    foreach ($params as $val) {
        if (!property_exists($request_json, $val)) {
            return false;
        }
    }
    return true;
}

function connect_db()
{
    $db = $_ENV['database'];
    $host = $db['host'];
    $database = $db['dbname'];
    $user_name = $db['user'];
    $password = $db['password'];

    try {
        $pdo = new PDO("mysql:host=$host;dbname=$database;charset=utf8", $user_name, $password);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    } catch (PDOException $e) {
        echo json_encode(array(
            "result" => "ng",
            "msg" => $e->getMessage()
        ));
        exit();
    }
    return $pdo;
}

# Coonect to Redis
function connect_redis(){
    $redis = new Redis();
    $redis->connect($_ENV['redis']['host']);
    return $redis;
}

# Check Login
function check_login($redis, $session_id){
    return $redis->get($session_id);
}

# get stamina flag
# if not exists then return false(bool)
function get_stamina_flag($redis, $key){
    $ret = $redis->get($key);
    return $ret;
}

# get battle information
# if not exists then return false(bool)
function get_battle_info($redis, $key){
    $ret = $redis->get($key);
    return $ret;
}

# get battle information
# if not exists then return false(bool)
function get_lock_flag($redis, $key){
    $ret = $redis->get($key);
    return $ret;
}

# set battle information
# if update was not success then return false(bool)
function set_battle_info($redis, $key, $value, $expire){
    $ret = $redis->set($key, $value, $expire);
    return $ret;
}

# set lock flag
function set_lock_flag($redis, $key, $value, $expire, $additional_info){
    if(!$redis->set($key, $value, $expire)){
      // is failed
      echo json_encode(array(
          "result" => "ng",
          "msg"    => "Can't update lock flag to redis: $additional_info"));
      exit();
    }
    return true;
}

# set stamina flag
function set_stamina_flag($redis, $key, $value, $expire, $additional_info){
    if(!$redis->set($key, $value, $expire)){
      // is failed
      echo json_encode(array(
          "result" => "ng",
          "msg"    => "Can't update stamina flag to redis: $additional_info"));
      exit();
    }
    return true;
}

