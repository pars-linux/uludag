<html>
<head>
<?php

        @require_once('utils.php');
        if (!($Pardus = new Pardus($DbHost,$DbUser,$DbPass,$DbData)))
            die();

?>
    <title>PardusOrgTr</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link href="stil.css" rel="stylesheet" type="text/css">
    <script src="scripts/prototype.js"></script>
    <script src="scripts/scriptaculous.js"></script>
    <script src="scripts/effects.js"></script>
    <script>
        function get_news(nid) {
            var url ='utils.php';
            var linke = 'NewsID='+nid;
            var AjaxPointer = new Ajax.Request(url,{method:'get', parameters: linke, onComplete: showit});
        }

        function showit(originalRequest){
            var newData = originalRequest.responseText;
            $('haber').innerHTML = "";
            $('haber').innerHTML = newData;
            new Effect.Highlight('haber',{startcolor:'#CCE0E6', endcolor:'#FFFFFF'});
            $('haber').style.background = "#FFF";
        }
    </script>
</head>

<body>
<center>

<!-- Content -->

    <?php
    ?>

<table>
    <tr>
        <td id="header">
            <div id="menu">  </div>
        </td>
    </tr>
    <tr>
            <td id="pardus-11">
                <div id="boxdetay1">
                Pardus 1.1 Muhteşem :)
                </div>
            </td>
            <td id="kutular">
                    <div id="pardus-nedir">
                    Pardus, TUBITAK UEKAE tarafından yürütülen, kodları ve geliştirme süreçleri açık, herkesin katılabileceği, özgür yazılım modeliyle geliştirilen bir işletim sistemidir. Kolay kullanılır ve bir bilişim okuryazarının tüm ihtiyaçlarını doğrudan karşılar.
                    <br>
                    Pardus ile ilgili ayrıntılı bilgi için <a href="/Bireysel/PardusTanitim">tıklayınız</a>.
                    </div>
                    <div id="pardus-indir"></div>
            </td>
    </tr>

    <tr>
            <td id="navi" colspan=2>
            <div id="ana-butonlar">
                <a href="Bireysel"><img src="images/newdesign/button-bireysel-kullanici.png" border="0" alt="" /></a>
                <a href="Kurumsal"><img src="images/newdesign/button-kurumsal-kullanici.png" border="0" alt="" /></a>
                <a href="Gelistirici"><img src="images/newdesign/button-gelistirici.png" border="0" alt="" /></a>
            </div>
            </td>
    </tr>

    <tr>
            <td id="icerik">
            <div id="ayrintilar">
            <div id="haber">
            <?php
                    $Pardus->GetNews();
            ?>
            </div>
            </div>
            </td>
            <td id="kutular">
            <div id="haberler">
                <?php
                    $Pardus->GetNewsList();
                ?>
            </div>
            </td>
    </tr>
    <tr>
        <td colspan=2>
            <div id="footer">Pardus TUBITAK/UEKAE 'nin Tescilli Markasıdır.</div>
        </td>
    </tr>
 </table>

</center>
</body>
</html>
