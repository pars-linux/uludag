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

    setlocale(LC_TIME,"tr_TR.UTF8");

    db_connection('connect', $config['db']['host'].':'.$config['db']['port'], $config['db']['user'], $config['db']['pass'], $config['db']['dbname'], $config['db']['ctype']);

    session_start();

    if (isset($_GET['quit'])) {
        session_unregister("pgx");
        $_SESSION["state"]="";
        header ("location: ".$_SELF);
    }

    if (array_key_exists ('login', $_GET)){
        $pass = rtag($_POST['pass']);

        if (md5($pass)==$config['core']['pass']){
            session_unregister("pgx");
            @session_register("pgx");
            header ("location: index.php");
        }
        else $login_error=USER_OR_PASS_WRONG;
    }

?>
