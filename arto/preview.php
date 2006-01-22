<?php
include("globals.php");

                $preview = get_preview($_GET["id"]);
		set_smarty_vars("preview",$preview);
                $smarty->display("preview.html");
                die();
?>