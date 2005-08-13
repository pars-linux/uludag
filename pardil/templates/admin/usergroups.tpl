#include $site_path + "templates/header.tpl"
<div id="content">
  #def printError($s)
    #if $errors.has_key($s)
      #echo """<div class="error_msg">%s</div>""" % ($errors[$s])
    #end if
  #end def

  #def printValue($s, $t='')
    #if not $errors.has_key($s) and $posted_values.has_key($s)
      #echo $posted_values[$s]
    #else
      #echo $t
    #end if
  #end def
  <h2>Kullanıcı Grupları</h2>
  #if $status == 'list' or $status == ''
  <div style="float: right; ">
  <form method="post" action="admin_usergroups.py">
    <fieldset>
      <legend>Gruba Kullanıcı Ekle</legend>
      <div class="required">
        <label for="u_group">Grup:</label>
        <select name="u_group" id="u_group">
          <option value="0">Grup Seçin</option>
          #for $i in $groups
            #if $i.gid == $printValue('u_group')
              <option value="$i.gid" selected="selected">$i.label</option>
            #else
              <option value="$i.gid">$i.label</option>
            #end if
          #end for
        </select>
        #echo $printError('u_group')
      </div>
      <div class="required">
        <label for="u_user">Kullanıcı:</label>
        <select name="u_user" id="u_user">
          <option value="0">Kullanıcıyı Seçin</option>
          #for $i in $users
            #if $i.uid == $printValue('u_user')
              <option value="$i.uid" selected="selected">$i.username</option>
            #else
              <option value="$i.uid">$i.username</option>
            #end if
          #end for
        </select>
        #echo $printError('u_user')
      </div>
    </fieldset>
    <fieldset>
      <button type="submit" name="insert" value="1">Ekle</button>
    </fieldset>
  </form>
  </div>
  <table>
    <tr>
      <th>No</th>
      <th>Grup Adı</th>
      <th>Kullanıcı Adı</th>
      <th>&nbsp;</th>
    </tr>
    #for $i in $rel_groups
    <tr>
      <td>$i.relid</td>
      <td>$i.group</td>
      <td>$i.username</td>
      <td>[<a href="admin_usergroups.py?delete=$i.relid">Sil</a>]</td>
    </tr>
    #end for
  </table>
  #else if $status == 'delete_confirm'
    <p>
      $user isimli kullanıcı $group grubundan çıkarılsın mı?
    </p>
    <ul>
      <li><a href="admin_usergroups.py?delete=$relid&amp;confirm=no">Hayır</a></li>
      <li><a href="admin_usergroups.py?delete=$relid&amp;confirm=yes">Evet</a></li>
    </ul>
  #else if $status == 'delete_yes'
    <p>
      $user isimli kullanıcı $group grubundan çıkarıldı.
    </p>
    <ul>
      <li><a href="admin_usergroups.py">Listeye Dön</a></li>
    </ul>
  #else if $status == 'delete_no'
    <p>
      Silme işlemi iptal edildi.
    </p>
    <ul>
      <li><a href="admin_usergroups.py">Listeye Dön</a></li>
    </ul>
  #else if $status == 'error'
    <p>
      $relid numaralı bir grup-kullanıcı kaydı bulunmuyor.
    </p>
    <ul>
      <li><a href="admin_usergroups.py">Listeye Dön</a></li>
    </ul>
  #else if $status == 'insert'
    <p>
      $user isimli kullanıcı $group grubuna eklendi.
    </p>
    <ul>
      <li><a href="admin_usergroups.py">Listeye Dön</a></li>
    </ul>
  #end if
</div>
#include $site_path + "templates/footer.tpl"
