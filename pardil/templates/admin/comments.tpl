#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Önerilere Yapılan Yorumlar</h2>
  <table>
    <tr>
      <th>No</th>
      <th>Başlık</th>
    </tr>
    #for $i in $proposals
    <tr>
      <td><a href="admin_comments.py?action=comments&amp;pid=$i.pid">$i.pid</a></td>
      <td><a href="admin_comments.py?action=comments&amp;pid=$i.pid">$i.title</a></td>
    </tr>
    #end for
  </table>
</div>
#include $site_path + "templates/footer.tpl"
