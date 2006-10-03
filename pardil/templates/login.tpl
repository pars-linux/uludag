#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Kullanıcı Girişi</h2>

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
  <form action="login.py" method="post">
    <fieldset>
      <legend>Hesap Bilgileri</legend>
      <div class="required">
        <label for="l_username">Kullanıcı Adı:</label>
        <input class="$errorCl('l_username')" type="text" id="l_username" name="l_username" value="#echo $printValue('l_username', '') #" />
      </div>
      <div class="required">
        <label for="l_password">Parola:</label>
        <input class="$errorCl('l_password')" type="password" id="l_password" name="l_password" value="#echo $printValue('l_password', '') #" />
      </div>
    </fieldset>
    <fieldset>
      <input type="hidden" name="action" value="login" />
      <button type="submit">Giriş</button>
    </fieldset>
  </form>
  <ul>
    <li><a href="change_password.py">Şifremi Unuttum</a></li>
  </ul>
</div>
#include $site_path + "templates/footer.tpl"
