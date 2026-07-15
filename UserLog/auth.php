<?php
header("Content-Type: application/json");
session_start();
require "db.php";
$action = $_POST['action'] ?? $_GET['action'] ?? '';

/* SESSION CHECK */
if($action == "session"){
    if(isset($_SESSION['user_id'])){
        echo json_encode([
            "loggedIn" => true,
            "username" => $_SESSION['username']
        ]);
    } else {
        echo json_encode([
            "loggedIn" => false
        ]);
    }
    exit;
}

/* SIGNUP */
if($action=="signup"){

$username=db_escape($_POST['username']);
$email=db_escape($_POST['email']);
$password=$_POST['password'];
$gen=db_escape($_POST['Gen']);
$dob=db_escape($_POST['DOB']);
$lang=db_escape($_POST['DefLang']);

$hash=password_hash($password,PASSWORD_DEFAULT);

$sql="INSERT INTO users
(username,email,password_hash,Gen,DOB,DefLang,login_mode)
VALUES
('$username','$email','$hash','$gen','$dob','$lang','email')";

if(db_query($sql)){

echo json_encode(["success"=>true]);

}else{

echo json_encode(["success"=>false,"error"=>"User exists"]);

}

exit;

}

/* LOGIN */

if($action=="login"){

$email=db_escape($_POST['email']);
$password=$_POST['password'];

$q=db_query("SELECT * FROM users WHERE email='$email'");

$row=db_fetch($q);

if(!$row){

echo json_encode([
"success"=>false,
"error"=>"User not found"
]);

exit;

}

if(password_verify($password,$row['password_hash'])){

$_SESSION['user_id']=$row['id'];
$_SESSION['username']=$row['username'];

if ($db_type === 'sqlite') {
    db_query("UPDATE users SET LastLog=datetime('now') WHERE id=".$row['id']);
} else {
    db_query("UPDATE users SET LastLog=NOW() WHERE id=".$row['id']);
}

echo json_encode([
"success"=>true,
"username"=>$row['username']
]);

}else{

echo json_encode([
"success"=>false,
"error"=>"Wrong password"
]);

}

exit;

}

/* LOGOUT */

if($action=="logout"){

session_destroy();

echo json_encode(["success"=>true]);

exit;

}

/* DELETE ACCOUNT */

if($action=="deleteAccount"){

$id=$_SESSION['user_id'];

db_query("DELETE FROM users WHERE id=$id");

session_destroy();

echo json_encode(["success"=>true]);

exit;

}

/* DEFAULT */

echo json_encode([
"success"=>false,
"error"=>"Invalid request"
]);

?>