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
    ssv("p_bustypes",get_("x","BusTypes"));
    ssv("p_category",get_categories());

//  For All Users (Guest)
    foreach ($_GET as $key => $value){
        switch ($key){
            case "activateuser":
                if ($_GET['username'] AND $_GET['code']){
                    $msj = activate_user($_GET['username'],$_GET['code']);
                    ssv("message",$msj);
                    $smarty->display("welcome.html");
                    die();
                }
                break;
            case "register_f":
                if (isset($_POST["username"])&&isset($_POST["realname"])&&isset($_POST["password"])&&isset($_POST["email"])) {
                    if (make_user("x",$_POST["realname"],$_POST["web"],$_POST["email"],$_POST["password"],$_POST["username"])) {
                        $id=mysql_insert_id();
                        echo $id;
                        if (send_activation_mail($id,$_POST["username"])) ssv("message",REGISTER_OK); else ssv("message",SENDMAIL_ERROR);
                    }
                    else ssv("message",CONFLICT_ERROR);
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
                ssv("cm",get_comments($_GET["detail"]));
                ssv("rs",get_states($_GET["detail"]));
                $smarty->display("details.html");
                die();
                break;
            case "search":
                if (isset($_POST["p_name"])&&isset($_POST["p_vendor"])&&isset($_POST["p_category"])) {
                    if ($temp=find_product($_POST["p_vendor"],$_POST["p_name"],$_POST["p_category"],$_POST["p_device_id"],$_POST["p_bus_type"])) ssv ("sr",$temp); else ssv("message",NOT_FOUND.MAINLINK);
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
                        if ($_SESSION["state"]<>"A") ssv("message",RESCTRICTED_AREA.MAINLINK);
                    }
                    $smarty->display("newhardware.html");
                    die();
                    break;
                case "newhardware_f":
                    if ($_POST["p_name"]<>""&&$_POST["p_vendor"]<>""&&$_POST["p_category"]<>""&&$_POST["p_distro"]<>"") {
                        if (make_hardware("x",$_POST["p_name"],$_POST["p_vendor"],$_POST["p_device_id"],$_POST["p_bus_type"],$_POST["p_category"],$_POST["p_date"],'0',$_POST["userid"],"",$_POST["p_distro"],$_POST["p_state"],$_POST["p_todo"])) header ("location: ?myhardwares");
                        else ssv("message",ERROR.MAINLINK);
                    }
                    else {
                        ssv("message",MISSING_FIELDS);
                    }
                    $smarty->display("newhardware.html");
                    die();
                    break;
                case "myhardwares":
                    if ($temp=get_products("UserID",$_SESSION["uid"])) ssv("sr",$temp); else ssv("message",NO_RECORD);
                    $smarty->display("myhardwares.html");
                    die();
                    break;
                case "edit":
                    if (check_entry($_SESSION["uid"],$_GET["edit"])){
                        ssv("sr",get_($_GET["edit"],"Hardwares"));
                        ssv("rs",get_states($_GET["edit"]));
                    } else ssv("message",WRONG_ENTRY);
                    $smarty->display("approve.html");
                    die();
                    break;
                case "edit_f":
                    if ($_POST["p_name"]<>""&&$_POST["p_vendor"]<>""&&$_POST["p_category"]<>""&&$_POST["p_distro"]<>""&&$_POST["p_id"]<>"") {
                        if (make_hardware($_POST["p_id"],$_POST["p_name"],$_POST["p_vendor"],$_POST["p_device_id"],$_POST["p_bus_type"],$_POST["p_category"],$_POST["p_date"],'0',$_POST["userid"],"",$_POST["p_distro"],$_POST["p_state"],$_POST["p_todo"])) header ("location: ?myhardwares");
                        else ssv("message",ERROR.MAINLINK);
                    }
                    else {
                        ssv("message",MISSING_FIELDS);
                    }
                    $smarty->display("myhardwares.html");
                    die();
                    break;
                case "ac":
                    if ($_POST["p_comment"]<>""&&$_POST["p_date"]<>""&&$_POST["userid"]<>""&&$_POST["p_id"]<>"") {
                        if (make_comment("x",$_POST["p_id"],$_POST["userid"],$_POST["p_comment"],$_POST["p_date"])) header ("location: ?detail=".$_POST["p_id"]);
                        else ssv("message",ERROR);
                    }
                    else {
                        ssv("message",MISSING_FIELDS);
                    }
                    break;
            }
        }
    }

//  For Admin Users (A)
    if (session_is_registered("pardon") AND $_SESSION["state"]=="A") {
        foreach ($_GET as $key => $value){
            switch ($key){
                case "queue":
                    if (isset($_GET["del"])) { if ($_GET["from"]) $link=$_GET["from"]; else $link="queue"; del_($_GET["del"],"Hardwares"); header("location: ?".$link);}
                    if (isset($_GET["set"])) { if ($_GET["from"]) $link=$_GET["from"]; else $link="queue"; activate_($_GET["set"]); header ("location: ?".$link);}
                    if ($temp=get_products("Status",0)) ssv("sr",$temp); else ssv("message",NO_QUEUE.MAINLINK);
                    $smarty->display("queue.html");
                    die();
                    break;
                case "queue_edit":
                    ssv("admin",TRUE);
                    ssv("sr",get_($_GET["queue_edit"],"Hardwares"));
                    ssv("rs",get_states($_GET["queue_edit"]));
                    $smarty->display("approve.html");
                    die();
                    break;
                case "queue_edit_f":
                    if ($_POST["p_name"]<>""&&$_POST["p_vendor"]<>""&&$_POST["p_category"]<>""&&$_POST["p_distro"]<>""&&$_POST["p_id"]<>"") {
                        if (make_hardware($_POST["p_id"],$_POST["p_name"],$_POST["p_vendor"],$_POST["p_device_id"],$_POST["p_bus_type"],$_POST["p_category"],$_POST["p_date"],'0',$_POST["userid"],$_POST["suserid"],$_POST["p_distro"],$_POST["p_state"],$_POST["p_todo"])){ activate_($_POST["p_id"]); header ("location: ?queue");}
                        else ssv("message",ERROR.MAINLINK);
                    }
                    else {
                        ssv("message",MISSING_FIELDS);
                    }
                    $smarty->display("aprrove.html");
                    die();
                    break;
                case "users":
                    if (isset($_GET["del"])) del_($_GET["users"],"Users");
                    if (isset($_GET["set"])) set_($_GET["users"],$_GET["set"]);
                    ssv("sr",get_("x","UniqUsers"));
                    $smarty->display("userlist.html");
                    die();
                    break;
                case "hw_list":
                    ssv("full",TRUE);
                    if ($temp=get_products("Status",1)) ssv("sr",$temp); else ssv("message",NO_RECORD.MAINLINK);
                    $smarty->display("queue.html");
                    die();
                    break;
            }
        }
    }
    $smarty->display("welcome.html");
?>
