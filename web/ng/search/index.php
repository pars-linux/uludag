
    <form action="<?$PHP_SELF?>" method="GET">
        <input type="text" name="q" size=100>
        <input type="submit" name="search" value="search">
    </form>

<?php

    // TUBITAK/UEAKE - 2006-07 - Pardus
    // Gökmen GÖKSEL <gokmen@pardus.org.tr>
    // Search in Pardus DataBase

    include_once '../config.php';
    include_once '../vezir.php';
    include_once 'search.php';

    $Vezir  = new Vezir($CF);
    $Pardus = new Pardus($Vezir);

    if (isset($_GET["q"])) {
        $SearchWord = $_GET["q"];
        $Results = $Pardus->Search($SearchWord);
        $Vezir->ShowLogs();
        $Search = new Sud($Results,$SearchWord);
        $Search->Mod1();
    }

?>
