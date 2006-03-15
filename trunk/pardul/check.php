<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    require ("lib/var.php");
    echo "<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"></head>";

    if (strlen($_GET["username"]) > 4) {
        if (user_exist($_GET["username"])) echo "<span style=\"color: red\">Bu kullanıcı adı ile bir kullanıcı kayıtlı !</span>"; else echo "<span style=\"color: green\">Kullanıcı adı müsait</span>";
    }
    else echo "<span style=\"color: red\">Bu kullanıcı adı uygun değil !</span>";

?>
