<?php
include("globals.php");

if(!$_GET){
    $smarty->display("index.html");
    die();
}
else{
    $result = do_search($_GET['keywords'], $_GET['start'], "uludag.org.tr");
    $result2 = do_search($_GET['keywords'], $_GET['start'], "pardus.org.tr");

    //echo "<pre>";
    //print_r(merge($result, $result2));
    //echo "</pre>";

    $smarty->assign("results", merge($result, $result2));
    $smarty->display("search.html");

    die();
}

function do_search($kw, $start, $domain){
    global $config;

    $searchString = $kw.' site:liste.'.$domain;
    $google = new googleClient($config['core']['licensekey']);

    if($start) $st = $start;
    else $st = 0;

    if($google->search($searchString, $st)){$result = $google->results;}
    $result->searchTime = round($result->searchTime, 2);
    for($i = 0; $i < count($result->resultElements); $i++){$result->resultElements[$i]->count = ($result->startIndex+$i);}

return $result;
}

function merge($obj1, $obj2){
    $return['estimatedTotalResultsCount'] = $obj1->estimatedTotalResultsCount + $obj2->estimatedTotalResultsCount;
    $return['resultElements'] = object2array(array_merge($obj1->resultElements, $obj2->resultElements));
    $return['startIndex'] = $obj1->startIndex + $obj2->startIndex;
    $return['endIndex'] = $obj1->endIndex + $obj2->endIndex;
    $return['searchTime'] = $obj1->searchTime + $obj2->searchTime;
    $return['searchQuery'] = str_replace(" site:liste.uludag.org.tr", "", $obj1->searchQuery);

return $return;
}

function object2array($object){
   $return = NULL;

   if(is_array($object)){
       foreach($object as $key => $value)
           $return[$key] = object2array($value);
   }
   else{
       $var = get_object_vars($object);

       if($var){
           foreach($var as $key => $value)
               $return[$key] = object2array($value);
       }
       else
           return strval($object);
   }

   return $return;
}
?>