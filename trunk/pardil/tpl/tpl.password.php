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
        <span class="title"><?php echo __('Create Temporary Password'); ?></span>
      </div>
      <div id="content">
        <div class="proposal">
          <p>
            <?php __e('In this page, you can create a temporary password. With this temporary password, you can login to your account to change your primary password.'); ?>
          </p>
          <p>
            <?php printf(__('This temporary password does not effect your primary password, and will be disabled after %d seconds.'), getop('temp_password_timeout')); ?>
          </p>
          <form action="password.php" method="post">
            <fieldset>
              <input type="hidden" name="password" value="1"/>
              <table class="form">
                <tr>
                  <td class="label"><?php echo __('E-Mail Address:'); ?></td>
                  <td>
                    <input type="text" name="password_email" size="25" value="" />
                  </td>
                </tr>
                <?php print_error('password_email'); ?>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td class="info">
                    <button type="submit"><b><?php echo __('Submit &raquo;'); ?></b></button>
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
