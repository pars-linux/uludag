#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Haberler</h2>
  <p>
    $nid numaralı "$title" haberi silindi.
  </p>
  <ul>
    <li><a href="admin_news.py?start=$pag_now">Listeye Dön</a></li>
  </ul>
</div>
#include $site_path + "templates/footer.tpl"
