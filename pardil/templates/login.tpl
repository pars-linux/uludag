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
        <h2>Kullanıcı Girişi</h2>

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

        #if $status == 'done'
          <p>Kullanıcı girişi başarılı.</p>
        #else:
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
            <button type="submit" name="login" value="1">Giriş</button>
          </fieldset>
        </form>
        #end if
      </div>
    </div>
  </body>
</html>
