<?php

    // TUBITAK/UEAKE - 2006-07 - Pardus
    // Gökmen GÖKSEL <gokmen@pardus.org.tr>
    // Pardus Web..

    require_once('config.php');
    require_once('vezir.php');
    require_once('langs/tr.php');
    require_once('Modules/Main.php');

?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//TR"
         "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="tr" xml:lang="en">
<head>
    <title><?=PAGE_TITLE?></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link href="stil.css" rel="stylesheet" type="text/css" />
    <script src="scripts/prototype.js" type="text/javascript"></script>
    <script src="scripts/scriptaculous.js" type="text/javascript"></script>
    <script src="scripts/main.js" type="text/javascript"></script>
    <?=$Modules['Head']?>
</head>
<body onLoad='<?=$Modules['Onload']?>' >
        <table id="como">
            <tr>
                <td id="header" colspan=3>
                    <div id="menu"><?=$Navi?></div>
                    <div id="searchbar">
                        <form action="search/" method="get">
                        <input name="q" type="text" value="<?=SEARCH?>" onclick="javascript:if (this.value=='<?=SEARCH?>') this.value=''" onblur="javascript:if (this.value=='') this.value='<?=SEARCH?>'" />
                        </form>
                    </div>
                </td>
            </tr>

            <?php
                if(isset($Page)){
                    echo "<tr>";
                    echo "<td id='mainBody'>".$Page[0]["Content"]."</td>";
                    if ($Modules<>"")
                        echo "\n<td id='kucular'>".$Modules['Body']."</td>";
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
</body>
</html>
