#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Bildiri Sorumluları</h2>
    <p>
      $user isimli kullanıcı artık $pid numaralı bildirinin sorumlusu değil.
    </p>
    <ul>
      <li><a href="admin_maintainers.py&amp;start=$pag_now">Listeye Dön</a></li>
    </ul>
</div>
#include $site_path + "templates/footer.tpl"
