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
  <h2>Gruplar</h2>
  #if $status == 'list' or $status == ''
  <div style="float: right;">
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
        <button type="submit" name="insert" value="1">Ekle</button>
      </fieldset>
    </form>
  </div>
  <table>
    <tr>
      <th>No</th>
      <th>Grup Adı</th>
      <th>&nbsp;</th>
    </tr>
    #for $i in $groups
    <tr>
      <td>$i.gid</td>
      <td>$i.label</td>
      <td>[<a href="admin_groups.py?delete=$i.gid">Sil</a>]</td>
    </tr>
    #end for
  </table>
  #else if $status == 'delete_confirm'
    <p>
      Eğer bir grubu silerseniz, grup ile ilişkili tüm erişim hakları da silinir.<br/>
      $gid numaralı "$label" grubunu silmek istediğinizden emin misiniz?
    </p>
    <ul>
      <li><a href="admin_groups.py?delete=$gid&amp;confirm=no">Hayır</a></li>
      <li><a href="admin_groups.py?delete=$gid&amp;confirm=yes">Evet</a></li>
    </ul>
  #else if $status == 'delete_yes'
    <p>
      $gid numaralı "$label" grubu silindi.<br/>
      Grup ile ilişkili tüm erişim hakları kaldırıldı.
    </p>
    <ul>
      <li><a href="admin_groups.py">Listeye Dön</a></li>
    </ul>
  #else if $status == 'delete_no'
    <p>
      Silme işlemi iptal edildi.
    </p>
    <ul>
      <li><a href="admin_groups.py">Listeye Dön</a></li>
    </ul>
  #else if $status == 'error'
    <p>
      $gid numaralı bir grup bulunmuyor.
    </p>
    <ul>
      <li><a href="admin_groups.py">Listeye Dön</a></li>
    </ul>
  #else if $status == 'insert'
    <p>
      $gid numaralı "$label" grubu listeye eklendi.
    </p>
    <ul>
      <li><a href="admin_groups.py">Listeye Dön</a></li>
    </ul>
  #end if
</div>
#include $site_path + "templates/footer.tpl"
