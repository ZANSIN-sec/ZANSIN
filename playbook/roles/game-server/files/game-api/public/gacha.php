<?php
require_once('./config.php');
require_once('./lib/request.php');

$request_json = get_request_json();
if (!check_required_params($request_json, array('gold'))) {
    echo json_encode(array(
        "result" => "ng",
        "msg" => "Gold is required."));
    exit();
}

//check login status
$session_id = $_COOKIE['session_id'];
$redis = connect_redis();
$user_id = check_login($redis, $session_id);

if (!$user_id) {
    echo json_encode(array(
        "result" => "ng",
        "msg" => "Invalid session ID."));
    exit();
}

//don't process during battle
if ($redis->get('battle_goingon::' . $session_id) == "1") {
    echo json_encode(array(
        "result" => "ng",
        "msg" => "Battle is going on."
    ));
}

//get player data
try{
    $pdo = connect_db();
    $stmt = $pdo->prepare("SELECT weapon_id,armor_id,gold FROM player WHERE id =:id;");
    $stmt->bindValue(':id', $user_id, PDO::PARAM_INT);
    $stmt->execute();
    $result = $stmt->fetch();

    $current_weapon_id = $result["weapon_id"];
    $current_armor_id = $result["armor_id"];
    $current_gold = $result["gold"];
    $post_gold = $request_json->gold;
} catch(PDOException $e){
    echo json_encode(array(
        "result" => "ng",
        "msg" => $e->getMessage()
    ));
    exit();
}

//compare current gold and post value
if($current_gold < $post_gold) {
    echo json_encode(array(
        "name" => "",
        "rarity" => "",
        "result" => "ok",
        "resulttype" => 1,
        "type" => ""
    ));
    exit();
}

//rarity drawing
$result_rarity = draw_rarity();

//extract the equipment data of the selected rarity
try{
    $stmt = $pdo->prepare("SELECT id FROM equipment WHERE rarity = :rarity");
    $stmt->bindValue(':rarity', $result_rarity, PDO::PARAM_STR);
    $stmt->execute();
    $draw_target = $stmt->fetchAll();
} catch(PDOException $e){
    echo json_encode(array(
        "result" => "ng",
        "msg" => $e->getMessage()
    ));
    exit();
}

//drawing extracted equipment data
$result_id = $draw_target[random_int(0,count($draw_target)-1)];

//get data for selected equipment
try{    
    $stmt = $pdo->prepare("SELECT id,type,rarity,name,param FROM equipment WHERE id = :id;");
    $stmt->bindValue(':id', $result_id["id"], PDO::PARAM_INT);
    $stmt->execute();
    $result_data = $stmt->fetch();
} catch(PDOException $e){
    echo json_encode(array(
        "result" => "ng",
        "msg" => $e->getMessage()
    ));
    exit();
}

//get data on the player's current equipment
if($result_data["type"] == "weapon"){
	$serch_id = $current_weapon_id;
} else {
	$serch_id = $current_armor_id;
}
try{
    $stmt = $pdo->prepare("SELECT id,type,rarity,name,param FROM equipment WHERE id = :serch_id;");
    $stmt->bindValue(':serch_id', $serch_id, PDO::PARAM_INT);
    $stmt->execute();
    $current_data = $stmt->fetch();
} catch(PDOException $e){
    echo json_encode(array(
        "result" => "ng",
        "msg" => $e->getMessage()
    ));
    exit();
}

//equipment data is updated when performance is good
if($result_data["param"] > $current_data["param"]){
    if($result_data["type"] == "weapon"){
        $query = "UPDATE player SET weapon_id = :equipment_id WHERE id = :user_id;";
    } else {
        $query = "UPDATE player SET armor_id = :equipment_id WHERE id = :user_id;";
    }
    try{
        $stmt = $pdo->prepare($query);
        $stmt->bindValue(':equipment_id', $result_data["id"], PDO::PARAM_INT);
        $stmt->bindValue(':user_id', $user_id, PDO::PARAM_INT);
        $stmt->execute();        
    } catch(PDOException $e){
        echo json_encode(array(
            "result" => "ng",
            "msg" => $e->getMessage()
        ));
        exit();
    }
    $resulttype = 3;
}else{
    $resulttype = 2;
}

//subtract payment from current gold 
$result_gold = $current_gold - $post_gold;

try{
    $stmt = $pdo->prepare("UPDATE player SET gold = :result_gold WHERE id = :user_id");
    $stmt->bindValue(':result_gold', $result_gold, PDO::PARAM_INT);
    $stmt->bindValue(':user_id', $user_id, PDO::PARAM_INT);
    $stmt->execute();
} catch(PDOException $e){
    echo json_encode(array(
        "result" => "ng",
        "msg" => $e->getMessage()
    ));
    exit();
}

//return the result as a response
echo json_encode(array(
    "name" => $result_data["name"],
    "rarity" => $result_rarity,
    "result" => "ok",
    "resulttype" => $resulttype,
    "type" => $result_data["type"]
));

//rarity drawing process
function draw_rarity(){
   
    // SR 0.01%   R 0.99%  // N 99%
    $gachaweights  = array(1, 99, 9900);

    $boundaries[0] = 0;
    for($i = 1; $i <= count($gachaweights); $i++){
        $boundaries[$i] = $boundaries[$i-1] + $gachaweights[$i-1];
    }
    array_shift($boundaries);
    $draw = random_int(1,$boundaries[count($boundaries)-1]);

    for($j = 0; $j < count($boundaries); $j++){
		if($draw <= $boundaries[$j]){
            if($j == 0){
				$result_rarity = "SR";
		    }else if($j == 1){
			    $result_rarity = "R";
		    }else{
				$result_rarity = "N";
		    }
            break;
		}
    }
    return $result_rarity;
}