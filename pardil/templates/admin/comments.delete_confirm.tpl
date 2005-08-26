#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Yorumlar</h2>
  <p>
    "$username" isimli kullanıcının gönderdiği $cid numaralı silmek istediğinizden emin misiniz?
  </p>
  <ul>
    <li><a href="admin_comments.py?action=delete&amp;pid=$pid&amp;cid=$cid&amp;confirm=no">Hayır</a></li>
    <li><a href="admin_comments.py?action=delete&amp;pid=$pid&amp;cid=$cid&amp;confirm=yes">Evet</a></li>
  </ul>
</div>
#include $site_path + "templates/footer.tpl"
