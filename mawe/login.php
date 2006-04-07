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
    require_once 'config/maWeLang.php';
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
        $Pages = maWeGet('Pages');
        maWeSetSmartyVar("PageList", maWeGet('Pages'));

        isset($G['ok']) ? maWeSetSmartyVar("OK",UPDATE_OK) : maWeSetSmartyVar("OK","");
        is_numeric($G['edit']) ? $Value = maWeGet('Pages','ID',$G['edit']) : $Value = "";

            maWeSetSmartyVar("PageTitle",$Value[0]['PageTitle']);
            maWeSetSmartyVar("PageID",$Value[0]['ID']);
            maWeSetSmartyVar("FCK",maWeShowFCK($Value[0]['PageBody']));

        maWeShowSmarty('admin.mt');
    }
    else
        die();

?>
