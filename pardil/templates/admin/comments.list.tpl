#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Önerilere Yapılan Yorumlar</h2>
  <ul>
    <li><strong>Öneri:</strong> $pid</li>
    <li><a href="admin_comments.py">Listeye Dön</a></li>
  </ul>
  <table width="100%">
    <tr>
      <th>Tarih</th>
      <th>Gönderen</th>
      <th>Yorum</th>
      <th>&nbsp;</th>
    </tr>
    #for $i in $comments
    <tr>
      <td>$i.date</td>
      <td>$i.user</td>
      <td><textarea>$i.content</textarea></td>
      <td>[<a href="admin_comments.py?action=delete&amp;pid=$pid&amp;cid=$i.cid">Sil</a>]</td>
    </tr>
    #end for
  </table>
</div>
#include $site_path + "templates/footer.tpl"
