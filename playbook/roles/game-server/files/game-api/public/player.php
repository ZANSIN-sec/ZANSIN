<?php
require_once('./config.php');
require_once('./lib/request.php');

$redis = connect_redis();

// check login status
// checking "user_data" is for debbuging only!
// checking "session_id" is mandatory!
if (isset($_COOKIE['user_data'])) {
    $user_id = $_COOKIE['user_data'];
} elseif (isset($_COOKIE['session_id'])) {
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

// obtain the value of stamina recovery interval from config
$stamina_env = $_ENV['stamina'];
$recoverytime = $stamina_env['recoverytime'];

// obtain the player data from DB
$pdo = connect_db();
$stmt = $pdo->prepare("SELECT * FROM player where id =:id;");
$stmt->bindValue(':id', $user_id, PDO::PARAM_INT);
$stmt->execute();
$userData = array();
$rows_found = false;
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $rows_found = true;
    $userData =[
        'id' => $row['id'],
        'user_name' => $row['user_name'],
        'password' => $row['password'],
        'nick_name' => $row['nick_name'],
        'image' => $row['image'],
        'level' => $row['level'],
        'stamina' => $row['stamina'],
        'weapon_id' => $row['weapon_id'],
        'armor_id' => $row['armor_id'],
        'gold' => $row['gold'],
        'exp' => $row['exp'],
        'created_at' => $row['created_at'],
        'staminaupdated_at' => $row['staminaupdated_at']
    ];
}
if(!$rows_found) {
    echo json_encode(array(
        "result" => "ng",
        "msg" => "No Player was found."));
    exit();
}

// obtain the values for each level of player from DB
$stmt = $pdo->prepare("SELECT * FROM level where level =:level;");
$stmt->bindValue(':level', $userData['level'], PDO::PARAM_INT);
$stmt->execute();    
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $userData += array('max_hp' => $row['max_hp']);
    $userData += array('max_str' => $row['max_str']);
    $userData += array('max_stamina' => $row['max_stamina']);
    $userData += array('need_exp' => $row['need_exp']);
}

// obtain the data of weapons from DB
$stmt = $pdo->prepare("SELECT * FROM equipment where id =:weapon_id;");
$stmt->bindValue(':weapon_id', $userData['weapon_id'], PDO::PARAM_INT);
$stmt->execute();    
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $userData += array('weapon_name' => $row['name']);
    $userData += array('weapon_rarity' => $row['rarity']);
    $userData += array('weapon_param' => $row['param']);
}

// obtain the data of armors from DB
$stmt = $pdo->prepare("SELECT * FROM equipment where id =:armor_id;");
$stmt->bindValue(':armor_id', $userData['armor_id'], PDO::PARAM_INT);
$stmt->execute();    
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $userData += array('armor_name' => $row['name']);
    $userData += array('armor_rarity' => $row['rarity']);
    $userData += array('armor_param' => $row['param']);
}

// if the recovery flag for the player in redis is "1", rewrite the value of stamina as "max_stamina"
if ($redis->get('recovery::' . $user_id) == "1") {
    $userData['stamina'] = $userData['max_stamina'];
}

// calculate the delta (sec) between current time and staminaupdated_at, then recover stamina by the value of delta
$delta_sec = strtotime(date('Y-m-d H:i:s')) - strtotime($userData['staminaupdated_at']);
$recovery = floor($delta_sec/$recoverytime);
if ($userData['stamina'] + $recovery >= $userData['max_stamina']) {
    $userData['stamina'] = $userData['max_stamina'];
} else {
    $userData['stamina'] = $userData['stamina'] + $recovery;
}

// add "ok"
$userData += array('result' => 'ok');

echo json_encode($userData);
