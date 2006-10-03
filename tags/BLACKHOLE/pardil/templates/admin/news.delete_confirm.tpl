#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Haberler</h2>
  <p>
    $nid numaralı "$title" haberini silmek istediğinizden emin misiniz?
  </p>
  <ul>
    <li><a href="admin_news.py?action=delete&amp;nid=$nid&amp;confirm=no&amp;start=$pag_now">Hayır</a></li>
    <li><a href="admin_news.py?action=delete&amp;nid=$nid&amp;confirm=yes&amp;start=$pag_now">Evet</a></li>
  </ul>
</div>
#include $site_path + "templates/footer.tpl"
