#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Kullanıcı Grupları</h2>
    <p>
      $user isimli kullanıcı $group grubundan çıkarılsın mı?
    </p>
    <ul>
      <li><a href="admin_usergroups.py?action=delete&amp;delete=$relid&amp;confirm=no">Hayır</a></li>
      <li><a href="admin_usergroups.py?action=delete&amp;delete=$relid&amp;confirm=yes">Evet</a></li>
    </ul>
</div>
#include $site_path + "templates/footer.tpl"
