<?php

    function generate_files($files){
        for($i = 0; $i < count($files); $i++){
            write_xml($files[$i][0], get_xml($files[$i][1], $files[$i][2]), $files[$i][3]);
        }
    }

    function get_xml($orderby, $cat){
        global $config;

        if(!$orderby){$orderby = "release";}

        $category = get_type($cat);
        if($category[0]['parent_id'] == 0){$cat = $category[0]['id'];}

        $content = get_something("cat",$cat,"",$orderby,"25");

        $xml = "<knewstuff>\n";
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

            $xml .= "<stuff>\n";
            $xml .= "<name>{$content[$i]['name']}</name>\n";
            $xml .= "<type>{$content[$i]['type']}</type>\n";
            $xml .= "<author>{$author[0]['name']}</author>\n";
            $xml .= "<email>{$email[0]['email']}</email>\n";
            $xml .= "<licence>{$content[$i]['lname']}</licence>\n";
            $xml .= "<summary lang=\"en\">{$content[$i]['description']}</summary>\n";
            $xml .= "<version></version>\n";
            $xml .= "<release></release>\n";
            $xml .= "<releasedate>{$content[$i]['release']['year']}-{$content[$i]['release']['month']}-{$content[$i]['release']['day']}</releasedate>\n";
            $xml .= "<preview lang=\"en\">{$config['core']['url']}files/thumbs/{$preview}</preview>\n";
            $xml .= "<payload lang=\"en\">{$config['core']['url']}files/{$file}</payload>\n";
            $xml .= "<rating>{$content[$i]['rating']}</rating>\n";
            $xml .= "<downloads>{$content[$i]['counter']}</downloads>\n";
            $xml .= "<more>{$config['core']['url']}node/{$content[$i]['id']}</more>\n";
            $xml .= "</stuff>\n";
        }
        $xml .= "</knewstuff>";
    return $xml;
    }

    function write_xml($filename, $xml, $destdir = "kde/", $tempdir = "/kde/"){
        global $config;

        $tmpdir = $config['core']['path'].$config['core']['temp'].$tempdir;
        $tmpfile = $tmpdir.$filename;
        $destdir = $config['core']['path'].$destdir;

        if(file_exists($tmpfile)){unlink($tmpfile);}

        if(!file_exists($tmpfile)){
            if(!file_exists($tmpdir)){mkdir($tmpdir);}
            touch($tmpfile);
        }

        $file = fopen($tmpfile, 'a+');
        ftruncate($file, 0);
        fwrite($file, $xml);
        fclose($file);

        if(file_exists($tmpfile)){
            if(file_exists($destdir.$filename)){unlink($destdir.$filename);}
            if(copy($tmpfile, $destdir.$filename)){chmod($tmpfile, "0666"); unlink($tmpfile); chmod($destdir.$filename, "0777");}
        }
    }
?>