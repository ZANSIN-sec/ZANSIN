<?php
require_once('./config.php');
require_once('./lib/request.php');
$request_json = get_request_json();
if (!check_required_params($request_json, array('user_name', 'password'))) {
    echo json_encode(array(
        "result" => "ng",
        "msg" => "Not found required param(s)"));
    exit();
}

$user_name = $request_json->user_name; //user input
$password = $request_json->password; // user input
$image = "default.png";

$pdo = connect_db();
$sql = "select * from player where user_name = '$user_name' and password = '$password'";
$login_stmt= $pdo->query($sql);
$row = $login_stmt->fetch(PDO::FETCH_ASSOC);
if (!$row) {
    echo json_encode(array(
        "result" => "ng",
        "msg" => "Invalid your username and password."));
    exit();
}
$user_id = $row['id']; // Get User

// Generate Session ID
$session_id = sha1(uniqid("", 1));

// Get User Data
$user_cookie_data = $user_id;

setcookie('session_id', $session_id);
setcookie('user_data', $user_cookie_data);

$redis = connect_redis();

$redis->set($session_id, $user_id);

$redis->expire($session_id, 24 * 60 * 60);

echo json_encode(array(
    "result" => "ok",
    "session_id" => $session_id
));