#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Kullanıcı Kaydı</h2>

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

  <form action="register.py" method="post">
    <fieldset>
      <legend>Hesap Bilgileri</legend>
      <div class="required">
        <label for="r_username">Kullanıcı Adı:</label>
        <input type="text" id="r_username" name="r_username" value="#echo $printValue('r_username', '') #" />
        #echo $printError('r_username')
      </div>
      <div class="required">
        <label for="r_email">E-Posta Adresi:</label>
        <input type="text" id="r_email" name="r_email" value="#echo $printValue('r_email', '') #" />
        #echo $printError('r_email')
      </div>
      <div class="sep">&nbsp;</div>
      <div class="required">
        <label for="r_password">Parola:</label>
        <input type="password" id="r_password" name="r_password" value="#echo $printValue('r_password', '') #" />
      </div>
      <div class="required">
        <label for="r_password2">Tekrar Parola:</label>
        <input type="password" id="r_password2" name="r_password2" value="#echo $printValue('r_password', '') #" />
        #echo $printError('r_password')
      </div>
    </fieldset>
    <!--
    <fieldset>
      <legend>Kişisel Bilgiler</legend>
      <div class="required">
        <label for="r_firstname">İsim:</label>
        <input type="text" id="r_firstname" name="r_firstname" value="#echo $printValue('r_firstname', '') #" />
        #echo $printError('r_firstname')
      </div>
      <div class="required">
        <label for="r_lastname">Soyisim:</label>
        <input type="text" id="r_lastname" name="r_lastname" value="#echo $printValue('r_lastname', '') #" />
        #echo $printError('r_lastname')
      </div>
    </fieldset>
    -->
    <fieldset>
      <input type="hidden" name="action" value="register" />
      <button type="submit">Kayıt</button>
    </fieldset>
  </form>
</div>
#include $site_path + "templates/footer.tpl"
