<?php
require_once('./config.php');
require_once('./lib/request.php');

$session_id = $_COOKIE['session_id'];

$redis = connect_redis();

$user_id = check_login($redis, $session_id);

if(!$user_id){
    echo json_encode(array(
        "result" => "ng",
        "msg" => "Invalid session ID."));
    exit();
}

echo json_encode(array(
    "result" => "ok",
    "user_id" => $user_id
));