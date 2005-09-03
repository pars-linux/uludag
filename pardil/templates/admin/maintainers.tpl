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
  <h2>Öneri Sorumluları</h2>
  <div>
  <form method="post" action="admin_maintainers.py">
    <fieldset>
      <legend>Sorumlu Ekle</legend>
      <div class="required">
        <label for="m_proposal">Öneri:</label>
        <select name="m_proposal" id="m_proposal">
          <option value="0">Öneri Seçin</option>
          #for $i in $proposals
            #if $i.pid == $printValue('m_proposal')
              <option value="$i.pid" selected="selected">$i.title</option>
            #else
              <option value="$i.pid">$i.title</option>
            #end if
          #end for
        </select>
        #echo $printError('m_proposal')
      </div>
      <div class="required">
        <label for="m_user">Kullanıcı:</label>
        <select name="m_user" id="m_user">
          <option value="0">Kullanıcıyı Seçin</option>
          #for $i in $users
            #if $i.uid == $printValue('m_user')
              <option value="$i.uid" selected="selected">$i.username</option>
            #else
              <option value="$i.uid">$i.username</option>
            #end if
          #end for
        </select>
        #echo $printError('m_user')
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
      <th>Öneri</th>
      <th>Kullanıcı Adı</th>
      <th>&nbsp;</th>
    </tr>
    #for $i in $rel_maintainers
    <tr>
      <td>$i.relid</td>
      <td>$i.proposal</td>
      <td>$i.username</td>
      <td>[<a href="admin_maintainers.py?action=delete&amp;relid=$i.relid">Sil</a>]</td>
    </tr>
    #end for
  </table>
</div>
#include $site_path + "templates/footer.tpl"
