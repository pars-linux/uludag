#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Onay Bekleyen Öneriler</h2>
  <table width="100%">
    <tr>
      <th>No</th>
      <th>Başlık</th>
      <th>&nbsp;</th>
    </tr>
    #for $i in $pending
    <tr>
      <td>$i.tpid</td>
      <td>$i.title</td>
      <td><a href="admin_p_proposals.py?action=view&amp;tpid=$i.tpid">Görüntüle</a></td>
    </tr>
    #end for
  </table>
</div>
#include $site_path + "templates/footer.tpl"
