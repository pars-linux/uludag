#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Yeni Sürüm</h2>

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
  <form action="edit_proposal.py" method="post" id="proposal_form">
    <fieldset>
      <legend>Bildiri Künyesi</legend>
      <div class="required">
        <label for="p_title">Başlık:</label>
        <input class="$errorCl('p_title')" type="text" id="p_title" name="p_title" value="#echo $printValue('p_title', '') #" size="35" />
      </div>
      <input type="hidden" name="pid" value="$pid" />
      <div class="optional">
        <label>Mevcut Sürüm No.:</label>
        <input id="version" name="version" type="text" value="$version" readonly="readonly" />
      </div>
      <div class="required">
        <label for="p_version">Değişiklik Derecesi:</label>
        <select class="$errorCl('p_version')" id="p_version" name="p_version">
          <option value="3">Düşük</option>
          <option value="2">Orta</option>
          <option value="1">Yüksek</option>
        </select>
      </div>
    </fieldset>
    <fieldset>
      <legend>Bildiri Özeti</legend>
      <div class="required">
        <textarea class="widetext $errorCl('p_summary')" id="p_summary" name="p_summary" cols="60" rows="5">#echo $printValue('p_summary', '') #</textarea>
      </div>
    </fieldset>
    <fieldset>
      <legend>Bildiri İçeriği</legend>
      <div class="required">
        <textarea class="widetext $errorCl('p_content')" id="p_content" name="p_content" cols="60" rows="30">#echo $printValue('p_content', '') #</textarea>
      </div>
    </fieldset>
    <fieldset>
      <legend>Sürüm Notları</legend>
      <div class="required">
        <textarea class="widetext $errorCl('p_changelog')" id="p_changelog" name="p_changelog" cols="60" rows="5">#echo $printValue('p_changelog', '') #</textarea>
      </div>
    </fieldset>
    <fieldset>
      <input type="hidden" name="action" value="edit" />
      <button type="submit">Gönder</button>
    </fieldset>
  </form>
</div>
#include $site_path + "templates/footer.tpl"
