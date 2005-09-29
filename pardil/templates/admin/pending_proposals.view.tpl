#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Onay Bekleyen Öneri</h2>

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
  <form action="admin_p_proposals.py" method="post">
    <input type="hidden" name="p_tpid" value="#echo $printValue('p_tpid', '') #" />
    <fieldset>
      <legend>Öneri Bilgileri</legend>
      <div class="required">
        <label for="p_title">Başlık:</label>
        <input class="$errorCl('p_title')" type="text" id="p_title" name="p_title" size="35" value="#echo $printValue('p_title', '') #" />
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
        <textarea class="widetext $errorCl('p_summary')" id="p_summary" name="p_summary" cols="60" rows="5">#echo $printValue('p_summary', '') #</textarea>
      </div>
    </fieldset>
    <fieldset>
      <legend>Öneri İçeriği</legend>
      <div class="required">
        <textarea class="widetext $errorCl('p_content')" id="p_content" name="p_content" cols="60" rows="30">#echo $printValue('p_content', '') #</textarea>
      </div>
    </fieldset>
    <fieldset>
      <input type="hidden" name="start" value="$pag_now" />
      <button type="submit" name="action" value="publish"><strong>Yayınla</strong></button>
      <button type="submit" name="action" value="delete">Sil</button>
    </fieldset>
  </form>
</div>
#include $site_path + "templates/footer.tpl"
