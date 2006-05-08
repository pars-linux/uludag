<?php

     /*
         TUBITAK UEKAE 2005-2006
         Gökmen GÖKSEL gokmen_at_pardus.org.tr
     */

    session_start();

    if (isset($_GET['quit'])) {
        session_unregister($cf['core']["session_key"]);
        $_SESSION["state"]="";
        header ("location: ".$_SELF);
    }

    if (array_key_exists ('login', $_GET)){
        $user = rtag($_POST['user']);
        $pass = rtag($_POST['pass']);

        if ($ird=get_user_details($user,$pass)){
            session_unregister($cf['core']["session_key"]);
            @session_register($cf['core']["session_key"]);
            $_SESSION["uid"]=$ird[0]['ID'];
            $_SESSION["uname"]=$ird[0]['UserRealName'];
            $_SESSION["user"]=$user;
            $_SESSION["state"]=$ird[0]['UserState'];
            header ("location: index.php");
        }
        else $login_error=USER_OR_PASS_WRONG;
    }

?>
