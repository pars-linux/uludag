#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Onay Bekleyen Öneriler</h2>
  <table width="100%">
    <tr>
      <th width="25">No</th>
      <th>Başlık</th>
      <th width="40">&nbsp;</th>
    </tr>
    #for $c, $i in enumerate($pending)
      #if $c % 2
      <tr class="odd">
      #else
      <tr class="even">
      #end if
      <td>$i.tpid</td>
      <td>$i.title</td>
      <td><a href="admin_p_proposals.py?action=view&amp;tpid=$i.tpid&amp;start=$pag_now">Görüntüle</a></td>
    </tr>
    #end for
  </table>
  <p>&nbsp;</p>
  <p style="text-align: center;">
    #for $i in range(0, $pag_total)
      #if $i == $pag_now
        <b>#echo $i+1 #</b>
      #else
        <a href="admin_p_proposals.py?start=$i">#echo $i+1 #</a>
      #end if
    #end for
  </p>
</div>
#include $site_path + "templates/footer.tpl"
