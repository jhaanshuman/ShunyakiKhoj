<?php
header("Content-Type: application/json;charset=UTF-8"); $q = $_GET['q'] ?? '';
if(strlen($q) < 1){ echo json_encode([]);exit;}
$host = "sql106.infinityfree.com";$user = "if0_41366642";$password = "ySp2t8afpDyv";$db = "if0_41366642_sanskrit_dict_mw";
$conn = new mysqli($host,$user,$password,$db);
if($conn->connect_error){ echo json_encode([]);exit;}
$q = $conn->real_escape_string($q);
$sql = "SELECT word, meaning FROM dictionary WHERE word LIKE '$q%' LIMIT 15";
$result = $conn->query($sql);$data=[]; while($row=$result->fetch_assoc()){ $data[]=$row; }
echo json_encode($data);$conn->close();

?>