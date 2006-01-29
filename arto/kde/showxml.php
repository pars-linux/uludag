<?php
Header("Content-type: text/xml; charset: utf-8");

if(!$orderby){$orderby = "release";}

echo "<knewstuff>\n";

$category = get_type($cat);
if($category[0]['parent_id'] == 0){$cat = $category[0]['id'];}

$content = get_something("cat",$cat,"",$orderby,"25");

for($i = 0; $i < count($content); $i++){
    $author = get_user_something($content[$i]['user'], "name");
    $email = get_user_something($content[$i]['user'], "email");
    if($content[$i]['path'] != "" AND $content[$i]['path2'] == ""){$preview = $content[$i]['path'];}
    elseif($content[$i]['path'] != "" AND $content[$i]['path'] != ""){$preview = $content[$i]['path2'];}
    if($content[$i]['path'] != "" AND $content[$i]['path2'] == ""){$file = $content[$i]['path'];}
    elseif($content[$i]['path'] != "" AND $content[$i]['path'] != ""){$file = $content[$i]['path2'];}
    if(get_file_type($preview) == "package"){$preview = "no-preview.png";}
    if($content[$i]['point'] > 1){$content[$i]['rating'] = round($content[$i]['point']/$content[$i]['rated']);}
    else{$content[$i]['rating'] = 0;}

    echo "<stuff>\n";
    echo "<name>{$content[$i]['name']}</name>\n";
    echo "<type>{$content[$i]['type']}</type>\n";
    echo "<author>{$author[0]['name']}</author>\n";
    echo "<email>{$email[0]['email']}</email>\n";
    echo "<licence>{$content[$i]['lname']}</licence>\n";
    echo "<summary lang=\"en\">{$content[$i]['description']}</summary>\n";
    echo "<version></version>\n";
    echo "<release></release>\n";
    echo "<releasedate>{$content[$i]['release']['year']}-{$content[$i]['release']['month']}-{$content[$i]['release']['day']}</releasedate>\n";
    echo "<preview lang=\"en\">{$config['core']['url']}files/thumbs/{$preview}</preview>\n";
    echo "<payload lang=\"en\">{$config['core']['url']}files/{$file}</payload>\n";
    echo "<rating>{$content[$i]['rating']}</rating>\n";
    echo "<downloads>{$content[$i]['counter']}</downloads>\n";
    echo "<more>{$config['core']['url']}node/{$content[$i]['id']}</more>\n";
    echo "</stuff>\n";
}
echo "</knewstuff>";
?>