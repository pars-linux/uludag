<?php
include("globals.php");

            $file = get_filepaths($_GET["id"]);
            if($file[0]['path2']){$download = $file[0]['path2'];}
            elseif($file[0]['path2'] == "" && isset($file[0]['path'])){$download = $file[0]['path'];}
            if (count_download($download)) header ("location: ".$config['core']['url']."files/".$download);
            else {
                $message["title"] = ERROR;
                $message["message"] = FILE_NOT_FOUND;
		set_smarty_vars("message",$message);
		$smarty->display("message.html");
            }
            die();
?>