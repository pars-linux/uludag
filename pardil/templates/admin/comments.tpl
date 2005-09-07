#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Önerilere Yapılan Yorumlar</h2>
  <table width="100%">
    <tr>
      <th>No</th>
      <th>Başlık</th>
    </tr>
    #for $i in $proposals
    <tr>
      <td><a href="admin_comments.py?action=comments&amp;pid=$i.pid&amp;start=$pag_now">$i.pid</a></td>
      <td><a href="admin_comments.py?action=comments&amp;pid=$i.pid&amp;start=$pag_now">$i.title</a></td>
    </tr>
    #end for
  </table>
  <p>&nbsp;</p>
  <p style="text-align: center;">
    #for $i in range(0, $pag_total)
      #if $i == $pag_now
        <b>#echo $i+1 #</b>
      #else
        <a href="admin_comments.py?start=$i">#echo $i+1 #</a>
      #end if
    #end for
  </p>
</div>
#include $site_path + "templates/footer.tpl"
