<?php include('server.php') ?>
<!DOCTYPE html>
<html>
<head>
  <title>Registration system PHP and MySQL</title>
  <link rel="stylesheet" type="text/css" href="styleNew.css">
</head>
<body>

  <div id="content">
  <div id="user">
   <div class="user_header">Login</div>
	 <div id="form_Box">
    <form method="post" action="login.php">
  	<?php include('errors.php'); ?>
  	<div class="input-group">
  		<label>Username</label>
  		<input type="text" name="username" >
  	</div>
  	<div class="input-group">
  		<label>Password</label>
  		<input type="password" name="password">
  	</div>
  	<div class="input-group">
  		<button type="submit" class="btn" name="login_user">Login</button>
  	</div>
  	<div class="form-register">
  		Not yet a member? <a href="index.php">Sign up</a>
  	</div>
  </form></div>
  </div>
  </div>
  	
</body>
</html>