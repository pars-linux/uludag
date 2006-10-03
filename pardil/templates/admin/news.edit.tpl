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
  <h2>Haberler</h2>
  #if $mode == 'done'
  <p>
    $nid numaralı "$title" haberi değiştirildi.
  </p>
  <ul>
    <li><a href="admin_news.py?start=$pag_now">Listeye Dön</a></li>
  </ul>
  #else
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
    <form method="post" action="admin_news.py">
      <input type="hidden" name="post" value="1" />
      <fieldset>
        <legend>Haber Ekle</legend>
        <div class="required">
          <label for="nid">No:</label>
          <input type="text" id="nid" name="nid" value="$nid" readonly="readonly" size="40" />
        </div>
        <div class="required">
          <label for="n_title">Başlık:</label>
          <input class="$errorCl('n_title')" type="text" id="n_title" name="n_title" value="#echo $printValue('n_title', '') #" size="40" />
        </div>
        <div class="required">
          <label for="n_icon">Simge:</label>
          <select class="$errorCl('n_icon')" id="n_icon" name="n_icon">
          #for $i in $icons
            #if $i == $printValue('n_icon')
              <option value="$i" selected="selected">$i</option>
            #else
              <option value="$i">$i</option>
            #end if
          #end for
          </select>
        </div>
      </fieldset>
      <fieldset>
        <legend>İçerik</legend>
        <div class="required">
          <textarea class="widetext $errorCl('n_body')" id="n_body" name="n_body" cols="60" rows="10">#echo $printValue('n_body', '') #</textarea>
        </div>
      </fieldset>
      <fieldset>
        <input type="hidden" name="action" value="edit" />
        <button type="submit">Değiştir</button>
      </fieldset>
    </form>
  </div>
  #end if
</div>
#include $site_path + "templates/footer.tpl"
