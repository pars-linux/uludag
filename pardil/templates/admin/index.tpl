#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Site Yönetimi</h2>
  <ul>
    <li><a href="admin_groups.py">Gruplar</a></li>
    <li><a href="admin_rights.py">Erişim Kodları</a></li>
  </ul>
  <ul>
    <li><a href="admin_usergroups.py">Kullanıcı Grupları</a></li>
    <li><a href="admin_userrights.py">Erişim Hakları</a></li>
    <li><a href="admin_maintainers.py">Bildiri Sorumluları</a></li>
  </ul>
  <ul>
    <li><a href="admin_p_proposals.py">Onay Bekleyen Bildiriler</a></li>
    <!--
    <li><a href="admin_proposals.py">Tüm Bildiriler</a></li>
    -->
  </ul>
  <ul>
    <li><a href="admin_comments.py">Yorumlar</a></li>
  </ul>
  <ul>
    <li><a href="admin_news.py">Haberler</a></li>
  </ul>
</div>
#include $site_path + "templates/footer.tpl"
