<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="tr">
  <head>
    <title><?php echo CONF_TITLE; ?></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" href="style.css" type="text/css" />
    <link rel="icon" type="image/png" href="favicon.png">
  </head>
  <body>
    <div id="container">
      <div id="header">
        <img src="images/logo2.png" alt="Pardil"/>
      </div>
      <div id="menubar">
        <span class="arrowL">&#171;</span>
        <span class="arrowR">&#187;</span>
        <span class="title"><?php echo CONF_TITLE; ?></span>
      </div>
      <div id="content">
        <div class="proposal">
          <p>
            <b>&raquo;</b> <a href="login.php"><?php echo _('User Login'); ?></a>
          </p>
          <p>
            <b><?php echo _('Session Information:'); ?></b>
          </p>
          <?php
            echo '<pre>';
            print_r($_PSESSION);
            echo '</pre>';
          ?>
        </div>
      </div>
      <div id="footer">
        &nbsp;
      </div>
    </div>
  </body>
</html>
