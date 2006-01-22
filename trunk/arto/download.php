<?php
include("globals.php");

            $file=rtag($_GET["file"]);
            if (count_download($file)) header ("location: ".$config['core']['url']."files/".$_GET["file"]);
            else {
                $message["title"] = ERROR;
                $message["message"] = FILE_NOT_FOUND;
		set_smarty_vars("message",$message);
		$smarty->display("message.html");
            }
            die();
?>