<?php
include("globals.php");

if(!$_GET){
    $smarty->display("index.html");
    die();
}

else{
    $searchString = "{$_GET['keywords']} site:liste.uludag.org.tr";
    $google = new googleClient($config['core']['licensekey']);

    if($_GET['start']) $start = $_GET['start'];
    else $start = 0;

    if($google->search($searchString, $start)){$result = $google->results;}
    $result->searchQuery = str_replace(" site:liste.uludag.org.tr", "", $result->searchQuery);
    $result->searchTime = round($result->searchTime, 2);
    for($i = 0; $i < count($result->resultElements); $i++){$result->resultElements[$i]->count = ($result->startIndex+$i);}
    //else $smarty->assign("error", $google->error());

    $smarty->assign("results", $result);
    $smarty->display("search.html");
    //echo "<pre>";
    //print_r($result);
    //echo "<pre>";
    die();
}
?>