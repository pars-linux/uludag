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
                <center>
                    <br />
                    <form action="?">
                        <input type="text" name="q" size=55>&nbsp;<input type="submit" value="yeniden ara">
                    </form>
                </center>
                <?php

                if (isset($_GET["q"])) {
                    $SearchWord = htmlspecialchars(strip_tags($_GET["q"]));
                    if (strlen($SearchWord)>3) {
                        $Pardus = new Pardus($DbHost,$DbUser,$DbPass,$DbData);
                        $Results = $Pardus->Search($_GET["q"]);
                        if ($Results[0]['NiceTitle']<>"") echo "Toplam ".sizeof($Results)." kayıt bulundu.Ayrıca <a href='http://www.google.com.tr/search?ie=UTF-8&q=$SearchWord' target='_blank'>Google sonuçları</a>na da göz atabilirsiniz.<br>";
                        else echo "Hiçbir kayıda rastlanmadı, daha fazla kelime ile aramayı ya da <a href='http://www.google.com.tr/search?ie=UTF-8&q=$SearchWord' target='_blank'>Google sonuçları</a>na göz atmayı deneyebilirsiniz.";
                        echo "<hr>";
                        if ($Results) {
                            foreach ($Results as $Values)
                                echo "<b><a href='?".$Values['NiceTitle']."'>".$Values['Title']."</a></b><p class='searchresults'>".Highlight($Values['Content'],$_GET['q'],$Values['Score'])."...</p>";
                        }
                    }
                    else
                        echo "Arama kelimesi en az 4 (dört) karakter olmalıdır.";
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
