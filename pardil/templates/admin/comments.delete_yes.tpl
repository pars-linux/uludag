#include $site_path + "templates/header.tpl"
<div id="content">
  <p>
    "$username" isimli kullanıcının gönderdiği $cid numaralı yorum silindi.<br/>
  </p>
  <ul>
    <li><a href="admin_comments.py?action=comments&amp;pid=$pid&amp;start=$pag_now">Listeye Dön</a></li>
  </ul>
</div>
#include $site_path + "templates/footer.tpl"
