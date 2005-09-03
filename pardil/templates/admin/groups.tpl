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
  <h2>Gruplar</h2>
  <div>
    <form method="post" action="admin_groups.py">
      <fieldset>
        <legend>Grup Ekle</legend>
        <div class="required">
          <label for="g_label">Grup Adı:</label>
          <input type="text" id="g_label" name="g_label" value="" />
          #echo $printError('g_label')
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
      <th>&nbsp;</th>
    </tr>
    #for $i in $groups
    <tr>
      <td>$i.gid</td>
      <td>$i.label</td>
      <td>[<a href="admin_groups.py?action=delete&amp;gid=$i.gid">Sil</a>]</td>
    </tr>
    #end for
  </table>
</div>
#include $site_path + "templates/footer.tpl"
