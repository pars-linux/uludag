    <tr>
        <td id="pardus-11" colspan="2">
           <!-- <div id="boxdetay1">
                Pardus 1.1 Muhteşem :)
            </div>
            -->
        </td>
        <td class="kutular">
            <div id="pardus-nedir">
                Pardus, TUBITAK UEKAE tarafından yürütülen, kodları ve geliştirme süreçleri açık, herkesin katılabileceği, özgür yazılım modeliyle geliştirilen bir işletim sistemidir. Kolay kullanılır ve bir bilişim okuryazarının tüm ihtiyaçlarını doğrudan karşılar.<br />Pardus ile ilgili ayrıntılı bilgi için <a href="?PardusTanitim">tıklayınız</a>.
            </div>
            <div id="pardus-indir"></div>
        </td>
    </tr>

    <tr id="main-buttons">
        <td><a href="?page=Bireysel"><img src="images/newdesign/button-bireysel-kullanici.png" alt="Bireysel Kullanıcı" /></a></td>
        <td><a href="?page=Kurumsal"><img src="images/newdesign/button-kurumsal-kullanici.png" alt="Kurumsal Kullanıcı" /></a></td>
        <td><a href="?page=Gelistirici"><img src="images/newdesign/button-gelistirici.png" alt="Geliştirici" /></a></td>
    </tr>

    <tr>
        <td id="icerik" colspan="2">
            <div id="ayrintilar">
                <div id="haber">
                <?php
                    $Pardus->GetNews();
                ?>
                </div>
            </div>
        </td>
        <td class="kutular">
            <div id="haberler">
                <?php
                    $Pardus->GetNewsList();
                ?>
            </div>
        </td>
    </tr>

