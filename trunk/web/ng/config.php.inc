<?php

    // TUBITAK/UEAKE - 2006-07 - Pardus
    // Gökmen GÖKSEL <gokmen@pardus.org.tr>
    // Config file for PardusWeb
    // Edit and saveas 'config.php' in the same directory

    $CF["DbHost"]  = 'localhost';
    $CF["DbUser"]  = 'username';
    $CF["DbPass"]  = 'password';
    $CF["DbData"]  = 'dbname';
    $CF["DbLogLevel"] = 4;
    $CF["UsePrefix"] =  false;

    $CF["Modules"]["BLOGS"]["BlogUrl"] = "http://**/**.xml";
    $CF["Modules"]["BLOGS"]["Count"]   = 4;
    $CF["Modules"]["BLOGS"]["CharLen"] = 30;

    $CF["Tools"]["Pic"]["Enable"] = true;
    $CF["Tools"]["Pic"]["Dir"]="../images/texts/";

    $KnownLangs = Array ("tr","en");

?>
