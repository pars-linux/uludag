#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Önerilere Yapılan Yorumlar</h2>
  <ul>
    <li><strong>Öneri:</strong> $pid</li>
    <li><a href="admin_comments.py?start=$pag_now">Listeye Dön</a></li>
  </ul>
  <table width="100%">
    <tr>
      <th>Tarih</th>
      <th>Gönderen</th>
      <th>Yorum</th>
      <th width="30">&nbsp;</th>
    </tr>
    #for $c, $i in enumerate($comments)
      #if $c % 2
      <tr class="odd">
      #else
      <tr class="even">
      #end if
      <td>$i.date</td>
      <td>$i.user</td>
      <td><textarea>$i.content</textarea></td>
      <td>[<a href="admin_comments.py?action=delete&amp;pid=$pid&amp;cid=$i.cid&amp;start=$pag_now">Sil</a>]</td>
    </tr>
    #end for
  </table>
</div>
#include $site_path + "templates/footer.tpl"
