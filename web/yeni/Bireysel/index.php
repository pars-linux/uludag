<html>
<head>
<?php

    $ActivePage = "B";

    require_once('../utils.php');
    require_once('../Modules/Main.php');
    require_once('../Modules/RSS.php');

    $Blogs = new RssRead($BlogRssLink);

?>

    <title><?=$PageTitle?> » Bireysel</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link href="../stil.css" rel="stylesheet" type="text/css">
    <script src="../scripts/prototype.js"></script>
    <script>

        function get_news(nid) {
            var url ='utils.php';
            var linke = 'NewsID='+nid;
            var AjaxPointer = new Ajax.Request(url,{method:'get', parameters: linke, onComplete: showit});
        }

        function showit(originalRequest){
            var newData = originalRequest.responseText;
            $('ayrintilar').innerHTML = "";
            $('ayrintilar').innerHTML = newData;
        }

        function ShowPageList(){
            var ajax = new Ajax.Updater(
                'hede',
                'http://www.pardus.org.tr',
                {
                    method:'get',
                    onComplete: showPlain
                }
            );
        }

        function showPlain(req)
        {
            $('hede').innerHTML = req.responseText;
        }

    </script>
</head>

<body>
<center>

<!-- Content -->
<table>
    <tr>
        <td id="header">
            <div id="menu"><b><a href="../">Ana Sayfa</a> »
            <?php
                if($Page<>"Main"){
                    echo "<a href='?'>Bireysel</a> » ";
                    if ($Parent)
                        echo "<a href='?".$ParentContent["NiceTitle"]."'>".$ParentContent["Title"]."</a> » ";
                     echo $PageContent["Title"];
               }
                else
                    echo "Bireysel";
            ?>
            </b></div>
        </td>
        <td>
            <img src="../images/newdesign/head-bireysel.png" style="float:right;padding-right:5px;" />
        </td>
    </tr>
    <tr>
        <td <?php if ($PageContent["PType"]==="D") { ?> id="docTable" colspan=2 <?php } else { ?> id="mainBody" <? } ?> >
            <div id="hede">
                <?=$PageContent["Content"]?>
            </div>
        </td>
        <?php if ($PageContent["PType"]<>"D") { ?>
        <td id="kucular">
            <div id="hodo">
                <img src="../images/newdesign/head-hizli-baslangic.png">
		<div id="RssList">
			Masaüstü ihtiyaçlarınız için tam bir çözüm öneren Pardus ile hangi işlemi nasıl yapabileceğinize dair pratik bilgiler
		</div>
                <img src="../images/newdesign/head-donanim-uyumlulugu.png">
		<div id="RssList">
			"Benim bilgisayarımda çalışır mı?", "Fotoğraf makinamı görür mü?" gibi sorularınız için Donanım Uyumluluğu sistemimizi kullanabilirsiniz.
		</div>
                <img src="../images/newdesign/head-pardus-ekran-goruntuleri.png">
                <img src="../images/newdesign/dock-gelistirici.png">
            </div>
        </td>
        <?php } ?>
    </tr>
    <tr>
        <td colspan=2 id="footer-forpw">
            Pardus TUBITAK/UEKAE 'nin Tescilli Markasıdır.
        </td>
    </tr>
 </table>

</center>
</body>
</html>
