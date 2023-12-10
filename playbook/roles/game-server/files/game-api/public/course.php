<?php

require_once('./config.php');
require_once('./lib/request.php');

header("Content-type: Application/JSON; charset=utf-8");
#header("Content-type: text/html; charset=utf-8");

// debug //
//var_dump($config_yaml);

// battle settings //
$hmac_secret          = $config_yaml['battle']['secret'];

// stamina settings //
$stamina_interval     = $config_yaml['stamina']['recoverytime'];

// redis settings //
$redis_session_header = 'battle::';
$redis_lock_header    = 'battle_goingon::';
$redis_stamina_header = 'recovery::';


$result = [
    "result" => "ng",
    "msg"    => "",
];

// check session_id
$session_id = @$_COOKIE['session_id'];
if($session_id === null){
    # user was not logged in
    $result["msg"] = "Invalid session ID.";
    echo json_encode($result);
    exit();
}

// check login status
$redis      = connect_redis();
$user_id    = check_login($redis, $session_id);
if(!$user_id){
    # user was not logged in
    $result["msg"] = "Invalid session ID.";
    echo json_encode($result);
    exit();
}


if($_SERVER["REQUEST_METHOD"] === "GET"){
    // is_GET
    // get course informations
    $pdo = connect_db();
    try {
        $stmt = $pdo->prepare("SELECT id,name,stamina FROM course");
        $stmt->execute();
    } catch(PDOException $e){
        // is failed
        $result["msg"] = "Can't find course:" . $e->getMessage(). "; line:" . __LINE__;
        echo json_encode($result);
        exit();
   }
    
   $course = array();
   $courseData = array();
   while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        $courseData =[
            'id'      => $row['id'],
            'name'    => $row['name'],
            'stamina' => $row['stamina'],
        ];
        array_push($course, $courseData);
    }
    $result["course"] = $course;
    $result["result"] = "ok"; 
    echo json_encode($result);

} elseif($_SERVER["REQUEST_METHOD"] === "POST") {
    // is_POST
    // set course setting
    $required_params = [
        "id" => '/^[\d]{1,3}$/',
    ];

    $course_id = 0;
    $request_json = get_request_json();
    
    // debug
    //echo gettype($request_json);
    //var_dump($request_json);

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
    $course_id = $request_json->{"id"};

    // debug
    //$result["msg"] = "id:" . $course_id;
    //echo json_encode($result);

    // make redis key names
    $redis_stamina_name = $redis_stamina_header . $user_id;
    $redis_session_name = $redis_session_header . $session_id;

    
    // get stamina recover flag
    $stamina_flag = get_stamina_flag($redis, $redis_stamina_name);
    if($stamina_flag === false){
      // the flag is nil.
      $stamina_flag = 0; // initialize
    }




    // check course id via database, and get course information
    $pdo  = connect_db();
    $sql  = 'select id, stamina from course where id = :course_id limit 1';
    try {
      $stmt = $pdo->prepare($sql);
      $stmt->bindValue(':course_id', $course_id, PDO::PARAM_STR);
      $stmt->execute();
    } catch(PDOException $e){
        // is failed
        $result["msg"] = "Can't find course id:"  . $e->getMessage() . "; line:" . __LINE__;
        echo json_encode($result);
        exit();
    }
    //    $courseData =[
    //        'id'      => $row['id'],
    //        'name'    => $row['name'],
    //        'stamina' => $row['stamina'],
    //    ];
    $course_info = $stmt->fetch(PDO::FETCH_ASSOC);
    $cost = $course_info["stamina"];
  

    // get player information from user_id via database
    $sql = 'select p.id, p.user_name, p.nick_name, p.image as player_image, p.level, l.max_hp as base_hp, l.max_str as base_str, (l.max_hp + a.param) as hp, (l.max_str + w.param) as str, p.stamina as current_stamina, l.max_stamina, unix_timestamp(p.staminaupdated_at) as epoch, p.gold, p.exp, w.name as wepon, a.name as armor from player as p inner join equipment as w on p.weapon_id=w.id inner join equipment as a on p.armor_id=a.id inner join level as l on p.level=l.level where p.id= :user_id';
    try {
      $stmt = $pdo->prepare($sql);
      $stmt->bindValue(':user_id', $user_id, PDO::PARAM_STR);
      $stmt->execute();
    } catch(PDOException $e) {
      // is failed
      $result["msg"] = "Can't find player information: " . $e->getMessage() . "; line:" . __LINE__;
      echo json_encode($result);
      exit();
    }

    $player_info = $stmt->fetch(PDO::FETCH_ASSOC);
    #### promise to order of output for json. if forget the this step, so may will be change the hmac value for each time. ####
    ksort($player_info);
    $pinfo_json = json_encode($player_info);

  
    // decide to current stamina
    $pinfo_stamina = get_current_stamina($player_info, $stamina_flag);
    if($pinfo_stamina < $cost){
      $result["msg"] = "You lacking stamina.";
      $result["current_stamina"] = $pinfo_stamina;
      echo json_encode($result);
      exit();
    }
  
  
    // add hmac for prevent falsification
    $cksum = hash_hmac('sha1', $pinfo_json, $hmac_secret);
    $player_info["hmac"] = $cksum;
    $result["player"]    = $player_info;
  
  
    // get enemy information from course_id via database
    $sql = 'select id, hp, str, gold, exp, name, image from enemy where course_id = :course_id limit 1';
    try {
      $stmt = $pdo->prepare($sql);
      $stmt->bindValue(':course_id', $course_id, PDO::PARAM_STR);
      $stmt->execute();
    } catch(PDOException $e) {
      // is failed
      $result["msg"] = "Can't find enemy information: " . $e->getMessage() . "; line:" . __LINE__;
      echo json_encode($result);
      exit();
    }

    $enemy_info = $stmt->fetch(PDO::FETCH_ASSOC);
    #### promise to order of output for json. if forget the this step, so may will be change the hmac value for each time. ####
    ksort($enemy_info);
    $einfo_json = json_encode($player_info);

    // add hmac for prevent falsification
    $cksum = hash_hmac('sha1', $einfo_json, $hmac_secret);
    $enemy_info["hmac"] = $cksum;
    $result["enemy"]     = $enemy_info;

    // append course_id, battle phase, battle cost
    $result["phase"]  = 1;
    $result["course"] = $course_id;
    $result["cost"]   = $cost;
  
  
    // update battle information to redis
    ksort($result);
    $binfo_json = json_encode($result);
    //$redis_binfo = get_battle_info($redis, $redis_session_name);
    //if($redis_binfo === false){
    //  $result["msg"] = "Can't read battle information.";
    //  echo json_encode($result);
    //  exit();
    //} else {
    //  var_dump($redis_binfo);
    //}
    if(! set_battle_info($redis, $redis_session_name, $binfo_json, 300)){
      // is failed
      $result["msg"] = "Can't update battle informatin; line:" . __LINE__;
      echo json_encode($result);
      exit();
    }
    $redis_binfo = get_battle_info($redis, $redis_session_name);

    #
    # update result
    #
    $result["result"]           = "ok";
    $result["turn"]             = 0;
    $result["tot_damage"]       = 0;
    $result["stamina_recovery"] = $stamina_flag;
  
    echo json_encode($result);
    
}

function get_current_stamina($player_info, $stamina_flag){
  global $stamina_interval;

  // get current time(epoch)
  $current_epoch = time();
  $incr_stamina  = floor(($current_epoch - $player_info["epoch"]) / $stamina_interval);
  $max_stamina   = $player_info["max_stamina"];
  $pinfo_stamina = $player_info["current_stamina"];

  if($stamina_flag > 0){
    // is recovery on
    $pinfo_stamina = $max_stamina;
  } elseif($pinfo_stamina + $incr_stamina >= $max_stamina){
    // is overflow
    $pinfo_stamina = $max_stamina;
  } else {
    $pinfo_stamina += $incr_stamina;
  }

  return $pinfo_stamina;
}
?>
