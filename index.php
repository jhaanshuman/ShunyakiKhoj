<?php include('server.php') ?>
<!DOCTYPE html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
    <meta charset="utf-8";">
    <meta http-equiv="x-ua-compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1,user-scalable=0">
    <meta name="description" content="">
    <meta name="author" content="">
    <link href="./Editstyle.css" rel="stylesheet">
    <meta name="keywords" content="">
    <meta name="description" content="">
    <link href=" " rel="stylesheet ">
    
        <script type="text/javascript" src="./CPGRAMS-Home_files/jquery.js"></script>
        <script type="text/javascript" src="./CPGRAMS-Home_files/chatbot.js"></script>
        <!--<script type="text/javascript" src="./CPGRAMS-Home_files/bot_work.js"></script>-->
        <script type="text/javascript" src="./CPGRAMS-Home_files/grieva_database.js"></script>
	    <link rel="stylesheet" type="text/css" href="styleNew.css">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        
    <title>Registration system</title>
</head>
<body> 
<div class="wrapper">
            
<div class="fixed-top">
    <div class="navbar">
        <div class="top">
                <div class="top-nv">
                    <div class="contact-info" onclick="ClearPage()">
                             <script type="text/javascript">
     	                    function ClearPage(){
                            var LogForm = document.getElementById("pageLogContent"); 
                                LogForm.style.display = "none";
                            var RegForm = document.getElementById("pageRegContent"); 
                                RegForm.style.display = "none";
                            var Admin = document.getElementById("pageAdminContent");
                                Admin.style.display = "none"; 
                        	}</script>
                    <span onclick="window.open('https://web.whatsapp.com/send?phone=919934714605', 'w2s_wa_chat')"><i class="icon-whatsapp" aria-hidden="true"></i> +91 9934714605</span> <span><i class="icon-s-mail" aria-hidden="true"></i>Contact Us</span>
                    </div>
                    <div class="user-buttons">
                        <div class="buttonLogin" onclick="ShowLoginForm()">
                        <script type="text/javascript">
     	                    function ShowLoginForm(){
                            var LogForm = document.getElementById("pageLogContent"); 
                                LogForm.style.display = "block";
                            var RegForm = document.getElementById("pageRegContent"); 
                                RegForm.style.display = "none";
                            var Admin = document.getElementById("pageAdminContent");
                                Admin.style.display = "none"; 
                        	}</script>Login</div>
                        <div class="buttonRegister" onclick="ShowRegisterForm()">
                        <script type="text/javascript">
     	                    function ShowRegisterForm() {
                            var RegForm = document.getElementById("pageRegContent"); 
                                RegForm.style.display = "block";
                            var LogForm = document.getElementById("pageLogContent"); 
                                LogForm.style.display = "none";
                            var Admin = document.getElementById("pageAdminContent");
                                Admin.style.display = "none"; 
                        	}</script>
                        Register</div>
                        <div class="buttonLogout">
                        <a href="./logout.php" class="logOut">Log Out</a></div>
                    </div>
            </div>
        </div>
       <!--<div class="nav-top-links">
       		<ul class="navigation top-nv nav-hidden">
                    <li id="free"><a href=""></a></li>
                    <li id="bsness"><a href=""></a></li>
                    <li id="pric"><a href=""></a></li>
                </ul>
        </div>-->
    </div>
</div>

            
<div class="sidebar">
<div id="logo"><img class="logo" src="./CPGRAMS-Home_files/grieva.jpg" alt="home"></div>
    <div class="sidebar-nav">
        <div class="user-profile">
    	 <span>Hi,<strong><?php echo $_SESSION['username'] ?></strong></span><hr>
    	 <span> Consumer ID : <?php echo $id  ?> </span><br>
    	 <span> Username : <?php echo $username ?> </span><br>
    	 <span> Email : <?php echo $email ?> </span><br>
    	 <span> Phone No. : <?php echo $Phone ?> </span><br>
    	 <span> Password : <?php echo $password ?> </span><br>
         <span> Last Active : <?php echo $Last_Active ?> </span>
        </div>
        <div class="sidebar-footer">
            <div class="copy-block">
                <ul>
                    <li><a href="" target="_blank"></a><a href="" target="_blank"></a> <a href="" target="_blank"></a>
                        <a href="Location" target="_blank">Locator</a>
                        <a href="" target="_blank"></a> <a href="" target="_blank">Contact Us</a> 
                    </li>
                    <li class="privacy-policy"><a href="" target="_blank"></a> <a href="" target="_blank"></a></li>
                    <li> <p>© 2019 Copyright</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>
            <div id="rightPanel">
            <div class="activate_grieva"><img id="activate_grieva" src="./CPGRAMS-Home_files/grieva.jpg"></div>
                       <?php include('chatbot.php')?>
            </div></div>
