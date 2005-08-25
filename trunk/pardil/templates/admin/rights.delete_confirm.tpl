#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Erişim Hakları</h2>
  <p>
    $relid numaralı "$group - $right" erişimini silmek istediğinizden emin misiniz?
  </p>
  <ul>
    <li><a href="admin_rights.py?action=delete&amp;delete=$relid&amp;confirm=no">Hayır</a></li>
    <li><a href="admin_rights.py?action=delete&amp;delete=$relid&amp;confirm=yes">Evet</a></li>
  </ul>
</div>
#include $site_path + "templates/footer.tpl"
