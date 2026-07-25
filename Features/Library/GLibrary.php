<!DOCTYPE html>
<html>
<head>
<meta name="google-adsense-account" content="ca-pub-1342189574858672">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1342189574858672" crossorigin="anonymous"></script>
<title>Global Library</title>
<style>
body{
    font-family: Arial;
    background: linear-gradient(135deg,#5D3FD3,#088F8F);
    color:white;
    text-align:center;
}
.container{
    display:flex;
    justify-content:center;
    gap:30px;
    margin-top:100px;
}
.card{
    padding:30px;
    background:rgba(255,255,255,0.1);
    border-radius:15px;
    cursor:pointer;
    transition:0.3s;
}
.card:hover{
    transform:scale(1.1);
}
</style>
</head>

<body>

<h1>📚 Sanskrit Global Library</h1>

<div class="container">
    <div class="card" onclick="openSource('sarit')">SARIT</div>
    <div class="card">GRETIL</div>
    <div class="card">Archive</div>
    <div class="card">Muktabodha</div>
</div>

<script>
function openSource(source){
    window.location.href = "sourceLib/index.php?source=" + source;
}
</script>

</body>
</html>