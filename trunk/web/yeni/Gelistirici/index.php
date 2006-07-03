<html>
<head>
<?php

    $ActivePage = "G";

    require_once('../Modules/Main.php');
    require_once('../Modules/RSS.php');

    $Blogs = new RssRead($BlogRssLink);

?>

    <title>PardusOrgTr</title>
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
                    echo "<a href='?'>Geliştiriciler</a> » ";
                    if ($Parent)
                        echo "<a href='?".$ParentContent["NiceTitle"]."'>".$ParentContent["Title"]."</a> » ";
                     echo $PageContent["Title"];
               }
                else
                    echo "Geliştiriciler";
            ?>
            </b></div>
        </td>
        <td>
            <img src="../images/newdesign/head-gelistirici.png" style="float:right;padding-right:5px;" />
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
                <div id="RssList">
                <b>Nasıl Katkıda Bulunabilirim?</b>
                <p>
                <li>Wiki'de deneyimlerinizi paylaşabileceğiniz belgelerle yeni kullanıcılara yardım edebilir;
                <li>Yaşadığınız sorunları ya da önerilerinizi Hata Takip Sistemine girerek daha iyi bir sistem yaratmamıza yardımcı olabilir;
                <li>İmece çalışmalarına katılarak, katkılarınızı doğrudan Pardus'a ekleyebilir;
                <li>Bunlar dışında fikirleriniz varsa Pardus Gönüllülerine başvurabilirsiniz...
                </p>
                </div>
                <img src="../images/newdesign/head-svn-degisiklik.png">
                <img src="../images/newdesign/head-bugzilla-degisiklik.png">
                <img src="../images/newdesign/head-gelistirici-gunlukler.png">
                    <div id="RssList">
                    <?php
                        $Blogs->ShowList(4,30);
                    ?>
                    </div>
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
