<?php

    /*
        TUBITAK UEKAE 2005-2006 
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    $known_languages = Array ("tr","en");

    if ($_SESSION["AL"]=="") $_SESSION["AL"]=$config['core']['lang'];
    if (isset($_GET["setlang"]))
        if (false!==array_search($_GET["setlang"],$known_languages))
            $_SESSION["AL"]=$_GET["setlang"];

?>
