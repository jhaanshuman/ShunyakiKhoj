const API="/UserLog/auth.php";

/* CHECK SESSION */

fetch(API+"?action=session")
.then(res=>res.text())
.then(text=>{

if(!text) return;

let data;

try{
data=JSON.parse(text);
}catch(e){
console.log("Invalid JSON",text);
return;
}

const btn=document.getElementById("profileBtn");

if(data.loggedIn){

btn.innerHTML=`
<div class="profileMenu">
${data.username}

<div class="profileDropdown">
<a href="/features/Settings/Profile/settings.php">Settings</a>
<a onclick="logout()">Logout</a>
</div>

</div>
`;

}else{

btn.onclick=openAuthModal;

}

});


/* OPEN LOGIN MODAL */

function openAuthModal(){

document.getElementById("authModal").style.display="flex";

}


/* LOGIN */

function login(){

let email=document.getElementById("loginEmail").value;
let password=document.getElementById("loginPassword").value;

fetch(API,{
method:"POST",
headers:{
"Content-Type":"application/x-www-form-urlencoded"
},
body:new URLSearchParams({
action:"login",
email:email,
password:password
})
})
.then(r=>r.json())
.then(data=>{

if(data.success){

location.reload();

}else{

alert(data.error);

}

});

}


/* SIGNUP */

function signup(){

let username=document.getElementById("signupUsername").value;
let email=document.getElementById("signupEmail").value;
let password=document.getElementById("signupPassword").value;
let gender=document.getElementById("gender").value;
let dob=document.getElementById("dob").value;
let lang=document.getElementById("lang").value;

fetch(API,{
method:"POST",
headers:{
"Content-Type":"application/x-www-form-urlencoded"
},
body:new URLSearchParams({
action:"signup",
username:username,
email:email,
password:password,
Gen:gender,
DOB:dob,
DefLang:lang
})
})
.then(r=>r.json())
.then(data=>{

if(data.success){

alert("Signup successful");
location.reload();

}else{

alert(data.error);

}

});

}


/* LOGOUT */

function logout(){

fetch(API,{
method:"POST",
headers:{
"Content-Type":"application/x-www-form-urlencoded"
},
body:new URLSearchParams({
action:"logout"
})
})
.then(()=>location.reload());

}

function openAuth(){
document.getElementById("authModal").style.display="flex"
}

function closeAuth(){
document.getElementById("authModal").style.display="none"
}

function showSignup(){
document.getElementById("authTitle").innerText="Sign Up"
}
function openAuth(){
document.getElementById("authModal").style.display="flex"
}

function closeAuth(){
document.getElementById("authModal").style.display="none"
}

function showSignup(){

document.getElementById("authTitle").innerText="Sign Up"

}

function forgotPassword(){
alert("Password recovery coming soon.")
}