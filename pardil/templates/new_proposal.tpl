#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Yeni Bildiri</h2>

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
  <form action="new_proposal.py" method="post" id="proposal_form">
    <fieldset>
      <legend>Bildiri Künyesi</legend>
      <div class="optional">
        <label for="p_pid">Bildiri Numarası:</label>
        <input class="$errorCl('p_pid')" type="text" id="p_pid" name="p_pid" size="20" value="#echo $printValue('p_pid', '') #" />
        <div>
          <small>Bildiri numarasının otomatik atanmasını istiyorsanız, burayı boş bırakın.</small>
        </div>
      </div>
      <div class="required">
        <label for="p_title">Başlık:</label>
        <input class="$errorCl('p_title')" type="text" id="p_title" name="p_title" size="35" value="#echo $printValue('p_title', '') #" />
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
      <input type="hidden" name="action" value="new" />
      <button type="submit">Gönder</button>
    </fieldset>
  </form>
</div>
#include $site_path + "templates/footer.tpl"
