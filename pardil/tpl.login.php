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

  include('tpl.header.php');
?>
      <div id="menubar">
        <span class="arrowL">&#171;</span>
        <span class="arrowR">&#187;</span>
        <span class="title"><?php echo _('User Login'); ?></span>
      </div>
      <div id="content">
        <div class="proposal">
          <form action="login.php" method="post">
            <fieldset>
              <input type="hidden" name="login" value="1"/>
              <table class="form">
                <tr>
                  <td class="label"><?php echo _('Username:'); ?></td>
                  <td>
                    <input type="text" name="username" size="25" value="<?php echo (!isset($arr_errors['username'])) ? htmlspecialchars($_POST['username'], ENT_QUOTES) : ''; ?>" />
                  </td>
                </tr>
                <?php print_error('username'); ?>
                <tr>
                  <td class="label"><?php echo _('Password:'); ?></td>
                  <td>
                    <input type="password" name="password" size="25" value="<?php echo (!isset($arr_errors['password'])) ? htmlspecialchars($_POST['password'], ENT_QUOTES) : ''; ?>" />
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
                    <b>&raquo;</b> <a href="register.php"><?php echo _('Not registered?'); ?></a>
                  </td>
                </tr>
              </table>
            </fieldset>
          </form>
        </div>
      </div>
<?php
  include('tpl.footer.php');
?>
