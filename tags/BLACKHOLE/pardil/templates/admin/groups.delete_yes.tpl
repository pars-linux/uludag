#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Gruplar</h2>
  <p>
    $gid numaralı "$label" grubu silindi.<br/>
    Grup ile ilişkili tüm erişim hakları kaldırıldı.
  </p>
  <ul>
    <li><a href="admin_groups.py?start=$pag_now">Listeye Dön</a></li>
  </ul>
</div>
#include $site_path + "templates/footer.tpl"
