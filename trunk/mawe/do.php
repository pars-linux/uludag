<?php

    /**
    *    TUBITAK UEKAE 2005-2006
    *    Gökmen GÖKSEL gokmen_at_pardus.org.tr
    *    Mawe - version 0.3
    */

    /**
    * Important Headers
    */
    require_once 'config/maWeSysCfg.php';
    require_once 'commonlib/php/maWeFunctions.php';

    /**
    * Easy of use
    */
    $G = $_GET;
    $P = $_POST;

    /**
    * make a db connection
    */
    maWeDBConnect($db);

    /**
    * setup smarty
    */
    maWeSetSmarty($sm);
    maWeSetSmartyVar("maWe",$smG);

    /**
    * Get Session State or DoLogin
    */
    $Control = maWeCheckLogin($P['DoLogin'],$P['maweUserName'],$P['mawePassword'],$G['quit']);

    /**
    * Check and start or die.
    */
    if ($Control){
        if (maWeAddPage($P['maWePageID'],$P['maWePageTitle'],$P['maWeFCKeditor'])) header ("location: login.php?edit=".$P['maWePageID']."&ok"); else echo "An error occured !";
    }
    else
        die();

?>
