#include $site_path + "templates/header.tpl"
<div id="content">
  #def printError($s)
    #if $errors.has_key($s)
      #echo """<div class="error_msg">%s</div>""" % ($errors[$s])
    #end if
  #end def

  #def printValue($s, $t='')
    #if not $errors.has_key($s) and $posted.has_key($s)
      #echo $posted[$s]
    #else
      #echo $t
    #end if
  #end def
  <h2>Erişim Kodları</h2>
  <div>
    <form method="post" action="admin_rights.py">
      <fieldset>
        <legend>Erişim Kodu Ekle</legend>
        <div class="required">
          <label for="r_category">Kategori:</label>
          <input type="text" id="r_category" name="r_category" value="" />
          #echo $printError('r_category')
        </div>
        <div class="required">
          <label for="r_keyword">Kod:</label>
          <input type="text" id="r_keyword" name="r_keyword" value="" />
          #echo $printError('r_keyword')
        </div>
        <div class="required">
          <label for="r_label">Etiket:</label>
          <input type="text" id="r_labe" name="r_label" value="" />
          #echo $printError('r_label')
        </div>
      </fieldset>
      <fieldset>
        <input type="hidden" name="action" value="insert" />
        <button type="submit">Ekle</button>
      </fieldset>
    </form>
  </div>
  <table width="100%">
    <tr>
      <th>No</th>
      <th>Kategori</th>
      <th>Kod</th>
      <th>Etiket</th>
      <th>&nbsp;</th>
    </tr>
    #for $i in $rights
    <tr>
      <td>$i.rid</td>
      <td>$i.category</td>
      <td>$i.keyword</td>
      <td>$i.label</td>
      <td>[<a href="admin_rights.py?action=delete&amp;rid=$i.rid&amp;start=$pag_now">Sil</a>]</td>
    </tr>
    #end for
  </table>
  <p>&nbsp;</p>
  <p style="text-align: center;">
    #for $i in range(0, $pag_total)
      #if $i == $pag_now
        <b>#echo $i+1 #</b>
      #else
        <a href="admin_rights.py?start=$i">#echo $i+1 #</a>
      #end if
    #end for
  </p>
</div>
#include $site_path + "templates/footer.tpl"
