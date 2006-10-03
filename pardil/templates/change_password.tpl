#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Parola Değiştir</h2>

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

  #if $mode == 'done':
    <p>Parolanız değiştirildi. Sisteme, yeni parolanızla giriş yapabilirsiniz.</p>
    <ul>
      <li><a href="login.py">Giriş Sayfası</a>'na Git</li>
    </ul>
  #elif $mode == 'code':
  <p>
    Parolanızı değiştirmeden önce, kullanıcı bilgilerinizi girin ve parola değiştirme
    işlemini tamamlamanız için gereken onay kodunun e-posta adresinize gönderilmesini
    sağlayın.
  </p>
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
  <form action="change_password.py" method="post">
    <input type="hidden" name="post" value="1" />
    <fieldset>
      <legend>Hesap Bilgileri</legend>
      <div class="required">
        <label for="c_username">Kullanıcı Adı:</label>
        <input class="$errorCl('c_username')" type="text" id="c_username" name="c_username" value="#echo $printValue('c_username', '') #" />
      </div>
      <div class="required">
        <label for="c_email">E-Posta Adresi:</label>
        <input class="$errorCl('c_email')" type="text" id="c_email" name="c_email" value="#echo $printValue('c_email', '') #" />
      </div>
    </fieldset>
    <fieldset>
      <input type="hidden" name="action" value="code" />
      <button type="submit">Kodu Gönder &raquo;</button>
    </fieldset>
  </form>
  #elif $mode == 'change'
  <p>
    Parolanızı değiştirmek için, yeni parolanızı ve e-posta adresinize gönderilen parola 
    değiştirme onay kodunu yazın. Bu işlemi <strong>$time</strong> içinde yapmazsanız, 
    parola değiştirme kodu geçerliliğini yitirir.
  </p>
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
  <form action="change_password.py" method="post">
    <input type="hidden" name="post" value="1" />
    <fieldset>
      <legend>Hesap Bilgileri</legend>
      <div class="required">
        <label for="c_password">Parola:</label>
        <input class="$errorCl('c_password')" type="password" id="c_password" name="c_password" value="#echo $printValue('c_password', '') #" />
      </div>
      <div class="required">
        <label for="c_password2">Tekrar Parola:</label>
        <input class="$errorCl('c_password')" type="password" id="c_password2" name="c_password2" value="#echo $printValue('c_password2', '') #" />
      </div>
      <div class="optional">
        <label for="c_code">Hatırlatma Kodu:</label>
        <input class="$errorCl('c_code')" type="text" id="c_code" name="c_code" value="#echo $printValue('c_code', '') #" />
      </div>
    </fieldset>
    <fieldset>
      <input type="hidden" name="action" value="change" />
      <button type="submit">Parolayı Değiştir &raquo;</button>
    </fieldset>
  </form>
  #end if
</div>
#include $site_path + "templates/footer.tpl"
