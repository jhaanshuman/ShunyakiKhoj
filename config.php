<?php

$servername = "localhost";
$username = "id11519117_jhaanshuman";
$password = "Anshu@05011995";
$database = "id11519117_trial_db";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully : Welcome Anshuman ";
?>