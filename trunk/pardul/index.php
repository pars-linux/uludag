<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    require ("lib/var.php");

    foreach ($_GET as $key => $value){
       switch ($key){
            case "register_f":
                if (isset($_POST["username"])&&isset($_POST["realname"])&&isset($_POST["password"])&&isset($_POST["email"])) {
                    if (make_user("x",$_POST["realname"],$_POST["web"],$_POST["email"],$_POST["password"],$_POST["username"])) ssv("message",SUCCESS); else ssv("message",FAILED);
                }
                else {
                    ssv("message",MISSING_FIELDS);
                }
                $smarty->display("newuser.html");
                die();
                break;
            case "register":
                $smarty->display("newuser.html");
                die();
                break;
            case "newhardware":
                $smarty->display("newhardware.html");
                die();
                break;
            case "submitted_var_3":
                $$key = $value;
                break;
       }
    }

?>