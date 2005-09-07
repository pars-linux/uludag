#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Gruplar</h2>
  <p>
    Eğer bir grubu silerseniz, grup ile ilişkili tüm erişim hakları da silinir.<br/>
    $gid numaralı "$label" grubunu silmek istediğinizden emin misiniz?
  </p>
  <ul>
    <li><a href="admin_groups.py?action=delete&amp;gid=$gid&amp;confirm=no&amp;start=$pag_now">Hayır</a></li>
    <li><a href="admin_groups.py?action=delete&amp;gid=$gid&amp;confirm=yes&amp;start=$pag_now">Evet</a></li>
  </ul>
</div>
#include $site_path + "templates/footer.tpl"
