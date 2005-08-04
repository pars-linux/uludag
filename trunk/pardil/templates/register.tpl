<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="tr">
  <head>
    <title>$site_title</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" href="style.css" type="text/css" />
    <!--
    <link rel="icon" type="image/png" href="images/favicon.png"/>
    <link rel="alternate" type="application/rss+xml" title="RSS 2.0" href="feed.rss" />
    <script type="text/javascript">
      // <![CDATA[
      // ]]>
    </script>
    -->
  </head>
  <body>
    <div id="container">
      <h1>$site_title</h1>
      <div id="menu">
        #include $site_path + "templates/menu.tpl"
      </div>
      <div id="content">
        <h2>Kullanıcı Kaydı</h2>

        #def printError($s)
          #if $errors.has_key($s)
            #echo """<div class="error_msg">%s</div>""" % ($errors[$s])
          #end if
        #end def

        #def printValue($s, $t='')
          #if not $errors.has_key($s) and $posted_values.has_key($s)
            #echo $posted_values[$s]
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
          <fieldset>
            <button type="submit" name="register" value="1">Kayıt</button>
          </fieldset>
        </form>
      </div>
    </div>
  </body>
</html>
