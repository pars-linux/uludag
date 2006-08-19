<?php

    // Gökmen GÖKSEL
    // Get news with given NewsID

    if (is_numeric($_GET["NewsID"])) {
        require_once('config.php');
        require_once('vezir.php');

        $Vezir = new Vezir($CF);
        $Pardus = new Pardus($Vezir);
        echo $Pardus->GetNews($_GET["NewsID"]);

    }
    else
        header("location:index.php");

?>
