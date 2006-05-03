<?php
include_once("config.php");

// including smarty class
include_once($config['core']['path'].$config['smarty']['libdir']."/Smarty.class.php");

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
$smarty->assign("url", $config['core']['url']);
$smarty->assign("themepath", $config['smarty']['tpldir']."/".$config['core']['theme']);

// including functions
include_once("google.client.php");
setlocale(LC_TIME,"tr_TR.UTF8");
?>