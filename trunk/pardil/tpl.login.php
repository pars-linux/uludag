<?php
  function print_error($str_name, $str_sub='') {
    global $arr_errors;
    if ($str_sub == '') {
      if (isset($arr_errors[$str_name])) {
        printf('<tr><td class="label">&nbsp;</td><td class="error">%s</td></tr>', $arr_errors[$str_name]);
      }
    }
    else {
      if (isset($arr_errors[$str_name][$str_sub])) {
        printf('<tr><td class="label">&nbsp;</td><td class="error">%s</td></tr>', $arr_errors[$str_name][$str_sub]);
      }
    }
  }
?>
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="tr">
  <head>
    <title><?php echo _('User Login'); ?></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" href="style.css" type="text/css" />
  </head>
  <body>
    <div id="container">
      <div id="header">
        <img src="images/logo2.png" alt="Pardil"/>
      </div>
      <div id="menubar">
        <span class="arrowL">&#171;</span>
        <span class="arrowR">&#187;</span>
        <span class="title"><?php echo _('User Login'); ?></span>
      </div>
      <div id="content">
        <div class="proposal">
          <form action="login.php" method="post">
            <input type="hidden" name="login" value="1"/>
            <table class="form">
              <tr>
                <td class="label"><?php echo _('Username:'); ?></td>
                <td>
                  <input type="text" name="username" size="25" />
                </td>
              </tr>
              <?php print_error('username'); ?>
              <tr>
                <td class="label"><?php echo _('Password:'); ?></td>
                <td>
                  <input type="password" name="password" size="25" />
                </td>
              </tr>
              <?php print_error('password'); ?>
              <tr>
                <td class="label">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td class="label">&nbsp;</td>
                <td class="info">
                  <button type="submit"><b><?php echo _('Login &raquo;'); ?></b></button>
                </td>
              </tr>
              <tr>
                <td class="label">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td class="label">&nbsp;</td>
                <td>
                  <b>&raquo;</b> <a href="#"><?php echo _('Forgot your password?'); ?></a>
                  <br/>
                  <b>&raquo;</b> <a href="#"><?php echo _('Not registered?'); ?></a>
                </td>
              </tr>
            </table>
          </form>
        </div>
      </div>
      <div id="footer">
        &nbsp;
      </div>
    </div>
  </body>
</html>
