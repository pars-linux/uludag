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
  <h2>Erişim Hakları</h2>
  #if $status == 'list' or $status == ''
  <div style="float: right; ">
  <form method="post" action="admin_rights.py">
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
      <button type="submit" name="insert" value="1">Ekle</button>
    </fieldset>
  </form>
  </div>
  <table>
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
      <td>[<a href="admin_rights.py?delete=$i.relid">Sil</a>]</td>
    </tr>
    #end for
  </table>
  #else if $status == 'delete_confirm'
    <p>
      $relid numaralı "$group - $right" erişimini silmek istediğinizden emin misiniz?
    </p>
    <ul>
      <li><a href="admin_rights.py?delete=$relid&amp;confirm=no">Hayır</a></li>
      <li><a href="admin_rights.py?delete=$relid&amp;confirm=yes">Evet</a></li>
    </ul>
  #else if $status == 'delete_yes'
    <p>
      $relid numaralı "$group - $right" erişim hakkı silindi.<br/>
    </p>
    <ul>
      <li><a href="admin_rights.py">Listeye Dön</a></li>
    </ul>
  #else if $status == 'delete_no'
    <p>
      Silme işlemi iptal edildi.
    </p>
    <ul>
      <li><a href="admin_rights.py">Listeye Dön</a></li>
    </ul>
  #else if $status == 'error'
    <p>
      $relid numaralı bir erişim hakkı bulunmuyor.
    </p>
    <ul>
      <li><a href="admin_rights.py">Listeye Dön</a></li>
    </ul>
  #else if $status == 'insert'
    <p>
      $relid numaralı "$group - $right" erişim hakkı listeye eklendi.
    </p>
    <ul>
      <li><a href="admin_rights.py">Listeye Dön</a></li>
    </ul>
  #end if
</div>
#include $site_path + "templates/footer.tpl"
