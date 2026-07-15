<?php

session_start();

require "../../../UserLog/db.php";

if(!isset($_SESSION['user_id'])){
die("Login required");
}

$id=$_SESSION['user_id'];

$q=mysqli_query($conn,"SELECT * FROM users WHERE id=$id");
$user=mysqli_fetch_assoc($q);

?>

<link rel="stylesheet" href="style.css">

<h2>Profile Settings</h2>

<table>

<tr>
<td>Username</td>
<td><?php echo $user['username']; ?></td>
</tr>

<tr>
<td>Email</td>
<td><?php echo $user['email']; ?></td>
</tr>

<tr>
<td>Gender</td>
<td><?php echo $user['Gen']; ?></td>
</tr>

<tr>
<td>Date of Birth</td>
<td><?php echo $user['DOB']; ?></td>
</tr>

<tr>
<td>Default Language</td>
<td><?php echo $user['DefLang']; ?></td>
</tr>

<tr>
<td>Last Login</td>
<td><?php echo $user['LastLog']; ?></td>
</tr>

<tr>
<td>Password</td>
<td>
<input type="password" id="pwd" value="********">
<button onclick="togglePwd()">👁</button>
</td>
</tr>

</table>

<button onclick="deleteAccount()">Delete Account</button>

<script>

function togglePwd(){

let p=document.getElementById("pwd");

p.type = p.type==="password" ? "text" : "password";

}

function deleteAccount(){

if(!confirm("Delete account permanently?")) return;

fetch("/UserLog/auth.php",{
method:"POST",
headers:{
"Content-Type":"application/x-www-form-urlencoded"
},
body:new URLSearchParams({
action:"deleteAccount"
})
})
.then(()=>location="/");

}

</script>