#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Şifre Değiştir</h2>

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
  
  #if $mode == 'done':
    Şifre değiştirildi.
  #elif $mode == 'code':
  <form action="change_password.py" method="post">
    <input type="hidden" name="post" value="1" />
    <fieldset>
      <legend>Hesap Bilgileri</legend>
      <div class="required">
        <label for="c_username">Kullanıcı Adı:</label>
        <input type="text" id="c_username" name="c_username" value="#echo $printValue('c_username', '') #" />
        #echo $printError('c_username')
      </div>
      <div class="required">
        <label for="c_email">E-Posta Adresi:</label>
        <input type="text" id="c_email" name="c_email" value="#echo $printValue('c_email', '') #" />
        #echo $printError('c_email')
      </div>
    </fieldset>
    <fieldset>
      <button type="submit" name="action" value="code">Kodu Gönder &raquo;</button>
    </fieldset>
  </form>
  #elif $mode == 'change'
  <form action="change_password.py" method="post">
    <input type="hidden" name="post" value="1" />
    <fieldset>
      <legend>Hesap Bilgileri</legend>
      <div class="required">
        <label for="c_password">Parola:</label>
        <input type="password" id="c_password" name="c_password" value="#echo $printValue('c_password', '') #" />
      </div>
      <div class="required">
        <label for="c_password2">Tekrar Parola:</label>
        <input type="password" id="c_password2" name="c_password2" value="#echo $printValue('c_password2', '') #" />
        #echo $printError('c_password')
      </div>
      <div class="optional">
        <label for="c_code">Hatırlatma Kodu:</label>
        <input type="text" id="c_code" name="c_code" value="#echo $printValue('c_code', '') #" />
        #echo $printError('c_code')
      </div>
    </fieldset>
    <fieldset>
      <button type="submit" name="action" value="change">Şifreyi Değiştir &raquo;</button>
    </fieldset>
  </form>
  #end if
</div>
#include $site_path + "templates/footer.tpl"
