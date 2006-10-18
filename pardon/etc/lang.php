<?php

    /*
        TUBITAK UEKAE 2005-2006 
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    $known_languages = Array ("tr","en");

    if (false!==array_search($_GET["pattern"],$known_languages) AND isset($_SESSION["AL"]))
        require_once("etc/".$_SESSION["AL"].".php");
    else
        require_once("etc/tr.php");

?>
