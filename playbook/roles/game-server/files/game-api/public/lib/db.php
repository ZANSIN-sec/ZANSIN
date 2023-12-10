<?php
require_once('./config.php');

function connect_user_list_db()
{
    $db = $_ENV['database'];
    $host = $db['host'];
    $database = $db['dbname'];
    $user_name = $db['user'];
    $password = $db['password'];

    try {
        $pdo = new PDO("mysql:host=$host;dbname=$database;charset=utf8;", $user_name, $password,
            array(PDO::ATTR_EMULATE_PREPARES => false));
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    } catch (PDOException $e) {
        echo json_encode(array(
            "result" => "ng",
            "msg" => $e->getMessage()
        ));
        exit();
    }
    return $pdo;
}