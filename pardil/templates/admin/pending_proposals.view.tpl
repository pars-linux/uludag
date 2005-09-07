#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Onay Bekleyen Öneri</h2>

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

  <form action="admin_p_proposals.py" method="post">
    <input type="hidden" name="p_tpid" value="#echo $printValue('p_tpid', '') #" />
    <fieldset>
      <legend>Öneri Bilgileri</legend>
      <div class="required">
        <label for="p_title">Başlık:</label>
        <input type="text" id="p_title" name="p_title" size="35" value="#echo $printValue('p_title', '') #" />
        #echo $printError('p_title')
      </div>
      <div class="required">
        <label for="p_timeB">Tarih:</label>
        <input type="text" id="p_timeB" name="p_timeB" size="35" value="#echo $printValue('p_timeB', '') #" readonly="readonly" />
      </div>
      <div class="required">
        <label for="p_username">Gönderen:</label>
        <input type="text" id="p_username" name="p_username" size="35" value="#echo $printValue('p_username', '') #" readonly="readonly" />
        <input type="hidden" name="p_uid" value="#echo $printValue('p_uid', '') #" />
      </div>
      <div class="required">
        <label for="p_maintainer">Sorumluluk:</label>
        <div>
          <input type="checkbox" id="p_maintainer" name="p_maintainer" />
          <label for="p_maintainer">Kullanıcıyı sorumlu olarak ata.</label>
        </div>
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
      <input type="hidden" name="start" value="$pag_start" />
      <button type="submit" name="action" value="publish"><strong>Yayınla</strong></button>
      <button type="submit" name="action" value="delete">Sil</button>
    </fieldset>
  </form>
</div>
#include $site_path + "templates/footer.tpl"
