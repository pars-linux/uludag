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


