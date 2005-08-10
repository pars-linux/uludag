#include $site_path + "templates/header.tpl"
<div id="content">
  #if $revision
  <h2>Yeni Sürüm</h2>
  #else
  <h2>Yeni Öneri</h2>
  #end if

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

  #if $status == 'done'
    <p>Öneri yayında.</p>
  #else:
  <form action="new_proposal.py" method="post">
    <fieldset>
      <legend>Öneri Bilgileri</legend>
      <div class="required">
        <label for="p_title">Başlık:</label>
        <input type="text" id="p_title" name="p_title" value="#echo $printValue('p_title', '') #" />
        #echo $printError('p_title')
      </div>
      #if $revision
      <input type="hidden" name="pid" value="$pid" />
      <div class="optional">
        <label>Mevcut Sürüm No.:</label>
        <input id="version" name="version" type="text" value="$version" readonly="readonly" />
      </div>
      <div class="required">
        <label for="p_version">Yeni Sürüm No.:</label>
        <input id="p_version" name="p_version" type="text" value="#echo $printValue('p_version', '') #" />
        <small>Sürüm numarasını değiştirmezseniz, belirtilen sürümün üzerine yazılır.</small>
        #echo $printError('p_version')
      </div>
      #end if
    </fieldset>
    <fieldset>
      <legend>Öneri İçeriği</legend>
      <div class="required">
        <textarea class="widetext" id="p_content" name="p_content">#echo $printValue('p_content', '') #</textarea>
        #echo $printError('p_content')
      </div>
    </fieldset>
    #if $revision
    <fieldset>
      <legend>Sürüm Notları</legend>
      <div class="required">
        <textarea class="widetext" id="p_changelog" name="p_changelog">#echo $printValue('p_changelog', '') #</textarea>
        #echo $printError('p_changelog')
      </div>
    </fieldset>
    #end if
    <fieldset>
      <button type="submit" name="new_proposal" value="1">Gönder</button>
    </fieldset>
  </form>
  #end if
</div>
#include $site_path + "templates/footer.tpl"
