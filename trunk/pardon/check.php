<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    require ("lib/var.php");

    if (isset($_GET["username"])) {
    if (strlen($_GET["username"]) > 4) {
        if (user_exist($_GET["username"])) ssv("state","UE");
        else ssv("state", "UO");
    }
    else ssv("state","UNO");
    $smarty->display("message.html");
    die();
    }

    if (isset($_GET["vendorpref"])) {
        $vendorlist = find_vendor($_GET["vendorpref"]);
        if ($vendorlist) { 
            foreach ($vendorlist as $vendor)
                $message.="<div class=\"ozvendorlist\" onclick=\"$('p_vendor').value='".$vendor["VendorName"]."'\">".$vendor["VendorName"]."</div>";
        }
        else $message = "NV";
        ssv("list",$message);
        $smarty->display("message.html");
        die();
    }


?>
