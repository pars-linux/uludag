<?php

    # Search Module for PW
    # Gökmen GÖKSEL <gokmen _at pardus.org.tr>

    include_once 'utils.php';

?>

<html>
<head>
    <title><?=$PageTitle?></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link href="stil.css" rel="stylesheet" type="text/css">
</head>

<body>
<center>
<table>
    <tr>
        <td id="header">
            <div id="menu">
                <b>
                <a href="index.php">Ana Sayfa</a> » <?php echo "'".htmlspecialchars($_GET["q"])."'";?> için arama sonuçları
                </b>
            </div>
        </td>
    </tr>

    <tr>
        <td id="mainBody" style="width:770px" colspan=2>
            <div id="hede">
                <?php

                if (isset($_GET["q"])) {
                    $Pardus = new Pardus($DbHost,$DbUser,$DbPass,$DbData);
                    $Results = $Pardus->Search($_GET["q"]);
                    $i=0;
                    if ($Results) {
                        foreach ($Results as $Values) {
                            echo "<h2>".$Values['Title']."</h2>".Highlight($Values['Content'],$_GET['q'],$Values['Score'],40)."...";
                        }
                    }
                }

                ?>
            </div>
        </td>
    </tr>

    <tr>
        <td colspan=2>
            <div id="footer-forpw">Pardus TUBITAK/UEKAE 'nin Tescilli Markasıdır.</div>
        </td>
    </tr>
 </table>

</center>
</body>
</html>
