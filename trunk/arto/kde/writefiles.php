<?php
include("../globals.php");
include("kde.functions.php");

$files = array();

//Wallpapers
$files[] = array("wallpaper.xml", "release", "1", "kde/wallpaper/");
$files[] = array("wallpaper-downloads.xml", "counter", "1", "kde/wallpaper/");
$files[] = array("wallpaper-score.xml", "point", "1", "kde/wallpaper/");

//Amarok Themes
$files[] = array("amarokthemes.xml", "release", "13", "kde/amarokthemes/");
$files[] = array("amarokthemes-downloads.xml", "counter", "13", "kde/amarokthemes/");
$files[] = array("amarokthemes-score.xml", "point", "13", "kde/amarokthemes/");

//SuperKaramba Themes
$files[] = array("karamba.xml", "release", "9", "kde/karamba/");
$files[] = array("karamba-downloads.xml", "counter", "9", "kde/karamba/");
$files[] = array("karamba-score.xml", "point", "9", "kde/karamba/");

//$files[] = array("filename.xml", "orderby", "category_id", "kde/destdir/");

generate_files($files);
?>