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
        <span class="title"><?php echo _('User Registration'); ?></span>
      </div>
      <div id="content">
        <div class="proposal">
          <form action="register.php" method="post">
            <fieldset>
              <input type="hidden" name="register" value="1"/>
              <table class="form">
                <tr>
                  <td class="label"><?php echo _('Name:'); ?></td>
                  <td>
                    <input type="text" name="register_name" size="25" value="<?php echo (!isset($arr_errors['register_name'])) ? htmlspecialchars($_POST['register_name'], ENT_QUOTES) : ''; ?>" />
                  </td>
                </tr>
                <?php print_error('register_name'); ?>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td class="label"><?php echo _('Username:'); ?></td>
                  <td>
                    <input type="text" name="register_username" size="25" value="<?php echo (!isset($arr_errors['register_username'])) ? htmlspecialchars($_POST['register_username'], ENT_QUOTES) : ''; ?>" />
                  </td>
                </tr>
                <?php print_error('register_username'); ?>
                <tr>
                  <td class="label"><?php echo _('E-Mail Address:'); ?></td>
                  <td>
                    <input type="text" name="register_email" size="25" value="<?php echo (!isset($arr_errors['register_email'])) ? htmlspecialchars($_POST['register_email'], ENT_QUOTES) : ''; ?>" />
                  </td>
                </tr>
                <?php print_error('register_email'); ?>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td class="label"><?php echo _('Password:'); ?></td>
                  <td>
                    <input type="password" name="register_password" size="25" value="<?php echo (!isset($arr_errors['register_password'])) ? htmlspecialchars($_POST['register_password'], ENT_QUOTES) : ''; ?>" />
                  </td>
                </tr>
                <tr>
                  <td class="label"><?php echo _('Password (again):'); ?></td>
                  <td>
                    <input type="password" name="register_password2" size="25" value="<?php echo (!isset($arr_errors['register_password'])) ? htmlspecialchars($_POST['register_password'], ENT_QUOTES) : ''; ?>" />
                  </td>
                </tr>
                <?php print_error('register_password'); ?>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td class="info">
                    <button type="submit"><b><?php echo _('Register &raquo;'); ?></b></button>
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
