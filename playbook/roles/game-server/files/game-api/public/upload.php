<?php
require_once('./config.php');
require_once('./lib/request.php');
$request_json = get_request_json();
if (!check_required_params($request_json, array('file_name', 'file_data'))) {
    echo json_encode(array(
        "result" => "ng",
        "msg" => "Not found required param(s)"));
    exit();
}

$target_file = "./images/players/" . $request_json->file_name;

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
$stmt = $pdo->prepare('UPDATE player SET image = :image WHERE id = :user_id');
$stmt->bindParam(':image', $request_json->file_name, PDO::PARAM_STR);
$stmt->bindValue(':user_id', $user_id, PDO::PARAM_STR);
$stmt->execute();

// Check Duplicate
if (file_exists($target_file)) {
    echo json_encode(array(
        "result" => "ng",
        "msg" => "Filename is duplicate."));
    exit();
}
try {
    ob_start();
    $file = file_put_contents($target_file, base64_decode($request_json->file_data));
    if ($file) {
        echo json_encode(array("result" => "ok"));
    } else {
        $warning = ob_get_contents();
        ob_end_clean();
        if ($warning) {
            throw new Exception($warning);
        }
        echo json_encode(array(
                "result" => "ng",
                "message" => "unknown error")
        );
    }
} catch (Exception $e) {
    echo json_encode(array(
        "result" => "ng",
        "message" => $e->getMessage()
    ));
}
