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
  <h2>Erişim Hakları</h2>
  <div>
    #if len($errors)
    <p>
      Formda bazı hatalar bulunuyor, lütfen gerekli düzeltmeleri yapın ve formu tekrar gönderin.
    </p>
    <ul class="errors">
      #for $e,$v in $errors.items()
        <li>$v</li>
      #end for
    </ul>
    #end if
  <form method="post" action="admin_userrights.py">
    <fieldset>
      <legend>Erişim Hakkı Ekle</legend>
      <div class="required">
        <label for="r_group">Grup:</label>
        <select class="$errorCl('r_group')" name="r_group" id="r_group">
          <option value="0">Grup Seçin</option>
          #for $i in $groups
            #if $i.gid == $printValue('r_group')
              <option value="$i.gid" selected="selected">$i.label</option>
            #else
              <option value="$i.gid">$i.label</option>
            #end if
          #end for
        </select>
      </div>
      <div class="required">
        <label for="r_right">Hak:</label>
        <select class="$errorCl('r_right')" name="r_right" id="r_right">
          <option value="0">Hak Seçin</option>
          #for $i in $rights
            #if $i.rid == $printValue('r_right')
              <option value="$i.rid" selected="selected">$i.category - $i.label</option>
            #else
              <option value="$i.rid">$i.category - $i.label</option>
            #end if
          #end for
        </select>
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
      <th width="25">No</th>
      <th>Kategori</th>
      <th>Grup Adı</th>
      <th>Erişim Adı</th>
      <th width="30">&nbsp;</th>
    </tr>
    #for $c, $i in enumerate($rel_rights)
      #if $c % 2
      <tr class="odd">
      #else
      <tr class="even">
      #end if
      <td>$i.relid</td>
      <td>$i.category</td>
      <td>$i.group</td>
      <td>$i.right</td>
      <td>[<a href="admin_userrights.py?action=delete&amp;relid=$i.relid&amp;start=$pag_now">Sil</a>]</td>
    </tr>
    #end for
  </table>
  <p>&nbsp;</p>
  <p style="text-align: center;">
    #for $i in range(0, $pag_total)
      #if $i == $pag_now
        <b>#echo $i+1 #</b>
      #else
        <a href="admin_userrights.py?start=$i">#echo $i+1 #</a>
      #end if
    #end for
  </p>
</div>
#include $site_path + "templates/footer.tpl"
