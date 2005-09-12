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
  <h2>Öneri Sorumluları</h2>
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
  <form method="post" action="admin_maintainers.py">
    <fieldset>
      <legend>Sorumlu Ekle</legend>
      <div class="required">
        <label for="m_proposal">Öneri:</label>
        <select class="$errorCl('m_proposal')" name="m_proposal" id="m_proposal">
          <option value="0">Öneri Seçin</option>
          #for $i in $proposals
            #if $i.pid == $printValue('m_proposal')
              <option value="$i.pid" selected="selected">$i.title</option>
            #else
              <option value="$i.pid">$i.title</option>
            #end if
          #end for
        </select>
      </div>
      <div class="required">
        <label for="m_user">Kullanıcı:</label>
        <select class="$errorCl('m_user')" name="m_user" id="m_user">
          <option value="0">Kullanıcıyı Seçin</option>
          #for $i in $users
            #if $i.uid == $printValue('m_user')
              <option value="$i.uid" selected="selected">$i.username</option>
            #else
              <option value="$i.uid">$i.username</option>
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
      <th>Öneri</th>
      <th>Kullanıcı Adı</th>
      <th width="30">&nbsp;</th>
    </tr>
    #for $c, $i in enumerate($rel_maintainers)
      #if $c % 2
      <tr class="odd">
      #else
      <tr class="even">
      #end if
      <td>$i.relid</td>
      <td>$i.proposal</td>
      <td>$i.username</td>
      <td>[<a href="admin_maintainers.py?action=delete&amp;relid=$i.relid&amp;start=$pag_now">Sil</a>]</td>
    </tr>
    #end for
  </table>
  <p>&nbsp;</p>
  <p style="text-align: center;">
    #for $i in range(0, $pag_total)
      #if $i == $pag_now
        <b>#echo $i+1 #</b>
      #else
        <a href="admin_maintainers.py?start=$i">#echo $i+1 #</a>
      #end if
    #end for
  </p>
</div>
#include $site_path + "templates/footer.tpl"
