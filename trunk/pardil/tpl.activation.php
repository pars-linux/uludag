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
        <span class="title"><?php echo __('Account Activation'); ?></span>
      </div>
      <div id="content">
        <div class="proposal">
          <form action="activation.php" method="post">
            <fieldset>
              <input type="hidden" name="activation" value="1"/>
              <table class="form">
                <tr>
                  <td class="label"><?php echo __('E-Mail Address:'); ?></td>
                  <td>
                    <input type="text" name="activation_email" size="25" value="" />
                  </td>
                </tr>
                <?php print_error('activation_email'); ?>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td class="info">
                    <button type="submit"><b><?php echo __('Request Code &raquo;'); ?></b></button>
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
