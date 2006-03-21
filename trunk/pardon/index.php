<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    require ("lib/var.php");

//  Session Check
    if (session_is_registered("pardon")){
        ssv("UserName",$_SESSION["user"]);
        ssv("UserRealName",$_SESSION["uname"]);
        ssv("UserState",$_SESSION["state"]);
        ssv("UserID",$_SESSION["uid"]);
    }

//  Get Standarts
    ssv("p_vendor",get_("x","Vendors"));
    ssv("p_distro",get_("x","Distribution"));
    ssv("p_scat",get_("x","Categories"));
    ssv("p_category",get_categories());

//  For All Users (Guest)
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
            case "detail":
                ssv("sr",get_($_GET["detail"],"Hardwares"));
                $smarty->display("details.html");
                die();
                break;
            case "search":
                if (isset($_POST["p_name"])&&isset($_POST["p_vendor"])&&isset($_POST["p_category"])) {
                    ssv ("sr",find_product($_POST["p_vendor"],$_POST["p_name"],$_POST["p_category"],$_POST["p_device_id"],$_POST["p_bus_type"]));
                }
                $smarty->display("search.html");
                die();
                break;
        }
    }

//  For SAdmin Users (SA)
    if (session_is_registered("pardon") AND $_SESSION["state"]=="SA" OR $_SESSION["state"]=="A") {
        foreach ($_GET as $key => $value){
            switch ($key){
                case "newhardware":
                    if (!session_is_registered("pardon")){
                        if ($_SESSION["state"]<>"A") ssv("message",RESCTRICTED_AREA);
                    }
                    $smarty->display("newhardware.html");
                    die();
                    break;
                case "newhardware_f":
                    if ($_POST["p_name"]<>""&&$_POST["p_vendor"]<>""&&$_POST["p_category"]<>"") {
                        if (make_hardware("x",$_POST["p_name"],$_POST["p_vendor"],$_POST["p_device_id"],$_POST["p_bus_type"],$_POST["p_category"],$_POST["p_date"],'0',$_POST["userid"],"",$_POST["p_distro"],$_POST["p_state"],$_POST["p_todo"])) header ("location: ?myhardwares");
                        else ssv("message",FAILED);
                    }
                    else {
                        ssv("message",MISSING_FIELDS);
                    }
                    $smarty->display("newhardware.html");
                    die();
                    break;
                case "myhardwares":
                    ssv("userpage","x");
                    ssv("sr",get_products("UserID",$_SESSION["uid"]));
                    $smarty->display("myhardwares.html");
                    die();
                    break;
                case "edit":
                    ssv("sr",get_($_GET["edit"],"Hardwares"));
                    $smarty->display("approve.html");
                    die();
                    break;
            }
        }
    }

//  For Admin Users (A)
    if (session_is_registered("pardon") AND $_SESSION["state"]=="A") {
        foreach ($_GET as $key => $value){
            switch ($key){
                case "queue":
                    if (isset($_GET["del"])) del_($_GET["del"],"Hardwares");
                    if (isset($_GET["set"])) activate_($_GET["set"]);
                    ssv("sr",get_products("Status",0));
                    $smarty->display("queue.html");
                    die();
                    break;
                case "users":
                    if (isset($_GET["del"])) del_($_GET["users"],"Users");
                    if (isset($_GET["set"])) set_($_GET["users"],$_GET["set"]);
                    ssv("sr",get_("x","Users"));
                    $smarty->display("userlist.html");
                    die();
                    break;
            }
        }
    }

    $smarty->display("welcome.html");
?>
