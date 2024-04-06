<?php
require_once('./config.php');
require_once('./lib/request.php');

$redis = connect_redis();

// check if 'price' is set as a post data
$request_json = get_request_json();
if (!check_required_params($request_json, array('price'))) {
    echo json_encode(array(
        "result" => "ng",
        "msg" => "Price is required."));
    exit();
}

// check login status
if (isset($_COOKIE['session_id'])) {
    $session_id = $_COOKIE['session_id'];
    $user_id = check_login($redis, $session_id);    
} else {
    echo json_encode(array(
        "result" => "ng",
        "msg" => "Session ID is required."));
    exit();
}

if (!$user_id) {
    echo json_encode(array(
        "result" => "ng",
        "msg" => "Invalid session ID."));
    exit();
}

// if battle is going on, chargeing is not allowed.
if ($redis->get('battle_goingon::' . $session_id) == "1") {
    echo json_encode(array(
        "result" => "ng",
        "msg" => "Battle is going on."
    ));
}

// charging process
$pdo = connect_db();
$stmt = $pdo->prepare("select gold from player where id =:id;");
$stmt->bindValue(':id', $user_id, PDO::PARAM_INT);
$stmt->execute();
$result = $stmt->fetch();
$current_amount_of_gold = $result['gold'];
$new_amount_of_gold = $current_amount_of_gold + $request_json->price;

try {
    $stmt = $pdo->prepare("UPDATE player SET gold =:charge where id =:id;");
    $stmt->bindValue(':charge', $new_amount_of_gold, PDO::PARAM_INT);
    $stmt->bindValue(':id', $user_id, PDO::PARAM_INT);
    $stmt->execute();
} catch (PDOException $e) {
    echo json_encode(array(
        "result" => "ng",
        "msg" => $e->getMessage()
    ));
    exit();
}

echo json_encode(array(
    "result" => "ok"
));