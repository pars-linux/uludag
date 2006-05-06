<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */
    
    require ('etc/config.php');
    require ('lib/lib.php');
    require ('lib/modules/db.php');

    function build_smarty(){
        global $smarty,$cf;
        require_once($cf['core']['path'].$cf['smarty']['libdir']."/Smarty.class.php");

        $smarty = new Smarty;
        $smarty->template_dir = $cf['core']['path'].$cf['smarty']['tpldir'];
        $smarty->plugins_dir = array($cf['core']['path'].$cf['smarty']['libdir']."/plugins");
        $smarty->cache_dir = $cf['core']['path'].$cf['smarty']['cachedir'];
        $smarty->caching = $cf['smarty']['caching'];
        $smarty->compile_dir = $cf['core']['path'].$cf['smarty']['compiledir'];
        $smarty->force_compile = $cf['smarty']['forcecompile'];
        $smarty->clear_all_cache();

    }

    function ssv($varname, $var){
        global $smarty;
        $smarty->assign($varname,$var);
    }

    function build_defaults(){
        global $cf;
        db_connection('connect', $cf['db']['host'].':'.$cf['db']['port'], $cf['db']['user'], $cf['db']['pass'], $cf['db']['dbname'], $cf['db']['ctype']);
    }
   
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

