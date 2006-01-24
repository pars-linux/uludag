<?php
include("globals.php");

    if(!$_GET['file']){$_GET['file'] = 1;}

    $file = get_filepaths($_GET["id"]);
    if($_GET['file'] == 2 && $file[0]['path2'] != ""){$download = $file[0]['path2'];}
    elseif($_GET['file'] == 1 && $file[0]['path'] != ""){$download = $file[0]['path'];}
    elseif($_GET['file'] == 1 && $file[0]['path'] == ""){$hata = TRUE;}
    elseif($_GET['file'] == 2 && $file[0]['path2'] == ""){$hata = TRUE;}

    if(!$hata){
    if(count_download($download)){Header("location: ".$config['core']['url']."files/".$download);}
    else{
        $message["title"] = ERROR;
        $message["message"] = FILE_NOT_FOUND;
        set_smarty_vars("message",$message);
        $smarty->display("message.html");
    }
    }
    elseif($hata){
        $message["title"] = ERROR;
        $message["message"] = FILE_NOT_FOUND;
        set_smarty_vars("message",$message);
        $smarty->display("message.html");
    }
    die();
?>