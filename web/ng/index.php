<?php

    // TUBITAK/UEAKE - 2006-07 - Pardus
    // Gökmen GÖKSEL <gokmen@pardus.org.tr>
    // Pardus Web..

    require_once('config.php');
    require_once('vezir.php');

    $Vezir  = new Vezir($CF);
    $Pardus = new Pardus($Vezir);

?>

<html>
<head>
    <title><?=PAGE_TITLE?></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link href="stil.css" rel="stylesheet" type="text/css" />
    <script src="scripts/prototype.js"></script>
    <script src="scripts/scriptaculous.js"></script>
    <script src="scripts/effects.js"></script>
    <script src="scripts/main.js"></script>
</head>

<body>
    <center>
        <table>
            <tr>
                <td id="header" colspan=2>
                    <span id="searchbar">
                        <form action="search/" method="get">
                            <input name="q" type="text" value="<?=SEARCH?>"
                            onClick="
                                if (this.value=='<?=SEARCH?>')
                                    this.value='';" 
                            onBlur="
                                if (this.value=='') 
                                    this.value='<?=SEARCH?>';">
                        </form>
                    </span>
                </td>
            </tr>

            <?php
                if(isset($_GET["page"]))
                    echo "page will come...";
                else
                    include ('index-data.php');
            ?>
            <tr>
                <td colspan=2>
                    <div id="footer-forpw">
                    <?php $Vezir->ShowLogs(); ?>
                    <?=PARDUS_REGISTER?></div>
                </td>
            </tr>
        </table>
    </center>
</body>
</html>