<div id="btnContent">
<div id="pageRegContent">
                <div id="content">
                <form method="post" action="index.php">	<?php include('errors.php'); ?>
                    <h2 class="visible-xs">Register</h2>
                    <div class="f-row">
                        <!--<label class="">Your name</label>-->
                        <input type="text" class="ip-control" id="name" onkeypress="" maxlength="20" name="username" value="<?php echo $username; ?>" placeholder="Enter Name">
                       
                    </div>
                    <div class="f-row">
                        <div class="ip-group user-contact"> 
                            <span class="addon">+91</span> 
                            <input inputmode="number" class="input-field-md" id="mobileNo" autocomplete="off" name="phoneNo" placeholder="Mobile number" maxlength="10" value="" >
                             
                        </div>
                    </div>
                    <div class="f-row">
                        <!--<label class="">Email address</label>-->
                        <input type="email" class="ip-control" onkeypress=";" maxlength="50" id="emailId" name="email" value="<?php echo $email; ?>" placeholder="Email Address">
                    </div>
                    <div class="f-row">
                        <!--<label class="">Password</label>-->
                        <input class="ip-control" maxlength="255"  type="password" name="password_1" value="" placeholder="Password">
                    </div>
                    <div class="f-row">
                        <!--<label class="">Confirm password</label>-->
                        <input type="password" class="ip-control" maxlength="255" id="emailId" name="password_2" value="" placeholder="Confirm Password">
                    </div>
                     
                    <!--<div class="f-row">
                        <div id="genAlert" class="radio-grp">
                            <div class="radio-block">
                                <label class="radio-inline">
                                    <input type="radio" class="optradio" id="genderM" name="gender" value="male">
                                        Male </label>
                                    <label class="radio-inline">
                                        <input type="radio" class="optradio" id="genderF" name="gender" value="female">
                                        Female </label>
                                </div>
                            </div>
                        </div>-->
                        <!--<div class="f-row">
                            <label class="label-small">Date of birth</label>
                            <input inputmode="number" type="text" class="ip-control" id="dob" name="dob" value="" placeholder="Date of Birth">
                    </div>-->
                    <div class="f-row">
                        <label class="label-small">Select City</label>
                        <div class="reg-sel">
				<?php include('city_name.php')?>
                        </div>
                    </div>
                    <!--<div class="f-row">
                        <label class="label-small">Letters are not case sensitive</label>
                        <input type="text" class="ip-control" name="captcha" id="captcha" placeholder="Enter the code shown below" onkeypress="" maxlength="6">
                    </div>
                    <div class="f-row">
                        <div class="captcha-block">
                            <a class="cp-img"><img id="captureImage" src="./Login Reg_files/captcha" alt="Refresh"></a>
                            <button type="button" class="btn-outline" onclick="reloadCaptcha()">
                                <i class="fa icon-refresh"></i>
                            </button>
                        </div>
                    </div>-->
                    	   <script type="text/javascript">
     	                    function ShowRegister(keyCheck) {
                            var Submit = document.getElementById("submit"); 
                                Submit.style.display = keyCheck.checked ? "block" : "none";
                        	}</script>
                    <div class="f-row agree-terms" id="terms">
                        <input type="checkbox"  for="keyCheck" name="terms" class="check-box" id="terms" onclick="ShowRegister(this)">I agree to the Register <a href="" target="_blank">privacy policy</a> <a href="" target="_blank">Terms Conditions</a>                                        
                    </div>
                    <div class="f-row align-right" id="submit">
                        <button type="submit" id="sendButton" class="button button-default" data-toggle="dropdown" name="reg_user">Register Now</button>
                    </div>
  </form></div></div>
            <div id="pageLogContent"><?php include('login.php')?></div>
            </div>

 </body></html>