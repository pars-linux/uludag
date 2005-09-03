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
  <h2>Erişim Hakları</h2>
  <div>
  <form method="post" action="admin_userrights.py">
    <fieldset>
      <legend>Erişim Hakkı Ekle</legend>
      <div class="required">
        <label for="r_group">Grup:</label>
        <select name="r_group" id="r_group">
          <option value="0">Grup Seçin</option>
          #for $i in $groups
            #if $i.gid == $printValue('r_group')
              <option value="$i.gid" selected="selected">$i.label</option>
            #else
              <option value="$i.gid">$i.label</option>
            #end if
          #end for
        </select>
        #echo $printError('r_group')
      </div>
      <div class="required">
        <label for="r_right">Hak:</label>
        <select name="r_right" id="r_right">
          <option value="0">Hak Seçin</option>
          #for $i in $rights
            #if $i.rid == $printValue('r_right')
              <option value="$i.rid" selected="selected">$i.label</option>
            #else
              <option value="$i.rid">$i.label</option>
            #end if
          #end for
        </select>
        #echo $printError('r_right')
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
      <th>Grup Adı</th>
      <th>Erişim Adı</th>
      <th>&nbsp;</th>
    </tr>
    #for $i in $rel_rights
    <tr>
      <td>$i.relid</td>
      <td>$i.category</td>
      <td>$i.group</td>
      <td>$i.right</td>
      <td>[<a href="admin_userrights.py?action=delete&amp;relid=$i.relid">Sil</a>]</td>
    </tr>
    #end for
  </table>
</div>
#include $site_path + "templates/footer.tpl"
