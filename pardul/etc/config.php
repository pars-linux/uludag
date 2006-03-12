<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    $config['core']['title']            = "Pardul - Pardus Donanım Uyumluluk Listesi";
    $config['core']['desc']             = "Pardus ile kullanılabilecek donanımların listesi..";
    $config['core']['path']             = "/home/pardul/public_html/";
    $config['core']['url']              = "http://localhost/~pardul/";
    $config['core']['email']            = "pardul@uludag.org.tr";
    $config['core']['postperpage']      = "5";
    $config['core']['postsinfeed']      = "10";
    $config['core']['theme']            = "pardul";
    $config['core']['temp']             = "tmp";
    $config['core']['lang']             = "tr";

    $config['db']['host']               = "localhost";
    $config['db']['port']               = "3306";
    $config['db']['user']               = "pardul";
    $config['db']['pass']               = "pardul";
    $config['db']['dbname']             = "pardul";
    $config['db']['tableprefix']        = "pardul";
    $config['db']['ctype']              = "persistent";

    $config['smarty']['libdir']         = "lib/smarty";
    $config['smarty']['tpldir']         = "etc/themes";
    $config['smarty']['compiledir']     = "tmp";
    $config['smarty']['cachedir']       = "tmp";
    $config['smarty']['plugindir']      = "plugins";
    $config['smarty']['caching']        = "false";
    $config['smarty']['forcecompile']   = "1";

?>
