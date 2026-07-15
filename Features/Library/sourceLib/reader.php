<?php
$source = $_GET['source'];
$file = $_GET['file'];

$path = "../../../bookLibrary/" . $source . "/" . $file;
$json = json_decode(file_get_contents($path), true);
?>

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title><?php echo $json['title']; ?></title>

<link rel="stylesheet" href="reader.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;500&family=Noto+Serif&display=swap" rel="stylesheet">
</head>

<body>

<!-- HEADER -->
<div class="header">
    <button onclick="toggleSidebar()">📚 Chapters</button>
    <div class="title"><?php echo $json['title']; ?></div>
</div>

<!-- PAGE INDICATOR -->
<div class="page-indicator" id="pageInfo">1 / 1</div>
<div id="progressContainer"><div id="progressBar"></div></div>

<!-- SIDEBAR -->
<div class="sidebar" id="sidebar"></div>

<!-- BOOKMARK PANEL -->
<div class="bookmark-panel" id="bookmarkPanel"></div>

<!-- READER -->
<div class="reader">
    <div class="page" id="page">
        <div id="content"></div>

        <!-- CURL CORNER -->
        <div class="page-corner" id="corner"></div>
    </div>
</div>

<!-- CONTROLS -->
<div class="controls">
    <button onclick="prevPage()">⬅</button>
    <button onclick="toggleDark()">🌙</button>
    <button onclick="activateBookmark()">🔖</button>
    <button onclick="toggleBookmarks()">📌</button>
    <button onclick="searchText()">🔍</button>
    <button onclick="nextPage()">➡</button>
</div>

<audio id="flipSound" src="https://cdn.pixabay.com/download/audio/2022/03/15/audio_115b9b64b1.mp3"></audio>

<script>
const book = <?php echo json_encode($json); ?>;
</script>

<script src="reader.js"></script>

</body>
</html>