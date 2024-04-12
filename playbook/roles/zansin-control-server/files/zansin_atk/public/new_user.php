<?php
require_once('../../config.php');
require_once('../../lib/request.php');
$request_json = get_request_json();
if (!check_required_params($request_json, array('user_name', 'password', 'nick_name'))) {
    echo json_encode(array(
        "result" => "ng",
        "msg" => "Not found required param(s)"));
    exit();
}

$user_name = $request_json->user_name; //user input
$password = $request_json->password; // user input
$nick_name = $request_json->nick_name; // user input
$image = "default.png";

$pdo = connect_db();

$dup_stmt = $pdo->query("select count(*) from player where user_name = '$user_name';");
$dup_count = $dup_stmt->fetchColumn();
if(0 < $dup_count){
    echo json_encode(array(
        "result" => "ng",
        "msg" => "Username is duplicate."));
    exit();
}

$params = array(
    ":user_name" => $user_name,
    ":password" => $password,
    ":nick_name" => $nick_name,
    ":image" => $image,
    ":level" => 99,
    ":stamina" => 9999999,
    ":weapon_id" => 1,
    ":armor_id" => 1,
    ":gold" => 9999999,
    ":exp" => 9999999,
    ":created_at" => date("Y-m-d H:i:s"),
    ":staminaupdated_at" => date("Y-m-d H:i:s")
);

try {
    $stmt = $pdo->prepare(
        "INSERT INTO player (
                     user_name, password, nick_name, image, level, stamina, weapon_id,
                     armor_id, gold, exp, created_at, staminaupdated_at
                     ) VALUES (
                     :user_name, :password, :nick_name, :image, :level, :stamina, :weapon_id,
                     :armor_id, :gold, :exp, :created_at, :staminaupdated_at)"
    );
    foreach ($params as $key => &$val) {
        $stmt->bindParam($key, $val);
    }
    $stmt->execute();
    $user_id = $pdo->lastInsertId('id');
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