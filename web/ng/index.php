<?php

    // TUBITAK/UEAKE - 2006-07 - Pardus
    // Gökmen GÖKSEL <gokmen@pardus.org.tr>
    // Pardus Web..

    require_once('config.php');
    require_once('vezir.php');
    require_once('langs/tr.php');
    require_once('Modules/Main.php');

?>
<!DOCTYPE html
     PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
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

    <?php
        if(isset($Page)){
            include_once('index__.php');
            echo "<div id='fullpage'>";
            if ($Modules<>""){
                echo "\n<div class='moduleser'>".$Modules['Body']."</div>";
            }
            echo $Page[0]["Content"];
            echo "</div>";
            echo "</div>";
        }
        else
            include ('index_.php');
    ?>

    <div id="footnote"><p><?=PARDUS_REGISTER?></p></div>
</div>
<?php $Vezir->ShowLogs();?>
</body>
</html>
