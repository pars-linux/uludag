<?php
include("globals.php");

	if (session_is_registered("arto")){
                $preview = get_preview($_GET["id"]);
		set_smarty_vars("preview",$preview);
                $smarty->display("preview.html");
                die();
	}
        else{
            //Fixme: adam gibi hata göster.
            Header("Location: index.php");
        }
?>