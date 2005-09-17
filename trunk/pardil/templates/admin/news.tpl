#include $site_path + "templates/header.tpl"
<div id="content">
  #def errorCl($s)
    #if $errors.has_key($s)
      #echo "error"
    #end if
  #end def

  #def printValue($s, $t='')
    #if not $errors.has_key($s) and $posted.has_key($s)
      #echo $posted[$s]
    #else
      #echo $t
    #end if
  #end def
  <h2>Haberler</h2>
  <ul>
    <li><a href="admin_news.py?action=insert">Haber Ekle</a></li>
  </ul>
  <table width="100%">
    <tr>
      <th width="25">No</th>
      <th width="200">Tarih</th>
      <th>Başlık</th>
      <th width="90">&nbsp;</th>
    </tr>
    #for $c, $i in enumerate($news)
      #if $c % 2
      <tr class="odd">
      #else
      <tr class="even">
      #end if
      <td>$i.nid</td>
      <td>$i.date</td>
      <td>$i.title</td>
      <td>
        [<a href="admin_news.py?action=edit&amp;nid=$i.nid&amp;start=$pag_now">Değiştir</a>]
        [<a href="admin_news.py?action=delete&amp;nid=$i.nid&amp;start=$pag_now">Sil</a>]
      </td>
    </tr>
    #end for
  </table>
  <p>&nbsp;</p>
  <p style="text-align: center;">
    #for $i in range(0, $pag_total)
      #if $i == $pag_now
        <b>#echo $i+1 #</b>
      #else
        <a href="admin_news.py?start=$i">#echo $i+1 #</a>
      #end if
    #end for
  </p>
</div>
#include $site_path + "templates/footer.tpl"
