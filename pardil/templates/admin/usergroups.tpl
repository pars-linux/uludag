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
  <h2>Kullanıcı Grupları</h2>
  <div>
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
      <input type="hidden" name="action" value="insert" />
      <button type="submit">Ekle</button>
    </fieldset>
  </form>
  </div>
  <table width="100%">
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
      <td>[<a href="admin_usergroups.py?action=delete&amp;relid=$i.relid&amp;start=$pag_now">Sil</a>]</td>
    </tr>
    #end for
  </table>
  <p>&nbsp;</p>
  <p style="text-align: center;">
    #for $i in range(0, $pag_total)
      #if $i == $pag_now
        <b>#echo $i+1 #</b>
      #else
        <a href="admin_usergroups.py?start=$i">#echo $i+1 #</a>
      #end if
    #end for
  </p>
</div>
#include $site_path + "templates/footer.tpl"
