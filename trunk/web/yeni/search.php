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
        <?php
            if (isset($_GET["r"])) {
                        $Pardus = new Pardus($DbHost,$DbUser,$DbPass,$DbData);
                        $Res = $Pardus->GetPage(htmlspecialchars($_GET["r"]));
            }
            $SearchWord = htmlspecialchars(strip_tags(trim($_GET["q"]))); 
        ?>
                <a href="index.php">Ana Sayfa</a> » 
                    <?if($Res<>""){?>
                        <a href="?q=<?=$SearchWord?>"><?="'".$SearchWord."'"?> için arama sonuçları</a> » <?=$Res["Title"]?>
                    <?} else {?>
                        <?="'".$SearchWord."'"?> için arama sonuçları
                    <? } ?>
                </b>
            </div>
        </td>
    </tr>

    <tr>
        <td id="mainBody" style="width:770px" colspan=2>
            <div id="hede">
                <?php
                    if (isset($_GET["r"])) {
                        $Pardus = new Pardus($DbHost,$DbUser,$DbPass,$DbData);
                        $Res = $Pardus->GetPage(htmlspecialchars($_GET["r"]));
                        echo GetHighlighted($SearchWord,$Res["Content"],"#F5FF9A");
                    }
                    else {
                ?>
                <center>
                    <br />
                    <form action="?">
                        <input type="text" name="q" size=55 value="<?=$SearchWord?>">&nbsp;<input type="submit" value="yeniden ara">
                    </form>
                </center>
                <?php

                    if (isset($_GET["q"])) {
                        if (strlen($SearchWord)>3) {
                            $Pardus = new Pardus($DbHost,$DbUser,$DbPass,$DbData);
                            $Results = $Pardus->Search($SearchWord);
                            if ($Results[0]['NiceTitle']<>"") echo "Toplam ".sizeof($Results)." kayıt bulundu.Ayrıca <a href='http://www.google.com.tr/search?ie=UTF-8&q=$SearchWord' target='_blank'>Google sonuçları</a>na da göz atabilirsiniz.<br>";
                            else echo "Hiçbir kayıda rastlanmadı, daha fazla kelime ile aramayı ya da <a href='http://www.google.com.tr/search?ie=UTF-8&q=$SearchWord' target='_blank'>Google sonuçları</a>na göz atmayı deneyebilirsiniz.";
                            echo "<hr>";
                            if ($Results) {
                                foreach ($Results as $Values)
                                echo "<b><a href='?r=".$Values['NiceTitle']."&q=".$SearchWord."'>".$Values['Title']."</a></b><p class='searchresults'>".Highlight($Values['Content'],$SearchWord)."...</p>";
                            }
                        }
                        else
                            echo "Arama kelimesi en az 4 (dört) karakter olmalıdır.";
                    }
                }
                $Pardus->Disconnect();
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
