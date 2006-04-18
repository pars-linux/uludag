<?php

    /**
    *    TUBITAK UEKAE 2005-2006
    *    Gökmen GÖKSEL gokmen_at_pardus.org.tr
    *    Mawe - version 0.3
    */

    /**
    * CommonConfig, includes maWe Sys Config Defaults.
    */
    $cc = Array();

    $cc['Path']     = '/home/rat/public_html/mawe/';
    $cc['DB']       = 'mysql';
    $cc['Session']	= 'mewapop';

    /**
    * DataBase, includes maWe DataBase Config Defaults.
    */
    $db = Array();

    $db['Server']   = '127.0.0.1';
    $db['UserName'] = 'root';
    $db['Password'] = 'goksel';
    $db['DbName']   = 'mawe';
    $db['DbPrefix'] = 'maWe';

    /**
    * Smarty, includes Smarty Config Defaults.
    */
    $sm = Array();

    $sm['Cache']    = 'false';
    $sm['Force']    = '1';
    $sm['Theme']    = 'mawe';

    $smG = Array();

    $smG['Title']	= 'maWe - make web easy 0.3';
    $smG['CharSet']	= 'UTF-8';
    $smG['Path']	= 'themes/'.$sm['Theme'].'/';
	
?>
