#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Kullanıcı Girişi</h2>

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

  <form action="login.py" method="post">
    <fieldset>
      <legend>Hesap Bilgileri</legend>
      <div class="required">
        <label for="l_username">Kullanıcı Adı:</label>
        <input type="text" id="l_username" name="l_username" value="#echo $printValue('l_username', '') #" />
        #echo $printError('l_username')
      </div>
      <div class="required">
        <label for="l_password">Parola:</label>
        <input type="password" id="l_password" name="l_password" value="#echo $printValue('l_password', '') #" />
        #echo $printError('l_password')
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
