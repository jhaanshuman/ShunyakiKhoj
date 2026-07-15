<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

$source = $_GET['source'] ?? '';

if(!$source){
    die("No source provided");
}

switch($source){

    case 'wikisource':
        $url = "https://sa.wikisource.org/";
        break;

    case 'csl':
        $url = "https://www.sanskrit-lexicon.uni-koeln.de/";
        break;
        
    case 'gretil':
        $url = "https://gretil.sub.uni-goettingen.de/gretil.html#Sanskrit";
        break;

    case 'archive':
        $url = "https://archive.org/details/texts";
        break;

    case 'sarit':
        $url = "https://github.com/sarit/SARIT-corpus";
        break;

    case 'sacred':
        $url = "https://www.sacred-texts.com/hin/";
        break;

    case 'muktabodha':
        $url = "https://muktabodha.org/";
        break;

    case 'dli':
        $url = "https://dli.gov.in/";
        break;

    default:
        die("Invalid source");
}

$html = @file_get_contents($url);

if($html === false){
    die("Failed to fetch content from source");
}

echo "<h2>Source: $source</h2>";
echo "<iframe src='$url' width='100%' height='800px'></iframe>";
?>