#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Yorumlar</h2>
  <p>
    "$username" isimli kullanıcının gönderdiği $cid numaralı yorumu silmek istediğinizden emin misiniz?
  </p>
  <ul>
    <li><a href="admin_comments.py?action=delete&amp;pid=$pid&amp;cid=$cid&amp;confirm=no&amp;start=$pag_now">Hayır</a></li>
    <li><a href="admin_comments.py?action=delete&amp;pid=$pid&amp;cid=$cid&amp;confirm=yes&amp;start=$pag_now">Evet</a></li>
  </ul>
</div>
#include $site_path + "templates/footer.tpl"
