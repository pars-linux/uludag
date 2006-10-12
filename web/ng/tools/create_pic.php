<?php

    #image: create,store tool for Pardus's Web.
    #needs pic.php in the same directory.

    function GetServerAddr() {
        return "http://".$_SERVER[SERVER_ADDR].dirname($_SERVER[PHP_SELF])."/";
    }

    include_once ("../config.php");

    if ($CF["Tools"]["Pic"]["Enable"]) {
        $image_path = $CF["Tools"]["Pic"]["Dir"];
        include_once ("../Modules/search.php");
        $real_word = $_GET["q"];
        $tools = new Sud();
        $file_name = $tools->turnToEn($tools->GetLower($real_word)).".gif";
        $file_name = eregi_replace(" ","_",$file_name);
        $real_word = urlencode($real_word);
        $root = GetServerAddr();

        if ($_GET["q"]<>"") {
            if (!file_exists($image_path.$file_name)) {
                if (copy("$root/pic.php?q=$real_word",$image_path.$file_name))
                    echo "$file_name saved into $image_path";
                else
                    echo "An error occured.";
            }
            else
                echo "Image ($file_name) already exists in $image_path .Exiting..";
                echo "<br /><a href='?'>Create New</a>";
        } else {
        echo '
            Write some words, it will store in image directory as .gif.
            <form action="" method="GET">
                <input type="text" name="q">
                <input type="submit" name="create" value="create">
            </form>';
        }
    }

?>
