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
        $body = unicode_decode($P['body']);
        if (maWeAddPage($P['id'],$P['title'],$body)) echo "<div style='padding:10px'><img src='".$smG['Path']."images/info.png' style='padding-right:5px' />Update success !</div>"; else echo "An error occured !";
    }
    else
        die();

?>
