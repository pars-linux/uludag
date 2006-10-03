#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Erişim Hakları</h2>
  <p>
    $relid numaralı "$group - $right" erişimini silmek istediğinizden emin misiniz?
  </p>
  <ul>
    <li><a href="admin_userrights.py?action=delete&amp;relid=$relid&amp;confirm=no&amp;start=$pag_now">Hayır</a></li>
    <li><a href="admin_userrights.py?action=delete&amp;relid=$relid&amp;confirm=yes&amp;start=$pag_now">Evet</a></li>
  </ul>
</div>
#include $site_path + "templates/footer.tpl"
