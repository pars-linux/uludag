#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Yeni Sürüm</h2>

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

  <form action="edit_proposal.py" method="post">
    <fieldset>
      <legend>Öneri Bilgileri</legend>
      <div class="required">
        <label for="p_title">Başlık:</label>
        <input type="text" id="p_title" name="p_title" value="#echo $printValue('p_title', '') #" size="35" />
        #echo $printError('p_title')
      </div>
      <input type="hidden" name="pid" value="$pid" />
      <div class="optional">
        <label>Mevcut Sürüm No.:</label>
        <input id="version" name="version" type="text" value="$version" readonly="readonly" />
      </div>
      <div class="required">
        <label for="p_version">Değişiklik Derecesi:</label>
        <select id="p_version" name="p_version">
          <option value="3">Düşük</option>
          <option value="2">Orta</option>
          <option value="1">Yüksek</option>
        </select>
        #echo $printError('p_version')
      </div>
    </fieldset>
    <fieldset>
      <legend>Öneri Özeti</legend>
      <div class="required">
        <textarea class="widetext" id="p_summary" name="p_summary" cols="60" rows="5">#echo $printValue('p_summary', '') #</textarea>
        #echo $printError('p_summary')
      </div>
    </fieldset>
    <fieldset>
      <legend>Amaç</legend>
      <div class="required">
        <textarea class="widetext" id="p_purpose" name="p_purpose" cols="60" rows="10">#echo $printValue('p_purpose', '') #</textarea>
        #echo $printError('p_purpose')
      </div>
    </fieldset>
    <fieldset>
      <legend>Öneri Detayları</legend>
      <div class="required">
        <textarea class="widetext" id="p_content" name="p_content" cols="60" rows="10">#echo $printValue('p_content', '') #</textarea>
        #echo $printError('p_content')
      </div>
    </fieldset>
    <fieldset>
      <legend>Çözüm</legend>
      <div class="required">
        <textarea class="widetext" id="p_solution" name="p_solution" cols="60" rows="10">#echo $printValue('p_solution', '') #</textarea>
        #echo $printError('p_solution')
      </div>
    </fieldset>
    <fieldset>
      <legend>Sürüm Notları</legend>
      <div class="required">
        <textarea class="widetext" id="p_changelog" name="p_changelog" cols="60" rows="5">#echo $printValue('p_changelog', '') #</textarea>
        #echo $printError('p_changelog')
      </div>
    </fieldset>
    <fieldset>
      <input type="hidden" name="action" value="edit" />
      <button type="submit">Gönder</button>
    </fieldset>
  </form>
</div>
#include $site_path + "templates/footer.tpl"
