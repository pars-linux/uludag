<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    require ('etc/config.php');
    require ('lib/modules/tools.php');

    build_smarty($cf);
    $smarty->display("homepage.html");
?>
