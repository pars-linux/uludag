#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Yeni Öneri</h2>

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

  <form action="new_proposal.py" method="post">
    <fieldset>
      <legend>Öneri Bilgileri</legend>
      <div class="required">
        <label for="p_title">Başlık:</label>
        <input type="text" id="p_title" name="p_title" size="35" value="#echo $printValue('p_title', '') #" />
        #echo $printError('p_title')
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
      <input type="hidden" name="action" value="new" />
      <button type="submit">Gönder</button>
    </fieldset>
  </form>
</div>
#include $site_path + "templates/footer.tpl"
