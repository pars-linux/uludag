<?php
include_once("config.php");

//including libmail
include_once($config['core']['path']."3rdparty/libmail/libmail.php");

// including smarty class and lang file
include_once($config['core']['path'].$config['smarty']['libdir']."/Smarty.class.php");
include_once($config['core']['path']."lang/lang-".$config['core']['lang'].".php");

// configuring smarty
$smarty = new Smarty;
$smarty->template_dir = $config['core']['path'].$config['smarty']['tpldir']."/".$config['core']['theme'];
$smarty->plugins_dir = array($config['core']['path'].$config['smarty']['libdir']."/plugins");
$smarty->cache_dir = $config['core']['path'].$config['smarty']['cachedir'];
$smarty->caching = $config['smarty']['caching'];
$smarty->compile_dir = $config['core']['path'].$config['smarty']['compiledir'];
$smarty->force_compile = $config['smarty']['forcecompile'];
$smarty->clear_all_cache();

// preparing smarty
$smarty->assign("title", $config['core']['title']);
$smarty->assign("desc", $config['core']['desc']);
$smarty->assign("url", $config['core']['url']);
$smarty->assign("themepath", $config['smarty']['tpldir']."/".$config['core']['theme']);
$smarty->assign("arto_signature","<a href=\"http://arto.fasafiso.org/\" title=\"Arto v{$config['arto']['version']} ({$config['arto']['builddate']})\">Arto  v{$config['arto']['version']}</a>");

// including arto functions
include_once("functions.php");
setlocale(LC_TIME,"tr_TR.UTF8");

//starting session
session_start();

//session unregister if "quit" selected
if (isset($_GET['quit'])) { session_unregister("arto"); header ("location: ".$_SELF); }

//connection to the database
db_connection('connect', $config['db']['hostname'].':'.$config['db']['port'], $config['db']['username'], $config['db']['password'], $config['db']['databasename'], $config['db']['connectiontype']);

//checking user if "user info's" posted

if (array_key_exists ('login', $_GET)){
	$username = rtag ($_POST['username']);
	$password = rtag ($_POST['password']);

	if ($ird=get_user_details($username,$password)){
		session_unregister("arto");
		@session_register("arto");
		$_SESSION["uid"]=$ird[0]['id'];
		$_SESSION["uname"]=$ird[0]['name'];
		$_SESSION["user"]=$username;
                $_SESSION["state"]=$ird[0]['state'];
		header ("location: ".$_SELF);
	}
	else $login_error=USER_OR_PASS_WRONG;
}
?>
