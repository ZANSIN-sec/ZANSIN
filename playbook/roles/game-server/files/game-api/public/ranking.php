<?php
require_once('./lib/db.php');
require_once('./lib/user.php');

$pdo = connect_user_list_db();

// Mapping Query to Column
$sort_num = $_GET['sort'] ?? "0";
if (strcmp("1", $sort_num) == 0) {
    $sort_mode = 'level';
} elseif (strcmp("2", $sort_num) == 0) {
    $sort_mode = 'stamina';
} elseif (strcmp("3", $sort_num) == 0) {
    $sort_mode = 'gold';
} elseif (strcmp("4", $sort_num) == 0) {
    $sort_mode = 'exp';
} elseif (strcmp("5", $sort_num) == 0) {
    $sort_mode = 'weapon_id';
} elseif (strcmp("6", $sort_num) == 0) {
    $sort_mode = 'armor_id';
} else {
    $sort_mode = 'level';
}
$ranking_count = 1;
$stmt = $pdo->prepare("SELECT * FROM player ORDER BY " . $sort_mode . " DESC Limit 10");

$request_content_type = $_SERVER["CONTENT_TYPE"] ?? "text/html";
if (strcmp("application/json", $request_content_type) == 0) {
    $stmt->execute();
    $userData = array();
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        $userData[] = array(
            'user_name' => $row['user_name'],
            'nick_name' => $row['nick_name'],
            'level' => $row['level'],
            'stamina' => $row['stamina'],
            'gold' => $row['gold'],
            'exp' => $row['exp'],
            'weapon_id' => $row['weapon_id'],
            'armor_id' => $row['armor_id'],
        );
    }
    header('Content-type: application/json');
    echo json_encode($userData);
    exit();
}

?>

<!doctype html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="./css/bootstrap.min.css">

    <title>Ranking！</title>
</head>
<body>
<h1>Ranking！</h1>
<div class="btn-group" role="group" style="margin-top: 10px; margin-bottom: 10px; margin-left:15px">
    <a href="ranking.php?sort=1" class="btn <?php echo ("level" == $sort_mode) ? "btn-secondary" : ""; ?>">Level</a>
    <a href="ranking.php?sort=2" class="btn <?php echo ("stamina" == $sort_mode) ? "btn-secondary" : ""; ?>">Stamina</a>
    <a href="ranking.php?sort=3" class="btn <?php echo ("gold" == $sort_mode) ? "btn-secondary" : ""; ?>">Gold</a>
    <a href="ranking.php?sort=4" class="btn <?php echo ("exp" == $sort_mode) ? "btn-secondary" : ""; ?>">Exp.</a>
    <a href="ranking.php?sort=5" class="btn <?php echo ("weapon_id" == $sort_mode) ? "btn-secondary" : ""; ?>">Weapon ID</a>
    <a href="ranking.php?sort=6" class="btn <?php echo ("armor_id" == $sort_mode) ? "btn-secondary" : ""; ?>">Armor ID</a>

</div>
<table class="table">
    <thead class="thead-light">
    <tr>
        <th>Nickname</th>
        <th>Level</th>
        <th>Stamina</th>
        <th>Gold</th>
        <th>Exp.</th>
        <th>Weapon ID</th>
        <th>Armor ID</th>
    </tr>
    </thead>
    <?php
    if ($stmt->execute()) {
        while ($row = $stmt->fetch()) {
            echo "<tr>\n";
            echo "<td>";
            if ($ranking_count == 1) {
                echo "<img src=\"/images/ranking/ranking01.png\" width=\"30%\">";
                echo "&nbsp&nbsp";

            } elseif ($ranking_count == 2) {
                echo "<img src=\"/images/ranking/ranking02.png\" width=\"20%\">";
                echo "&nbsp&nbsp";

            } elseif ($ranking_count == 3) {
                echo "<img src=\"/images/ranking/ranking03.png\" width=\"15%\">";
                echo "&nbsp&nbsp";

            } else {
                echo "<span style='font-weight: bold'>No." . $ranking_count . "</span>";
            }
            $ranking_count = $ranking_count + 1;
            echo htmlspecialchars($row['nick_name'], ENT_QUOTES, "utf-8") . "</td>";
            table_list($row);
        }
    }
    ?>
</table>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="./js/jquery-3.5.1.slim.min.js"></script>
<script src="./js/popper.min.js"></script>
<script src="./js/bootstrap.min.js"></script>
</body>
</html>
