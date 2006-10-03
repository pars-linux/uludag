#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Erişim Kodları</h2>
  <p>
    Eğer bir erişim kodunu silerseniz, kod ile ilişkili uygulamalar çalışmayabilir.<br/>
    $rid numaralı "$label" erişim kodunu silmek istediğinizden emin misiniz?
  </p>
  <ul>
    <li><a href="admin_rights.py?action=delete&amp;rid=$rid&amp;confirm=no&amp;start=$pag_now">Hayır</a></li>
    <li><a href="admin_rights.py?action=delete&amp;rid=$rid&amp;confirm=yes&amp;start=$pag_now">Evet</a></li>
  </ul>
</div>
#include $site_path + "templates/footer.tpl"
