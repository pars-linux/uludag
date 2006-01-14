<?php
include_once("globals.php");

	if (session_is_registered("arto")){
		set_smarty_vars("username",$_SESSION["user"]);
		set_smarty_vars("name",$_SESSION["uname"]);
	}

	$child_type=get_type($_GET["sid"]);
	$parent_type=get_type($_GET["cid"]);
	set_smarty_vars("login_error",$login_error);
	set_smarty_vars("categories",get_types());
	set_smarty_vars("sub_type",$child_type[0]["type"]);
	set_smarty_vars("parent_type",$parent_type[0]["type"]);

	if (isset($_GET["id"])) {
		set_smarty_vars("nodes",get_something("single",$_GET["id"]));
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
		$smarty->display("register.html");
		die();
	}

	elseif (isset($_GET["newtheme"])) {
		if (session_is_registered("arto")) {
		set_smarty_vars("licenses",get_licences());
		set_smarty_vars("userdetails",TRUE);
		}
		$smarty->display("new-theme.html");
		die();
	}

	elseif (isset($_GET["userdetails"])) {
		if (session_is_registered("arto")) {
		$details=get_user_details($_SESSION["uid"],$_SESSION["user"],1);
		set_smarty_vars("name",$details[0]["name"]);
		set_smarty_vars("up_user",$details[0]["uname"]);
		set_smarty_vars("up_name",$details[0]["name"]);
		set_smarty_vars("up_web",$details[0]["web"]);
		set_smarty_vars("up_email",$details[0]["email"]);
		set_smarty_vars("up_pass",$details[0]["password"]);
		set_smarty_vars("userdetails",TRUE);
		}
		$smarty->display("register.html");
		die();
	}

	elseif (isset($_GET["userfiles"])) {
		if (session_is_registered("arto")) {
// 		$files=get_user_files($_SESSION["uid"]);
		set_smarty_vars("userdetails",TRUE);
		}
		$smarty->display("userfiles.html");
		die();
	}
	
	else {
		set_smarty_vars("nodes",get_something("cat","1"));
		$smarty->display("posts.html");
		die();
	}

db_connection("disconnect");
?>
