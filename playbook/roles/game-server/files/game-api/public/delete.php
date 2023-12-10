<?php
require_once('./config.php');
require_once('./lib/request.php');

// Check Login
$session_id = $_COOKIE['session_id'];
$redis = connect_redis();
$user_id = check_login($redis, $session_id);
if (!$user_id) {
    echo json_encode(array(
        "result" => "ng",
        "msg" => "Invalid session ID."));
    exit();
}

$pdo = connect_db();
$stmt = $pdo->prepare('delete from player WHERE id = :user_id');
$stmt->bindValue(':user_id', $user_id, PDO::PARAM_STR);
$stmt->execute();

echo json_encode(array("result" => "ok"));