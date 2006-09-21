<?php

    // TUBITAK/UEAKE - 2006-07 - Pardus
    // Gökmen GÖKSEL <gokmen@pardus.org.tr>
    // Pardus Web..

    require_once('config.php');
    require_once('vezir.php');
    require_once('langs/tr.php');
    require_once('Modules/Main.php');

?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
         "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="tr" xml:lang="tr">
<head>
    <title><?=PAGE_TITLE?></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link href="style.css" rel="stylesheet" type="text/css" />
    <script src="scripts/prototype.js" type="text/javascript"></script>
    <script src="scripts/scriptaculous.js" type="text/javascript"></script>
    <script src="scripts/main.js" type="text/javascript"></script>
    <?=$Modules['Head']?>
</head>
<body onload='<?=$Modules['Onload']?>' >
    <div id="container">
    <div id="head_grey">
        <div id="blue"></div>
        <div id="quick_download">
            <img src="images/box-hizli-indir.png" alt="Pardus 1.1Beta"/>
            <form action="search/">
                <input type="text" name="q" id="search" value="<?=SEARCH?>" onclick="Javascript:if (this.value=='<?=SEARCH?>') this.value='';" onblur="Javascript:if (this.value=='') this.value='<?=SEARCH?>';"/>
            </form>
            <div id="menu"><img src="images/menu-blue.png" /></div>
        </div>
    </div>
            <?php
                if(isset($Page)){
                    echo "<div>";
                    echo "<p>".$Page[0]["Content"]."</p>";
                    #if ($Modules<>"")
                    #    echo "\n<td id='kucular'>".$Modules['Body']."</td>";
                    echo "</div>";
                }
                else
                    include ('index_.php');
            ?>

    <div id="footnote"><p><?=PARDUS_REGISTER?></p></div>
</div>
</body>
</html>
