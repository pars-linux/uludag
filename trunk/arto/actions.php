<?php
include_once("globals.php");

	switch ($_GET["call"]){
		case "updateuser":
			if (update_user($_SESSION["uid"],$_POST["realname"],$_POST["web"],$_POST["email"],$_POST["password"])){
			session_unregister("arto");
			$_SESSION["uname"]=$_POST['realname'];
			@session_register("arto");
			header ("location: index.php?userdetails&success");
			}
			else header ("location: index.php?error");
		break;

		case "addtheme":
			if (add_theme($_SESSION["uid"],$_POST["theme_name"],$_POST["theme_type"],$_POST["theme_path"],$_POST["theme_license"],$_POST["theme_description"],$_POST["theme_note"],$_POST["theme_date"])) header ("location: index.php?userfiles");
			else header ("location: index.php?error");
			break;

                case "addcomment":
                        if (add_comment($_POST["file_id"],$_SESSION["uid"],$_POST["comment_date"],$_POST["comment"])) header ("location: index.php?id=".$_POST["file_id"]);
                        else header ("location: index.php?error");
                break;
	}

?>