#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Öneri Sorumluları</h2>
    <p>
      $user isimli kullanıcının $pid numaralı öneri üzerindeki sorumluluğu kaldırılsın mı?
    </p>
    <ul>
      <li><a href="admin_maintainers.py?action=delete&amp;relid=$relid&amp;confirm=no">Hayır</a></li>
      <li><a href="admin_maintainers.py?action=delete&amp;relid=$relid&amp;confirm=yes">Evet</a></li>
    </ul>
</div>
#include $site_path + "templates/footer.tpl"
