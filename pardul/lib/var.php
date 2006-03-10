<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    require_once ("etc/config.php");
    require_once ("lib/version.php");
    require_once ("lib/utils.php");

    require_once($config['core']['path'].$config['smarty']['libdir']."/Smarty.class.php");

    setlocale(LC_TIME,"tr_TR.UTF8");

    $smarty = new Smarty;

    $smarty->template_dir = $config['core']['path'].$config['smarty']['tpldir']."/".$config['core']['theme'];
    $smarty->plugins_dir = array($config['core']['path'].$config['smarty']['libdir']."/plugins");
    $smarty->cache_dir = $config['core']['path'].$config['smarty']['cachedir'];
    $smarty->caching = $config['smarty']['caching'];
    $smarty->compile_dir = $config['core']['path'].$config['smarty']['compiledir'];
    $smarty->force_compile = $config['smarty']['forcecompile'];
    $smarty->clear_all_cache();

    $smarty->assign("pardul-v","v{$config['pardul']['version']} (r{$config['pardul']['build']})");
    $smarty->assign("pardul-title", $config['core']['title']);
    $smarty->assign("pardul-desc", $config['core']['desc']);
    $smarty->assign("pardul-url", $config['core']['url']);
    $smarty->assign("themepath", "etc/".$config['smarty']['tpldir']."/".$config['core']['theme']);

    db_connection('connect', $config['db']['host'].':'.$config['db']['port'], $config['db']['user'], $config['db']['pass'], $config['db']['dbname'], $config['db']['ctype']);

?>