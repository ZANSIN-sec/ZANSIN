<?php

require_once('./config.php');
require_once('./lib/request.php');

header("Content-type: Application/JSON; charset=utf-8");
#header("Content-type: text/html; charset=utf-8");

// debug //
//var_dump($config_yaml);

// battle settings //
$max_level            = $config_yaml['battle']['max_level'];
$hmac_secret          = $config_yaml['battle']['secret'];
$max_lock_time        = 300; //sec
$stamina_expire       = 300; //sec

// stamina settings //
$stamina_interval     = $config_yaml['stamina']['recoverytime'];

// redis settings //
$redis_session_header = 'battle::';
$redis_lock_header    = 'battle_goingon::';
$redis_stamina_header = 'recovery::';


// check session_id
$session_id = @$_COOKIE['session_id'];
if($session_id === null){
    # user was not logged in
    echo json_encode(array(
        "result" => "ng",
        "msg"    => "Invalid session ID.",
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


if($_SERVER["REQUEST_METHOD"] === "POST"){
    // is_POST
    // do the battle and if battle was over then update some status, insert battle history.
    $course_id          = 0;
    $cost               = 0;
    $turn               = 0;
    $tot_damage         = 0;
    $redis_session_name = "";
    $redis_lock_name    = "";
    $redis_stamina_name = "";
    $battle_result      = 0;

    $battle_status = [
      "result" => "going_on",
      "gold"   => 0,
      "exp"    => 0,
    ];
    $required_params = [
      "course"     => "/^[\d]{1,3}$/",
      "cost"       => "/^[\d]{1,3}$/",
      "turn"       => "/^[\d]{1,3}$/",
      "tot_damage" => "/^[\d]{1,4}$/",
    ];
    $required_params_player = [
      "id"              => "/^[\d]{1,4}$/",
      "hp"              => "/^[\d]{1,4}$/",
      "str"             => "/^[\d]{1,4}$/",
      "current_stamina" => "/^[\d]{1,4}$/",
      "max_stamina"     => "/^[\d]{1,4}$/",
      "exp"             => "/^[\d]{1,10}$/",
      "gold"            => "/^[\d]{1,10}$/",
      "epoch"           => "/^[\d]{10}$/",
      "hmac"            => "/^[0-9a-f]{40}$/",
    ];
    $required_params_enemy = [
      "id"   => "/^[\d]{1,4}$/",
      "hp"   => "/^[\d]{1,4}$/",
      "str"  => "/^[\d]{1,4}$/",
      "gold" => "/^[\d]{1,5}$/",
      "exp"  => "/^[\d]{1,5}$/",
      "hmac" => "/^[0-9a-f]{40}$/",
    ];
    $result = [
        "result" => "ng",
        "msg"    => "",
    ];

    
    // debug
    //echo gettype($request_json);
    //var_dump($request_json);


    //check request param
    $request_json = get_request_json();
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
    $course_id   = $request_json->{"course"};
    $cost        = $request_json->{"cost"};
    $turn        = $request_json->{"turn"};
    $tot_damage  = $request_json->{"tot_damage"};

    // make redis key names
    $redis_stamina_name = $redis_stamina_header . $user_id;
    $redis_session_name = $redis_session_header . $session_id;

    // update application level lock 
    $lock_flag = 1;
    set_lock_flag($redis, $redis_lock_name, $lock_flag, $max_lock_time, __LINE__);

    // get stamina recover flag
    $stamina_flag = get_stamina_flag($redis, $redis_stamina_name);
    if($stamina_flag === false){
      // the flag is nil.
      $stamina_flag = 0; // initialize
    }

    // get current battle information
    $binfo_json_text = get_battle_info($redis, $redis_session_name);
    if($binfo_json_text === false){
      $lock_flag = 0;
      set_lock_flag($redis, $redis_lock_name, $lock_flag, $max_lock_time, __LINE__);
      $result["msg"] = "Can't read battle information; line:" . __LINE__;
      echo json_encode($result);
      exit();
    }

    // restore battle information
    $binfo_current_json = json_decode($binfo_json_text);
    if(is_null($binfo_current_json)){
        $result["msg"] = "Malformed JSON request; line:" . __LINE__;
        echo json_encode($result);
        exit();
    }

    // check battle phase
    if($binfo_current_json->{"phase"} > 2){
      // the battle was alredy finished
      $lock_flag = 0;
      set_lock_flag($redis, $redis_lock_name, $lock_flag, $max_lock_time, __LINE__);
      $result["msg"] = "The battle was already finished; line:" . __LINE__;
      echo json_encode($result);
      exit();
    }


    // get enemy information
    $enemy_info_json = $request_json->{"enemy"};
  
    // get player information
    $player_info_json = $request_json->{"player"};


    // check the required params: enemy
    foreach ($required_params_enemy as $key => $value) {
      if(! property_exists($enemy_info_json, $key)){
        $lock_flag = 0;
        set_lock_flag($redis, $redis_lock_name, $lock_flag, $max_lock_time, __LINE__);
        $result["msg"] = "Not found required param(s): $key; line:" . __LINE__;
        echo json_encode($result);
        exit();
      }
      if(! preg_match($required_params_enemy[$key], $enemy_info_json->{$key})){
        $lock_flag = 0;
        set_lock_flag($redis, $redis_lock_name, $lock_flag, $max_lock_time, __LINE__);
        $result["msg"] = "Invalid param(s): $key => $value; line:" . __LINE__;
        echo json_encode($result);
        exit();
      }
    }

    // check the required params: player
    foreach ($required_params_player as $key => $value) {
      if(! property_exists($player_info_json, $key)){
        $lock_flag = 0;
        set_lock_flag($redis, $redis_lock_name, $lock_flag, $max_lock_time);
        $result["msg"] = "Not found required param(s): $key; line:" . __LINE__;
        echo json_encode($result);
        exit();
      }
      if(! preg_match($required_params_player[$key], $player_info_json->{$key})){
        $lock_flag = 0;
        set_lock_flag($redis, $redis_lock_name, $lock_flag, $max_lock_time, __LINE__);
        $result["msg"] = "Invalid param(s): $key => $value; line:" . __LINE__;
        echo json_encode($result);
        exit();
      }
    }

    // compare the hmac to check correct.
    if(
      ! check_hmac($player_info_json->{"hmac"}, $binfo_current_json->{"player"}->{"hmac"}) ||
      ! check_hmac($enemy_info_json->{"hmac"}, $binfo_current_json->{"enemy"}->{"hmac"})
    ){
      # incorrect hmac
      $lock_flag = 0;
      set_lock_flag($redis, $redis_lock_name, $lock_flag, $max_lock_time, __LINE__);
      $result["msg"] = "The hmac was not correct; line:" . __LINE__;
      echo json_encode($result);
      exit();
    }


    // battle phase
    $turn++;
    $is_finish = 0;
    $status = [
      "tot_damage" => $tot_damage,
      "e_hp"       => $enemy_info_json->{"hp"},
      "e_str"      => $enemy_info_json->{"str"},
      "p_hp"       => $player_info_json->{"hp"},
      "p_str"      => $player_info_json->{"str"},
      "fin"        => 0,
      "result"     => "",
    ];

    // the player gets right to attack first always
    $status = strike_player($status);
  
    // update status
    $enemy_info_json->{"hp"}   = $status["e_hp"];
    $enemy_info_json->{"str"}  = $status["e_str"];
    $player_info_json->{"hp"}  = $status["p_hp"];
    $player_info_json->{"str"} = $status["p_str"];
  
    if($status["fin"] > 0){
      // battle is end
      if($status["result"] === "win"){
        // player win
        $battle_result = 1;
      } else {
        // enemy win
        $battle_result = 2;
      }
    } else {
      // battle is still going on
    }
  

    // enemy
    // promise to order of output for json. if forget the this step, so may will be change the hmac value for each time.
    unset($enemy_info_json->{"hmac"});
    $enemy_info_array = json_decode(json_encode($enemy_info_json), true);
    ksort($enemy_info_array);
    $einfo_json = json_encode($enemy_info_array);
    // add hmac for prevent falsification
    $cksum = hash_hmac('sha1', $einfo_json, $hmac_secret);
    $enemy_info_json->{"hmac"} = $cksum;
    $result["enemy"]           = $enemy_info_json;
  
    // player
    // promise to order of output for json. if forget the this step, so may will be change the hmac value for each time.
    unset($player_info_json->{"hmac"});
    $player_info_array = json_decode(json_encode($player_info_json), true);
    ksort($player_info_array);
    $pinfo_json = json_encode($player_info_array);
    // add hmac for prevent falsification
    $cksum = hash_hmac('sha1', $pinfo_json, $hmac_secret);
    $player_info_json->{"hmac"} = $cksum;
    $result["player"]           = $player_info_json;
  

    // append course_id, battle phase, battle cost
    if($battle_result == 0){
      $result["phase"] = 2;
    } else {
      $result["phase"] = 3;
    }
    $result["cost"]   = $cost;
    $result["course"] = $course_id;



    // update battle information to redis
    ksort($result);
    $binfo_json = json_encode($result);

    // for debug: before update
    //$redis_binfo = get_battle_info($redis, $redis_session_name);
    //if($redis_binfo === false){
    //  $lock_flag = 0;
    //  set_lock_flag($redis, $redis_lock_name, $lock_flag, $max_lock_time, __LINE__);
    //  $result["msg"] = "Can't read battle information.";
    //  echo json_encode($result);
    //  exit();
    //}
    //var_dump(json_decode($redis_binfo));

    if(! set_battle_info($redis, $redis_session_name, $binfo_json, $max_lock_time)){
      $lock_flag = 0;
      set_lock_flag($redis, $redis_lock_name, $lock_flag, $max_lock_time, __LINE__);
      $result["msg"] = "Can't update battle information; line:" . __LINE__;
      echo json_encode($result);
      exit();
    }

    // for debug: after update
    //$redis_binfo = get_battle_info($redis, $redis_session_name);
    //if($redis_binfo === false){
    //  $lock_flag = 0;
    //  set_lock_flag($redis, $redis_lock_name, $lock_flag, $max_lock_time, __LINE__);
    //  $result["msg"] = "Can't read battle information.";
    //  echo json_encode($result);
    //  exit();
    //}
    //var_dump(json_decode($redis_binfo));





    // connect database
    $pdo  = connect_db();


    // update player information if battle was finished
    if( $result["phase"] === 3 && $status["fin"] > 0 ){
      // get current player information
      $rv = 0;
      $sql = 'select level, stamina, gold, exp, unix_timestamp(staminaupdated_at) as epoch from player where id = :user_id limit 1';
      try {
        $stmt = $pdo->prepare($sql);
        $stmt->bindValue(':user_id', $user_id, PDO::PARAM_STR);
        $stmt->execute();
      } catch(PDOException $e){
        // is failed
        $lock_flag = 0;
        set_lock_flag($redis, $redis_lock_name, $lock_flag, $max_lock_time, __LINE__);
        //printf("[%s] redis_battle_goingon: %s:%s\n", "*", $redis_lock_name, $lock_flag);
        $result["msg"] = "Can't find player information: " . $e->getMessage() . "; line:" . __LINE__;
        echo json_encode($result);
        exit();
      }
      $pinfo_current_array = $stmt->fetch(PDO::FETCH_ASSOC);
      //printf("[%s] player_info_current:\n", "*");
      //var_dump($pinfo_current_array);




  
      // set new status and battle status
      // decide to current status
      $max_stamina   = $player_info_json->{"max_stamina"};     // from request json
      $cur_stamina   = $player_info_json->{"current_stamina"}; // from request json
      $pinfo_stamina = get_current_stamina($pinfo_current_array, $cur_stamina, $max_stamina, $stamina_flag);
      $pinfo_gold    = $pinfo_current_array["gold"];
      $pinfo_exp     = $pinfo_current_array["exp"];

      // update status
      if($status["result"] === "win"){
        $pinfo_gold += $enemy_info_json->{"gold"};
        $pinfo_exp  += $enemy_info_json->{"exp"};
        $battle_status["result"] = "win"; 
        $battle_status["gold"]   = $enemy_info_json->{"gold"}; 
        $battle_status["exp"]    = $enemy_info_json->{"exp"};
      } elseif($status["result"] === "lose"){
        $battle_status["result"] = "lose"; 
      }

      // decide to current stamina at after battle
      $pinfo_stamina -= $cost;
      $player_info_json->{"current_stamina"} = $pinfo_stamina;
  

      // judge player level
      $current_level    = $pinfo_current_array["level"];
      $cap              = 0;
      $max_stamina_next = 0;
      while(!$cap && $current_level < $max_level){
        $sql_max_stamina_next = 'select max_stamina from level where level = :current_level limit 1';
        try {
          $stmt = $pdo->prepare($sql_max_stamina_next);
          $stmt->bindValue(':current_level', $current_level, PDO::PARAM_INT);
          $stmt->execute();
        } catch(PDOException $e){
          // is failed
          $lock_flag = 0;
          set_lock_flag($redis, $redis_lock_name, $lock_flag, $max_lock_time, __LINE__);
          //printf("[%s] redis_battle_goingon: %s:%s\n", "*", $redis_lock_name, $lock_flag);
          $result["msg"] = "Can't execute query: " . $e->getMessage() . "; line:" . __LINE__;
          echo json_encode($result);
          exit();
        }
        $row_stamina      = $stmt->fetch(PDO::FETCH_ASSOC);
        $max_stamina_next = $row_stamina["max_stamina"];

        $sql_level = 'select 1 from level where (select need_exp from level where level = :current_level1) <= :pinfo_exp - (select sum(need_exp) from level where level <= :current_level2) limit 1';
        try {
          $stmt = $pdo->prepare($sql_level);
          $stmt->bindValue(':current_level1', $current_level, PDO::PARAM_INT);
          $stmt->bindValue(':current_level2', $current_level, PDO::PARAM_INT);
          $stmt->bindValue(':pinfo_exp',      $pinfo_exp,     PDO::PARAM_INT);
          $stmt->execute();
        } catch(PDOException $e){
          // is failed
          $lock_flag = 0;
          set_lock_flag($redis, $redis_lock_name, $lock_flag, $max_lock_time, __LINE__);
          //printf("[%s] redis_battle_goingon: %s:%s\n", "*", $redis_lock_name, $lock_flag);
          $result["msg"] = "Can't execute query: " . $e->getMessage() . "; line:" . __LINE__;
          echo json_encode($result);
          exit();
        }

        $rv   = $stmt->rowCount();
        if($rv === 1){
          // bump up level
          $current_level++;
          // level up bonus: recover stamina
          $pinfo_stamina = $max_stamina_next;
        } else {
          $cap++;
        }

      }


      // update database to refrect new player information
      // and insert battle history record.
      $sql_level   = 'update player set level=:current_level, stamina=:pinfo_stamina, gold=:pinfo_gold, exp=:pinfo_exp, staminaupdated_at=now() where id=:user_id limit 1';
      $sql_history = 'insert into battle_history (user_id, enemy_id, course_id, result, turn_count, total_damage, get_exp, get_gold, created_at) values(:user_id, :enemy_id, :course_id, :battle_result, :turn, :tot_damage, :exp, :gold, now())';
      try {
        $pdo->beginTransaction();
        $stmt = $pdo->prepare($sql_level);
        $stmt->bindValue(':current_level', $current_level, PDO::PARAM_INT);
        $stmt->bindValue(':pinfo_stamina', $pinfo_stamina, PDO::PARAM_INT);
        $stmt->bindValue(':pinfo_gold',    $pinfo_gold,    PDO::PARAM_INT);
        $stmt->bindValue(':pinfo_exp',     $pinfo_exp,     PDO::PARAM_INT);
        $stmt->bindValue(':user_id',       $user_id,       PDO::PARAM_INT);
        $stmt->execute();
        $stmt = $pdo->prepare($sql_history);
        $stmt->bindValue(':user_id',       $user_id,                 PDO::PARAM_INT);
        $stmt->bindValue(':enemy_id',      $enemy_info_json->{"id"}, PDO::PARAM_INT);
        $stmt->bindValue(':course_id',     $course_id,               PDO::PARAM_INT);
        $stmt->bindValue(':battle_result', $battle_status["result"], PDO::PARAM_STR);
        $stmt->bindValue(':turn',          $turn,                    PDO::PARAM_INT);
        $stmt->bindValue(':tot_damage',    $status["tot_damage"],    PDO::PARAM_INT);
        $stmt->bindValue(':gold',          $battle_status["gold"],   PDO::PARAM_INT);
        $stmt->bindValue(':exp',           $battle_status["exp"],    PDO::PARAM_INT);
        $pdo->commit();
      } catch(PDOException $e){
        // is failed
        $pdo->rollBack();
        set_stamina_flag($redis, $redis_stamina_name, $stamina_flag, 3600 * 24 * 365, __LINE__);
        //printf("[%s] redis_battle_goingon: %s:%s\n", "*", $redis_stamina_name, $stamina_flag);
        $lock_flag = 0;
        set_lock_flag($redis, $redis_lock_name, $lock_flag, $max_lock_time, __LINE__);
        //printf("[%s] redis_battle_goingon: %s:%s\n", "*", $redis_lock_name, $lock_flag);
        $result["msg"] = "Can't update player information and history: " . $e->getMessage() . "; line:" . __LINE__;
        echo json_encode($result);
        exit();
      }
      if($stamina_flag > 0){
        // reset stamina flag
        set_stamina_flag($redis, $redis_stamina_name, 0, $stamina_expire, __LINE__);
        //printf("[%s] redis_stamina_recovery:%s:%s", "*", $redis_stamina_name, 0));
      }
    }



    // update application level lock
    $lock_flag = 0;
    set_lock_flag($redis, $redis_lock_name, $lock_flag, $max_lock_time, __LINE__);
    //printf("[%s] redis_battle_goingon: %s:%s\n", "*", $redis_lock_name, $lock_flag);
  
    // update result
    $result["result"]     = "ok";
    $result["status"]     = $battle_status;
    $result["turn"]       = $turn;
    $result["tot_damage"] = $status["tot_damage"];
  
    echo json_encode($result);
  };


//// functions ////
//
// get current stamina
//
// return params:
//  pinfo_stamina: number of stamina; INT
//
function get_current_stamina($player_info, $pinfo_stamina, $max_stamina, $stamina_flag){
  global $stamina_interval;

  // get current time(epoch)
  $current_epoch = time();
  // amount of gain stamina
  $incr_stamina  = floor(($current_epoch - $player_info["epoch"]) / $stamina_interval);

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

//
// check the hmac
//
// return params:
// general return code
function check_hmac($hmac, $hmac_old) {
  $ret = 1; # I will implement later...
  return $ret;
}

//
// battle function
// 
// return params:
// p_hp : player hp
// p_str : player str
// e_hp : enemy hp
// e_str : enemy str
// fin : status of battle. the battle was over if this value was not zero.
// result : status of battle that seen from player.
//
function strike_player($status) {

  // is player turn
  if($status["e_hp"] > 0){
    // fine
    $status["e_hp"] -= $status["p_str"];
    $status["tot_damage"] += $status["p_str"];
  } else {
    // dead
  }

  if($status["e_hp"] <= 0){
    $status["fin"]++; 
    $status["result"] = "win";
  }

  if(! $status["fin"]){
    // is enemy turn
    if($status["p_hp"] > 0){
      // fine
      $status["p_hp"] -= $status["e_str"];
    } else {
      // dead
    }
  }

  if($status["p_hp"] <= 0){
     $status["fin"]++; 
     $status["result"] = "lose";
  }

  return $status;
}


?>
