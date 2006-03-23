<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    require_once ("etc/config.php");
    require_once ("etc/lang.php");
    require_once ("lib/libmail.php");
    require_once ("lib/version.php");
    require_once ("lib/utils.php");

    $config["core"]["secretkey"] = "deneme";

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

    ssv("pardul_v","v{$config['pardul']['version']} (d{$config['pardul']['build']})");
    ssv("pardul_title", $config['core']['title']);
    ssv("pardul_desc", $config['core']['desc']);
    ssv("pardul_url", $config['core']['url']);
    ssv("tp", $config['smarty']['tpldir']."/".$config['core']['theme']);

    db_connection('connect', $config['db']['host'].':'.$config['db']['port'], $config['db']['user'], $config['db']['pass'], $config['db']['dbname'], $config['db']['ctype']);

    session_start();

    if (isset($_GET['quit'])) {
        session_unregister("pardon");
        $_SESSION["state"]="";
        header ("location: ".$_SELF);
    }

    if (array_key_exists ('login', $_GET)){
        $user = rtag($_POST['user']);
        $pass = rtag($_POST['pass']);

        if ($ird=get_user_details($user,$pass)){
            session_unregister("pardon");
            @session_register("pardon");
            $_SESSION["uid"]=$ird[0]['ID'];
            $_SESSION["uname"]=$ird[0]['UserRealName'];
            $_SESSION["user"]=$user;
            $_SESSION["state"]=$ird[0]['UserState'];
            header ("location: index.php");
        }
        else $login_error=USER_OR_PASS_WRONG;
    }

?>
