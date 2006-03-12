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
                    if (make_user("x",$_POST["realname"],$_POST["web"],$_POST["email"],$_POST["password"],$_POST["username"])) echo "basarili!"; else echo "failed";
                }
                else {
                    ssv("error",MISSING_FIELDS);
                }
                break;
            case "register":
                $smarty->display("newuser.html");
                die();
                break;
            case "submitted_var_3":
                $$key = $value;
                break;
       }
    }

?>