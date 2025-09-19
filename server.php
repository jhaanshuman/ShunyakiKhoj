<?php
session_start();

// initializing variables
$username = "";
$email    = "";
$errors = array(); 

// connect to the database
$db = mysqli_connect('localhost', 'id11710805_askgrieva', 'id11710805', 'id11710805_askgrievauser');

// REGISTER USER
if (isset($_POST['reg_user'])) {
  // receive all input values from the form
  $username = mysqli_real_escape_string($db, $_POST['username']);
  $phoneNo = mysqli_real_escape_string($db, $_POST['phoneNo']);
  $email = mysqli_real_escape_string($db, $_POST['email']);
  $password_1 = mysqli_real_escape_string($db, $_POST['password_1']);
  $password_2 = mysqli_real_escape_string($db, $_POST['password_2']);
  //$time = date("Y-m-d h:i:sa");
  // form validation: ensure that the form is correctly filled ...
  // by adding (array_push()) corresponding error unto $errors array
  if (empty($username)) { array_push($errors, "Username is required"); }
  //if (empty($phoneNo)) { array_push($errors, "Phone No. is required"); }
  if (empty($email)) { array_push($errors, "Email is required"); }
  if (empty($password_1)) { array_push($errors, "Password is required"); }
  if ($password_1 != $password_2) {
	array_push($errors, "The two passwords do not match");
  }

  // first check the database to make sure 
  // a user does not already exist with the same username and/or email
  $user_check_query = "SELECT * FROM Consumer WHERE username='$username' OR email='$email' LIMIT 1";
  $result = mysqli_query($db, $user_check_query);
  $user = mysqli_fetch_assoc($result);
  
  if ($user) { // if user exists
    if ($user['username'] === $username) {
      array_push($errors, "Username already exists");
    }

    if ($user['email'] === $email) {
      array_push($errors, "email already exists");
    }
  }

  // Finally, register user if there are no errors in the form
  if (count($errors) == 0) {
  	$password = md5($password_1);//encrypt the password before saving in the database

  	$query = "INSERT INTO Consumer (username, phoneNo, email, password, Last_Active) 
  			  VALUES('$username','$phoneNo', '$email', '$password', now())";
  	mysqli_query($db, $query);
  	$_SESSION['username'] = $username;
  	$_SESSION['success'] = "You are now logged in";
  	header('location: index.php');
  }
}
// LOGIN USER
if (isset($_POST['login_user'])) {
  $username = mysqli_real_escape_string($db, $_POST['username']);
  $password = mysqli_real_escape_string($db, $_POST['password']);

  if (empty($username)) {array_push($errors, "Username is required");}
  if (empty($password)) {array_push($errors, "Password is required");}
  if (count($errors) == 0) {
  	$password = md5($password);
  	$query = "SELECT * FROM Consumer WHERE username='$username' AND password='$password'";
  	$results = mysqli_query($db, $query);
  	if (mysqli_num_rows($results) == 1) {
  	  //$_SESSION['Last_Active'] = $time
  	  $_SESSION['username'] = $username;
  	  $_SESSION['success'] = "You are now logged in";
  	  header('location: index.php');
  	}else {
  		array_push($errors, "Wrong username/password combination");
  	}
  }
}

// RETRIEVE DATA from SERVER
// Check connection
if ($db->connect_error) {    die("Connection failed: " . $db->connect_error);}
//if (!$conn) {die('Could not connect: ' . mysqli_error($conn));}

$sql = "SELECT id, username, password, PhoneNo, email, Last_Active FROM Consumer";
$result = $db->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        $id = $row["id"];
        $username = $row["username"];
        $password = $row["password"];
        $Phone = $row["PhoneNo"];
        $email = $row["email"];
        $Last_Active = $row["Last_Active"];
        //echo "<br> id: ". $row["id"]. " - Username: ". $row["username"]." Password". $row["password"]." Phone No. ". $row["PhoneNo"]." Email Address ". $row["email"]." Last Seen". $row["Last_Active"]." ". "<br>";
        }} else {    echo "0 results";}
$db->close();
?>