#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Erişim Kodları</h2>
  <p>
    Eğer bir erişim kodunu silerseniz, kod ile ilişkili uygulamalar çalışmayabilir.<br/>
    $rid numaralı "$label" erişim kodunu silmek istediğinizden emin misiniz?
  </p>
  <ul>
    <li><a href="admin_rights.py?action=delete&amp;delete=$rid&amp;confirm=no">Hayır</a></li>
    <li><a href="admin_rights.py?action=delete&amp;delete=$rid&amp;confirm=yes">Evet</a></li>
  </ul>
</div>
#include $site_path + "templates/footer.tpl"
