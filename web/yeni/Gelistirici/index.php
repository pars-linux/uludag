<html>
<head>
<?php require_once('../utils.php'); ?>
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

<body onload="ShowPageList();">
<center>

<!-- Content -->

    <?php
        $Pardus = new Pardus($DbHost,$DbUser,$DbPass,$DbData);
    ?>

<table>
    <tr>
        <td id="header">
            <div id="menu"></div>
        </td>
    </tr>
    <tr>
            <td id="gelistirici" colspan=2>
            <div id="gelistiriciContent"></div>
            </td>
    </tr>
    <tr>
            <td id="mainBody">
                <div id="hede">
<!--                 <iframe frameborder="0" height="384px" width="100%" id="main" name="main" src="http://paketler.pardus.org.tr"></iframe> -->
                <h2> Kaynak Kodlar </h2>
                <p> Ürettiğimiz kodlar Subversion sürüm kontrol sisteminde tutulmaktadır.</p>
                <a href="http://svn.pardus.org.tr/uludag">Pardus Deposu</a>: Geliştirdiğimiz projelere ait kodlar<br>
                <a href="http://svn.pardus.org.tr/pardus">Paketler Kaynak Deposu</a>: Pisi paketlerini inşa ederken kullanılan tanım dosyaları ve yamalar.<br>
                <a href="http://svn.pardus.org.tr/projeler">Projeler Deposu</a>: Pardus ile doğrudan bağlantılı olmayan yazılım projeleri.
                <h2> Hata Takip Sistemi </h2>
                <p> Metin...</p>
                <h2> Paket Depoları </h2>
                <p> Derlenmiş paketlere aşağıdaki depolardan ulaşabilirsiniz:</p>
                Pardus 1 Deposu: <a href="http://paketler.pardus.org.tr/pardus-1">paketler</a> <a href="http://paketler.pardus.org.tr/1/">istatistikler</a><br>
                Pardus 1 Test Deposu: <a href="http://paketler.pardus.org.tr/pardus-1-test">paketler</a> <a href="http://paketler.pardus.org.tr/1/">istatistikler</a><br>
                Pardus Geliştirme Deposu: <a href="http://paketler.pardus.org.tr/pardus-devel">paketler</a> <a href="http://paketler.pardus.org.tr/devel/">istatistikler</a><br>
                <h2> İletişim </h2>
                <p>İletişim için temel olarak eposta listelerini kullanıyoruz.<br>
                <a href="http://liste.pardus.org.tr/mailman/listinfo/gelistirici">Geliştirici Listesi</a>: Geliştirme ile ilgili tartışmaların yapıldığı temel listedir. Listeye üye olmak için bir geliştirici hesabınız olmalı ya da davet edilmelisiniz. Liste arşivi herkese açıktır.<br>
                <a href="http://liste.pardus.org.tr/mailman/listinfo/pisi">Pisi Listesi</a>: Pardus'un paket yönetim sistemi Pisi ile ilgili teknik tartışmalar içindir.<br>
                <a href="http://liste.pardus.org.tr/mailman/listinfo/paketler">Paketler Listesi</a>: Pardus içerisinde yeralacak yazılımları belirlemek ve yapmakla ilgili tartışmalar içindir.<br>
                <a href="http://liste.pardus.org.tr/mailman/listinfo/bugzilla">Hata Takip Listesi</a>: Hata takip sistemindeki etkinliklerin takip edilebildiği yüksek trafikli bir listedir.<br>
                <a href="http://liste.pardus.org.tr/mailman/listinfo/uludag-commits">Kod Takip Listesi</a>: Pardus kaynak kod deposundaki değişikliklerin otomatik olarak gönderildiği yüksek trafikli bir listedir.<br>
                <a href="http://liste.pardus.org.tr/mailman/listinfo/paketler-commits">Paketler Takip Listesi</a>: Pardus paketler kaynak deposundaki değişikliklerin otomatik olarak gönderildiği yüksek trafikli bir listedir.<br>

                <h2> Hızlı İletişim </h2>
                <p> Belgelenmesi önemli olmayan tartışmalar ve daha hızlı iletişim için irc.freenode.org üzerindeki #pardus-devel IRC kanalını ve jabber.uludag.org.tr üzerinde çalışmakta olan Jabber sunucumuzu kullanabilirsiniz.</p>
                </div>
            </td>
            <td id="kucular">

            </td>
    </tr>
    <tr>
        <td colspan=2 id="footer">
            Pardus TUBITAK/UEKAE 'nin Tescilli Markasıdır.
        </td>
    </tr>
 </table>

</center>
</body>
</html>
