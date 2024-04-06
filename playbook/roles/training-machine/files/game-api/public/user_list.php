<?php
require_once('./lib/db.php');
require_once('./lib/user.php');
if(array_key_exists("HTTP_ORIGIN", $_SERVER)){
    header("Access-Control-Allow-Origin: " . $_SERVER['HTTP_ORIGIN'] . "");
    header('Access-Control-Allow-Credentials: true');
    header('Access-Control-Allow-Headers: X-Requested-With');
}

//TODO ACL
//$user_id = check_login($redis, $session_id);

$pdo = connect_user_list_db();

?>

<!doctype html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="./css/bootstrap.min.css">

    <title>User List</title>
</head>
<body>
<h1>User List</h1>
<?php
if($_SERVER["REQUEST_METHOD"] === "POST"){
    $stmt = $pdo->prepare('delete from player WHERE id = :user_id');
    $stmt->bindValue(':user_id', $_POST["user_id"], PDO::PARAM_STR);
    $stmt->execute();
    echo "<div class=\"alert alert-danger\" role=\"alert\">
Deleted
</div>";
}
?>

<table class="table">
    <thead class="thead-light">
    <tr>
        <th>ID</th>
        <th>Username</th>
        <th>Nickname</th>
        <th>Level</th>
        <th>Stamina</th>
        <th>Gold</th>
        <th>Exp.</th>
        <th>WeaponID</th>
        <th>ArmorID</th>
        <th>BAN</th>
    </tr>
    </thead>
    <?php
    $stmt = $pdo->prepare("SELECT * FROM player");
    if ($stmt->execute()) {
        while ($row = $stmt->fetch()) {
            echo "<tr>\n";
            echo "<td>" . htmlspecialchars($row['id'], ENT_QUOTES, "utf-8") . "</td>";
            echo "<td>" . htmlspecialchars($row['user_name'], ENT_QUOTES, "utf-8") . "</td>";
            echo "<td>" . htmlspecialchars($row['nick_name'], ENT_QUOTES, "utf-8") . "</td>";
            table_list($row);
            echo "
<td>
<form method='post' onsubmit='return form_confirm();'>
<input type='hidden' name='user_id' value='" . htmlspecialchars($row['id'], ENT_QUOTES, "utf-8") . "'>
<input type='submit' class='ban-button btn btn-danger' value='BAN!!'>
</form>
</td>";
        }
    }
    ?>
</table>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="./js/jquery-3.5.1.slim.min.js"></script>
<script src="./js/popper.min.js"></script>
<script src="./js/bootstrap.min.js"></script>
<script>
    function form_confirm() {
        if (window.confirm('OK?')) {
            return true;
        } else {
            return false;

        }
    }
</script>
</body>
</html>