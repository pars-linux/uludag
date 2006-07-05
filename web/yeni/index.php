<html>
<head>

<?php
    
    $ActivePage = "M";
    require_once('utils.php');
    require_once('Modules/Main.php');
    require_once('Modules/RSS.php');

    $Blogs = new RssRead($BlogRssLink);

?>

    <title><?=$PageTitle?></title>
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
<table>

<?php if($Page==="Main") { ?>

    <tr>
        <td id="header" colspan=2>
            <div id="menu"><span id="searchbar"><input type="text" value="ara"></span> </div>
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
                Pardus, TUBITAK UEKAE tarafından yürütülen, kodları ve geliştirme süreçleri açık, herkesin katılabileceği, özgür yazılım modeliyle geliştirilen bir işletim sistemidir. Kolay kullanılır ve bir bilişim okuryazarının tüm ihtiyaçlarını doğrudan karşılar.<br>Pardus ile ilgili ayrıntılı bilgi için <a href="?Bireysel/PardusTanitim">tıklayınız</a>.
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

<?php } else { ?>

    <tr>
        <td id="header">
            <div id="menu">
                <b>
                <a href="?">Ana Sayfa</a> »
            <?php
                if($Page<>"Main"){
                    if ($Parent)
                        echo "<a href='?".$ParentContent["NiceTitle"]."'>".$ParentContent["Title"]."</a> » ";
                     echo $PageContent["Title"];
               }
            ?>
                </b>
            </div>
        </td>
        <td>
            <!-- <img src="../images/newdesign/head-pardus.png" style="float:right;padding-right:5px;" /> -->
        </td>
    </tr>
    
    <tr>
        <td id="mainBody" <?php if ($PageContent["PType"]==="D") { ?> style="width:770px" colspan=2 <?php } ?> >
            <div id="hede">
                <?=$PageContent["Content"]?>
            </div>
        </td>
        <?php if ($PageContent["PType"]<>"D") { ?>
        <td id="kucular">
            <div id="hodo">
                <img src="images/newdesign/head-nasil-katkida-bulunabilirim.png">
                <div id="RssList">
                    <li>Wiki'de deneyimlerinizi paylaşabileceğiniz belgelerle yeni kullanıcılara yardım edebilir;
                    <li>Yaşadığınız sorunları ya da önerilerinizi Hata Takip Sistemine girerek daha iyi bir sistem yaratmamıza yardımcı olabilir;
                    <li>İmece çalışmalarına katılarak, katkılarınızı doğrudan Pardus'a ekleyebilir;
                    <li>Bunlar dışında fikirleriniz varsa Pardus Gönüllülerine başvurabilirsiniz...
                </div>
                <img src="images/newdesign/head-bugzilla-degisiklik.png">
                <img src="images/newdesign/head-gelistirici-gunlukler.png">
                <div id="RssList">
                <?php
                    $Blogs->ShowList(4,30);
                ?>
                </div>
                <img src="images/newdesign/dock-gelistirici.png">
            </div>
        </td>
        <?php } ?>
    </tr>

<?php } ?>
    
    <tr>
        <td colspan=2>
            <div id="footer-forpw">Pardus TUBITAK/UEKAE 'nin Tescilli Markasıdır.</div>
        </td>
    </tr>
 </table>

</center>
</body>
</html>
