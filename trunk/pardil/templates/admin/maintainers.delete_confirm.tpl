#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Bildiri Sorumluları</h2>
    <p>
      $user isimli kullanıcının $pid numaralı bildiri üzerindeki sorumluluğu kaldırılsın mı?
    </p>
    <ul>
      <li><a href="admin_maintainers.py?action=delete&amp;relid=$relid&amp;confirm=no&amp;start=$pag_now">Hayır</a></li>
      <li><a href="admin_maintainers.py?action=delete&amp;relid=$relid&amp;confirm=yes&amp;start=$pag_now">Evet</a></li>
    </ul>
</div>
#include $site_path + "templates/footer.tpl"
