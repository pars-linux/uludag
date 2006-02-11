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
			if (add_theme($_SESSION["uid"],$_POST["theme_name"],$_POST["theme_type"],$_POST["theme_path"],$_POST["theme_path2"],$_POST["theme_license"],$_POST["theme_description"],$_POST["theme_note"],$_POST["theme_date"])) header ("location: index.php?userfiles");
			else header ("location: index.php?error");
			break;

                case "addcomment":
                        if (add_comment($_POST["file_id"],$_SESSION["uid"],$_POST["comment_date"],$_POST["comment"])) {
                            $comment=rtag($_POST["comment"]);
                            $temp = get_user_something($_SESSION["uid"],"*");
                            $temp2 = get_file_author($_POST["file_id"]);
                            $mail_message = "Merhabalar {$temp2[0]['name']} ({$temp2[0]['uname']}),\n {$config['core']['url']}node/{$_POST["file_id"]} adresindeki içeriğiniz için {$temp[0]['name']} ({$temp[0]['uname']}) tarafından  bir yorum yapılmış: \n\n $comment \n\n İlginiz için teşekkürler.\n Uludağ Projesi";

                            sendmail($config['core']['email'],$temp2[0]['email'],COMMENT_EMAIL_SUBJECT,$mail_message,"3");
                            header ("location: index.php?id=".$_POST["file_id"]);
                        }
                        else header ("location: index.php?error");
                break;
	}

?>