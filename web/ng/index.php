<?php

    // TUBITAK/UEAKE - 2006-07 - Pardus
    // Gökmen GÖKSEL <gokmen@pardus.org.tr>
    // Pardus Web..

    require_once('config.php');
    require_once('vezir.php');
    require_once('langs/tr.php');
    require_once('Modules/Main.php');

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
    <?=$Modules['Head']?>
</head>
<body onLoad='<?=$Modules['Onload']?>' >
    <center>
        <table id="como">
            <tr>
                <td id="header" colspan=3>
                    <div id="menu"><?=$Navi?></div>
                    <div id="searchbar">
                        <form action="search/" method="get">
                        <input name="q" type="text" value="<?=SEARCH?>"
                               onClick="if (this.value=='<?=SEARCH?>') this.value='';" 
                               onBlur="if (this.value=='') this.value='<?=SEARCH?>';">
                        </form>
                    </div>
                </td>
            </tr>

            <?php
                if(isset($Page)){
                    echo "<tr>";
                    echo "<td id='mainBody'>".$Page[0]["Content"]."</td>";
                    if ($Modules<>"")
                        echo "\n<td id='kucular'><div id='right_pane'>".$Modules['Body']."</div></td>";
                    echo "</tr>";
                }
                else
                    include ('index-data.php');
            ?>

            <tr>
                <td colspan=3>
                    <div id="footer-forpw">
                    <?php $Vezir->ShowLogs(); ?>
                    <?=PARDUS_REGISTER?></div>
                </td>
            </tr>
        </table>
    </center>
</body>
</html>
