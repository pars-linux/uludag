#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Kullanıcı Kaydı</h2>

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
  <form action="register.py" method="post">
    <fieldset>
      <legend>Hesap Bilgileri</legend>
      <div class="required">
        <label for="r_username">Kullanıcı Adı:</label>
        <input class="$errorCl('r_username')" type="text" id="r_username" name="r_username" value="#echo $printValue('r_username', '') #" />
      </div>
      <div class="required">
        <label for="r_email">E-Posta Adresi:</label>
        <input class="$errorCl('r_email')" type="text" id="r_email" name="r_email" value="#echo $printValue('r_email', '') #" />
      </div>
      <div class="sep">&nbsp;</div>
      <div class="required">
        <label for="r_password">Parola:</label>
        <input class="$errorCl('r_password')" type="password" id="r_password" name="r_password" value="#echo $printValue('r_password', '') #" />
      </div>
      <div class="required">
        <label for="r_password2">Tekrar Parola:</label>
        <input class="$errorCl('r_password')" type="password" id="r_password2" name="r_password2" value="#echo $printValue('r_password', '') #" />
      </div>
    </fieldset>
    <fieldset>
      <input type="hidden" name="action" value="register" />
      <button type="submit">Kayıt</button>
    </fieldset>
  </form>
</div>
#include $site_path + "templates/footer.tpl"
