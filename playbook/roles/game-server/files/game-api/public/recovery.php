<?php

require_once('./config.php');
require_once('./lib/request.php');

header("Content-type: Application/JSON; charset=utf-8");
#header("Content-type: text/html; charset=utf-8");

// debug //
//var_dump($config_yaml);

// redis settings //
$redis_lock_header    = 'battle_goingon::';
$redis_stamina_header = 'recovery::';


// check session_id
$session_id = @$_COOKIE['session_id'];
if($session_id === null){
    # user was not logged in
    echo json_encode(array(
        "result" => "ng",
        "msg"    => "Invalid session ID.",
        //"msg"    => "Can't find Cookie.",
    ));
    exit();
}

// check login status
$redis      = connect_redis();
$user_id    = check_login($redis, $session_id);
if(!$user_id){
    # user was not logged in
    echo json_encode(array(
        "result" => "ng",
        "msg"    => "Invalid session ID.",
    ));
    exit();
}

// make redis key names
$redis_lock_name    = $redis_lock_header . $session_id;
$redis_stamina_name = $redis_stamina_header . $user_id;


if($_SERVER["REQUEST_METHOD"] === "GET"){
    // is_GET
    echo json_encode(array(
        "result" => "ng",
        "msg"    => "Allowed Method POST Only",
    ));
    exit();

} elseif($_SERVER["REQUEST_METHOD"] === "POST") {
    // is_POST

    // set recovery setting
    $result = [
        "result" => "ng",
        "msg"    => "",
    ];
    $required_params = [
        "price" => '/^[\d]{1,4}$/',
    ];

    // check content type
    $ctype = $_SERVER["CONTENT_TYPE"];
    if($ctype !== "application/json"){
        $result["msg"] = "different Content-Type: " . $ctype . "; line:" . __LINE__;
        echo json_encode($result);
        exit;
    }

    // get battle flag from redis
    $battle_lock_flag = get_lock_flag($redis, $redis_lock_name);

    // don't update stamina flag when the battle is still in progress
    if($battle_lock_flag === 1){
        $result["msg"] = "internal error; line:" . __LINE__;
        echo json_encode($result);
        exit;
    }

    // read json
    $request_json = get_request_json();
    
    // debug
    //echo gettype($request_json);
    //var_dump($request_json);

    // validate params
    foreach ($required_params as $key => $value) {
      if(! property_exists($request_json, $key)){
        $result["msg"] = "Not found required param(s): $key; line:" . __LINE__;
        echo json_encode($result);
        exit();
      }
      if(! preg_match($required_params[$key], $request_json->{$key})){
        $result["msg"] = "Invalid param(s): $key => $value; line:" . __LINE__;
        echo json_encode($result);
        exit();
      }
    }

    // get stamina recover flag
    $stamina_flag = get_stamina_flag($redis, $redis_stamina_name);
    if($stamina_flag === false){
      // the flag is nil.
      $stamina_flag = 0; // initialize
    }

    // stop processing when the flag is 1
    //echo "[*] gettype: " . gettype($stamina_flag) . ";";
    //echo "[*] stamina_flag: " . $stamina_flag . ";";
    if(intval($stamina_flag) === 1){
        $result["msg"] = "Your stamina has already recovered; line:" . __LINE__;
        echo json_encode($result);
        exit();
    }

    // set the flag to redis
    set_stamina_flag($redis, $redis_stamina_name, 1, 3600 * 24 * 365, __LINE__);

    // subtract gold
    $pdo = connect_db();
    try {
      subtractgold($pdo, $user_id, $request_json->{'price'});
    } catch(PDOException $e){
      // is failed
      $result["msg"] = "Can't update database:"  . $e->getMessage() . "; line:" . __LINE__;
      echo json_encode($result);
      exit();
    }

    // send response
    $result["result"] = "ok";
    $result["msg"]    = "no error";
    echo json_encode($result);
}


//
// update value of gold on database
// return: bool
//
function subtractgold($pdo, $user_id, $price){
  // get current gold from database
  $sql1  = 'select gold from player where id = :user_id limit 1';
  try {
    $stmt = $pdo->prepare($sql1);
    $stmt->bindValue(':user_id', $user_id, PDO::PARAM_INT);
    $stmt->execute();
  } catch(PDOException $e){
      // is failed
      throw $e;
  }
  $player_info = $stmt->fetch(PDO::FETCH_ASSOC);
  $gold = $player_info["gold"];

  // update gold on database
  $sql2 = 'update player set gold = :gold where id = :user_id';
  try {
    $stmt = $pdo->prepare($sql2);
    $stmt->bindValue(':gold',    $gold - $price, PDO::PARAM_INT);
    $stmt->bindValue(':user_id', $user_id,       PDO::PARAM_INT);
    $stmt->execute();
  } catch(PDOException $e){
      // is failed
      throw $e;
  }

  return true;
}

?>
