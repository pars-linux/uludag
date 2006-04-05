<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    require ("lib/var.php");
    echo "<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"></head>";

    if (isset($_GET["username"])) {
    if (strlen($_GET["username"]) > 4) {
        if (user_exist($_GET["username"])) echo "<span style=\"color: red\">Bu kullanıcı adı ile bir kullanıcı kayıtlı !</span>"; else echo "<span style=\"color: green\">Kullanıcı adı müsait</span>";
    }
    else echo "<span style=\"color: red\">Bu kullanıcı adı uygun değil !</span>";
    die();
    }
    
    if (isset($_GET["vendorpref"])) {
        $vendorlist = find_vendor($_GET["vendorpref"]);
        if ($vendorlist) { 
            foreach ($vendorlist as $vendor)
                echo "<div class=\"ozvendorlist\" onclick=\"$('p_vendor').value='".$vendor["VendorName"]."'\">".$vendor["VendorName"]."</div>";
        }
        else echo "Üretici bulunamadı<br>Eğer geçerli bir üretici ise yönetici tarafından eklenecektir";
    }
?>
