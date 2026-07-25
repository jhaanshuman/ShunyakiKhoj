<?php

$url = $_GET["url"] ?? "";

/* Basic safety */
if($url == ""){
 die("❌ No book URL provided");
}

/* Optional: decode URL */
$url = urldecode($url);

?>

<!DOCTYPE html>
<html>

<head>
<meta name="google-adsense-account" content="ca-pub-1342189574858672">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1342189574858672" crossorigin="anonymous"></script>

<title>Reader</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

body{
margin:0;
font-family:Arial;
background:#020617;
color:white;
}

/* HEADER */

.header{
display:flex;
justify-content:space-between;
align-items:center;
padding:10px 20px;
background:#020617;
border-bottom:1px solid #1e293b;
position:fixed;
top:0;
width:100%;
z-index:10;
}

.header h2{
margin:0;
font-size:16px;
}

/* BUTTONS */

.controls{
display:flex;
gap:10px;
}

.btn{
background:#1e293b;
color:white;
border:none;
padding:8px 12px;
border-radius:6px;
cursor:pointer;
transition:0.3s;
}

.btn:hover{
background:#334155;
}

/* READER */

.viewer{
position:absolute;
top:60px;
left:0;
width:100%;
height:calc(100vh - 60px);
}

iframe{
width:100%;
height:100%;
border:none;
background:white;
}

/* LOADER */

.loader{
position:absolute;
top:50%;
left:50%;
transform:translate(-50%,-50%);
font-size:14px;
opacity:0.6;
}

</style>

</head>

<body>

<div class="header">

<h2>📖 Reader</h2>

<div class="controls">

<button class="btn" onclick="goBack()">⬅ Back</button>

<button class="btn" onclick="openNew()">🔗 Open</button>

<button class="btn" onclick="reloadFrame()">🔄 Reload</button>

</div>

</div>

<div class="viewer">

<div class="loader" id="loader">Loading book...</div>

<iframe id="frame" src="<?php echo htmlspecialchars($url); ?>"></iframe>

</div>

<script>

const frame = document.getElementById("frame")
const loader = document.getElementById("loader")

frame.onload = () => {
 loader.style.display = "none"
}

/* controls */

function goBack(){
 history.back()
}

function openNew(){
 window.open("<?php echo htmlspecialchars($url); ?>","_blank")
}

function reloadFrame(){
 frame.src = frame.src
 loader.style.display = "block"
}

</script>

</body>
</html>