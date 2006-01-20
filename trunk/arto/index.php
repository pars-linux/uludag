<?php
include_once("globals.php");

	if (session_is_registered("arto")){
		set_smarty_vars("username",$_SESSION["user"]);
		set_smarty_vars("name",$_SESSION["uname"]);
		set_smarty_vars("level",$_SESSION["state"]);
	}

	$child_type=get_type($_GET["sid"]);
	$parent_type=get_type($_GET["cid"]);
	set_smarty_vars("login_error",$login_error);
	set_smarty_vars("categories",get_types());
	set_smarty_vars("sub_type",$child_type[0]["type"]);
	set_smarty_vars("parent_type",$parent_type[0]["type"]);
        set_smarty_vars("licenses",get_licenses());

	if (isset($_GET["id"])) {
                if (session_is_registered("arto")) {
                    set_smarty_vars("userdetails",TRUE);
		}
		$nodes = get_something("single",$_GET["id"]);
		$temp = get_user_something($nodes[0]['user'],"uname");
		set_smarty_vars("nodes",$nodes);
                set_smarty_vars("author",$temp[0]['uname']);
		set_smarty_vars("comments",get_comments($_GET["id"]));
		$smarty->display("post.html");
		die();
	}
	
	elseif (isset($_GET["cid"])) {
		if (isset($_GET["sid"])) set_smarty_vars("nodes",get_something("cat",$_GET["cid"],$_GET["sid"]));
		else set_smarty_vars("nodes",get_something("cat",$_GET["cid"]));
		set_smarty_vars("comments",get_comments($_GET["id"]));
		$smarty->display("posts.html");
		die();
	}

	elseif (isset($_GET["register"])) {
            if (isset($_POST["username"])){
                if (user_exist($_POST["username"])) {
                            set_smarty_vars("error",USER_EXIST);
		            set_smarty_vars("up_name",$_POST["realname"]);
		            set_smarty_vars("up_web",$_POST["web"]);
		            set_smarty_vars("up_email",$_POST["email"]);
		            set_smarty_vars("up_pass",$_POST["password"]);
                }
                elseif (update_user("",$_POST["realname"],$_POST["web"],$_POST["email"],$_POST["password"],1,$_POST["username"])){
                            $temporary = get_user_id($_POST["username"]);
                            $activationcode = md5($temporary[0]['id'].$config["core"]["secretkey"]);
                            $mail_message = "Merhaba\n\n    Siz ya da bir başkası bu e-posta adresini kullanarak {$config['core']['title']} ({$config['core']['url']}) sitesine kayıt yaptırdı.\n    Eğer kaydı siz yaptırdıysanız onaylamak için aşağıdaki bağlantıyı tıklayın.\n\n Onaylamak için tıklayın: {$config['core']['url']}?activateuser&username={$_POST["username"]}&code={$activationcode}\n İptal etmek için tıklayın: {$config['core']['url']}?activateuser&action=delete&username={$_POST["username"]}&code={$activationcode}\n\n İlginiz için teşekkürler.\n Uludağ Projesi";
                            sendmail($config['core']['email'],$_POST["email"],REGISTER_EMAIL_SUBJECT,$mail_message,"3");
                            set_smarty_vars("info",REGISTER_OK);
                }
            }
		$smarty->display("register.html");
		die();
	}

	elseif (isset($_GET["newtheme"])) {
		if (session_is_registered("arto")) {
		set_smarty_vars("userdetails",TRUE);
		}
		$smarty->display("new-theme.html");
		die();
	}

	elseif (isset($_GET["userdetails"])) {
		if (session_is_registered("arto")) {
		$details=get_user_details($_SESSION["uid"],$_SESSION["user"],4);
		set_smarty_vars("name",$details[0]["name"]);
		set_smarty_vars("up_user",$details[0]["uname"]);
		set_smarty_vars("up_name",$details[0]["name"]);
		set_smarty_vars("up_web",$details[0]["web"]);
		set_smarty_vars("up_email",$details[0]["email"]);
		set_smarty_vars("userdetails",TRUE);
                if (isset($_GET["success"])) set_smarty_vars("success",UPDATE_OK);
		}
		$smarty->display("register.html");
		die();
	}

	elseif (isset($_GET["activateuser"])) {
		$message = activate_user($_GET['username'],$_GET['code'],$_GET['action']);
                $message["title"] = ACTIVATE_USER_TITLE;
		set_smarty_vars("message",$message);
		$smarty->display("message.html");
		die();
	}

	elseif (isset($_GET["userfiles"])) {
		if (session_is_registered("arto")) {
		$files = get_user_files($_SESSION["uid"]);
		for($i = 0; $i < count($files); $i++){
			$files[$i]["types"] = set_types($files[$i]["type"],$files[$i]["sub_type"]);
			$files[$i]["release"] = conv_time("db2post",$files[$i]["release"]);
		}
		set_smarty_vars("uf",$files);
		}
		$smarty->display("userfiles.html");
		die();
	}

        elseif (isset($_GET["missions"])) {
		if (session_is_registered("arto") AND $_SESSION["state"]<=1) {
                    set_smarty_vars("info",OK);
                    set_smarty_vars("auth",TRUE);
                    if (isset($_GET["tid"])) {
                        $files=get_missions($_SESSION["uid"],$_GET["tid"]);
                        $files[0]["types"] = set_types($files[0]["type"],$files[0]["sub_type"],1);
                        set_smarty_vars("uf",$files);
                        $smarty->display("mission.html");
                        die();
                    }
                    elseif (isset($_GET["finish"])) {
                        if (isset($_POST["del"])) {
                            
                        }
                        elseif (isset($_POST["add"])) {
                            if($new_path=get_content($_POST["theme_path"],$_POST["theme_id"],$_POST["theme_path2"])) {
                                $temp = pathinfo($_POST["theme_path2"]);
                                if ($_POST["theme_path2"]<>"") $newsubpath= "2-".$_POST["theme_id"]."-".$temp['basename'];
                                if(add_theme($_POST["theme_id"],$_POST["theme_name"],$_POST["theme_type"],$new_path,$newsubpath,$_POST["theme_license"],$_POST["theme_description"],$_POST["theme_note"],$_POST["theme_date"],$_SESSION["uid"],1)) set_smarty_vars("status",THEME_ADDED);
                                else set_smarty_vars("status","hataaaa");//fix me düzgün hata yap
                            }
                            else set_smarty_vars("status",LOGIC_ERROR);//fix me düzgün hata yap
                        }
                    }
                    else {
                        $files=get_missions($_SESSION["uid"]);
                        for($i = 0; $i < count($files); $i++){
			     $files[$i]["types"] = set_types($files[$i]["type"],$files[$i]["sub_type"]);
			     $files[$i]["release"] = conv_time("db2post",$files[$i]["release"]);
                             $temp=get_user_something($files[$i]["user"],"name");
                             $files[$i]["author"] = $temp[0]["name"];
                             $temp=get_user_something($files[$i]["user"],"email");
                             $files[$i]["email"] = $temp[0]["email"];
		        }
		     set_smarty_vars("uf",$files);
                    }
                }
                else {
                    set_smarty_vars("auth",FALSE);
                }
            $smarty->display("missions.html");
            die();
        }
	
	else {
		set_smarty_vars("nodes",get_something("cat","1"));
		$smarty->display("posts.html");
		die();
	}

db_connection("disconnect");
?>
