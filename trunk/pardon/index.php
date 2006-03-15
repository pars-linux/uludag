<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    require ("lib/var.php");

    if (session_is_registered("pardon")){
        ssv("UserName",$_SESSION["user"]);
        ssv("UserRealName",$_SESSION["uname"]);
        ssv("UserState",$_SESSION["state"]);
        ssv("UserID",$_SESSION["uid"]);
    }

    ssv("p_vendor",get_("x","Vendors"));
    ssv("p_distro",get_("x","Distribution"));
    ssv("p_category",get_categories());

    foreach ($_GET as $key => $value){
       switch ($key){
            case "register_f":
                if (isset($_POST["username"])&&isset($_POST["realname"])&&isset($_POST["password"])&&isset($_POST["email"])) {
                    if (make_user("x",$_POST["realname"],$_POST["web"],$_POST["email"],$_POST["password"],$_POST["username"])) {
                        ssv("message",SUCCESS);
                    }
                    else ssv("message",FAILED);
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
            case "search":
                $smarty->display("search.html");
                die();
                break;
            case "newhardware":
                if ($_SESSION["state"]<>"A") ssv("message",RESCTRICTED_AREA);
                $smarty->display("newhardware.html");
                die();
                break;
            case "newhardware_f":
                if ($_SESSION["state"]<>"A") {
                    ssv("message",RESCTRICTED_AREA);
                }
                else 
                    if (isset($_POST["p_name"])&&isset($_POST["p_vendor"])&&isset($_POST["p_category"])) {
                        if (make_hardware("x",$_POST["p_name"],$_POST["p_vendor"],$_POST["p_device_id"],$_POST["p_bus_type"],$_POST["p_category"],$_POST["p_date"],'0',$_POST["userid"])) {
//                             make_hardware_status(mysql_insert_id(),$_POST["p_distro"],$_POST["p_state"]);
                            ssv("message",SUCCESS);
                        }
                        else ssv("message",FAILED);
                    }
                    else {
                        ssv("message",MISSING_FIELDS);
                    }
                $smarty->display("newhardware.html");
                die();
                break;
            case "submitted_var_3":
                $$key = $value;
                break;
       }
    }
    $smarty->display("welcome.html");
?>