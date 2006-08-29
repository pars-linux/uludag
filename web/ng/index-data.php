    <tr>
        <td id="pardus-11">
            <div id="boxdetay1">
                Pardus 1.1 Muhteşem :)
            </div>
        </td>
        <td id="kutular">
            <div id="pardus-nedir">
                Pardus, TUBITAK UEKAE tarafından yürütülen, kodları ve geliştirme süreçleri açık, herkesin katılabileceği, özgür yazılım modeliyle geliştirilen bir işletim sistemidir. Kolay kullanılır ve bir bilişim okuryazarının tüm ihtiyaçlarını doğrudan karşılar.<br>Pardus ile ilgili ayrıntılı bilgi için <a href="?PardusTanitim">tıklayınız</a>.
            </div>
            <div id="pardus-indir"></div>
        </td>
    </tr>

    <tr>
        <td id="navi" colspan=2>
            <div id="ana-butonlar">
                <a href="?page=Bireysel"><img src="images/newdesign/button-bireysel-kullanici.png" border="0" alt="" /></a>
                <a href="?page=Kurumsal"><img src="images/newdesign/button-kurumsal-kullanici.png" border="0" alt="" /></a>
                <a href="?page=Gelistirici"><img src="images/newdesign/button-gelistirici.png" border="0" alt="" /></a>
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

