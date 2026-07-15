<?php

$main=json_decode(file_get_contents("config/sources.json"),true);

$sources=[];

foreach($main["sources"] as $ref){

$file="config/".$ref["file"];

$data=json_decode(file_get_contents($file),true);

$sources[]=$data;

}

?>

<!DOCTYPE html>
<html>

<head>
<link rel="stylesheet" href="css/style.css">
</head>

<body>
<div class="tile-container">
<?php
foreach($sources as $src){
echo "
<a class='tile' href='library.php?source=".$src["id"]."'>
<img src='".$src["icon"]."'>
<h2>".$src["name"]."</h2>
<p>".$src["info"]."</p>
</a>
";
}
?>
</div>

</body>
</html>