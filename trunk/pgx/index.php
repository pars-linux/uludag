<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    require ("lib/var.php");

    foreach ($_GET as $key => $value){
        switch ($key){
            case "newuser":
                if ($_POST["UserRealName"]<>"" && $_POST["UserEmail"]<>"" && $_POST["UserPhone"]<>"" && $_POST["UserAddress"]<>"") {
                    echo "hede";
                }
            break;
        }
    }

?>
