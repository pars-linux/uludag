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
        <span class="title"><?php echo __('Installination'); ?></span>
      </div>
      <div id="content">
        <div class="proposal">
          <form action="install.php" method="post">
            <fieldset>
              <input type="hidden" name="install" value="1"/>
              <table class="form">
                <tr>
                  <td class="label"><?php echo __('MySQL Host:'); ?></td>
                  <td>
                    <input type="text" name="install_mysql_host" size="25" value="<?php echo (!isset($arr_errors['install_mysql_host'])) ? htmlspecialchars($_POST['install_mysql_host'], ENT_QUOTES) : ''; ?>" />
                  </td>
                </tr>
                <?php print_error('install_mysql_host'); ?>
                <tr>
                  <td class="label"><?php echo __('MySQL User:'); ?></td>
                  <td>
                    <input type="text" name="install_mysql_user" size="25" value="<?php echo (!isset($arr_errors['install_mysql_user'])) ? htmlspecialchars($_POST['install_mysql_user'], ENT_QUOTES) : ''; ?>" />
                  </td>
                </tr>
                <?php print_error('install_mysql_user'); ?>
                <tr>
                  <td class="label"><?php echo __('MySQL Password:'); ?></td>
                  <td>
                    <input type="text" name="install_mysql_password" size="25" value="<?php echo (!isset($arr_errors['install_mysql_password'])) ? htmlspecialchars($_POST['install_mysql_password'], ENT_QUOTES) : ''; ?>" />
                  </td>
                </tr>
                <?php print_error('install_mysql_password'); ?>
                <tr>
                  <td class="label"><?php echo __('MySQL Database:'); ?></td>
                  <td>
                    <input type="text" name="install_mysql_database" size="25" value="<?php echo (!isset($arr_errors['install_mysql_database'])) ? htmlspecialchars($_POST['install_mysql_database'], ENT_QUOTES) : ''; ?>" />
                  </td>
                </tr>
                <?php print_error('install_mysql_database'); ?>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td class="label"><?php echo __('Site Name:'); ?></td>
                  <td>
                    <input type="text" name="install_site_name" size="25" value="<?php echo (!isset($arr_errors['install_site_name'])) ? htmlspecialchars($_POST['install_site_name'], ENT_QUOTES) : ''; ?>" />
                  </td>
                </tr>
                <?php print_error('install_site_name'); ?>
                <tr>
                  <td class="label"><?php echo __('Site Title:'); ?></td>
                  <td>
                    <input type="text" name="install_site_title" size="25" value="<?php echo (!isset($arr_errors['install_site_title'])) ? htmlspecialchars($_POST['install_site_title'], ENT_QUOTES) : ''; ?>" />
                  </td>
                </tr>
                <?php print_error('install_site_url'); ?>
                <tr>
                  <td class="label"><?php echo __('Site URL:'); ?></td>
                  <td>
                    <input type="text" name="install_site_url" size="25" value="<?php echo (!isset($arr_errors['install_site_url'])) ? htmlspecialchars($_POST['install_site_url'], ENT_QUOTES) : ''; ?>" />
                  </td>
                </tr>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td><?php printf(__("Recommended: %s"), 'http://' . $_SERVER['SERVER_NAME'] . dirname($_SERVER['REQUEST_URI'])); ?></td>
                </tr>
                <?php print_error('install_site_url'); ?>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td class="label"><?php echo __('Admin Password:'); ?></td>
                  <td>
                    <input type="text" name="install_admin_password" size="25" value="<?php echo (!isset($arr_errors['install_admin_password'])) ? htmlspecialchars($_POST['install_admin_password'], ENT_QUOTES) : ''; ?>" />
                  </td>
                </tr>
                <?php print_error('install_admin_password'); ?>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td class="info">
                    <button type="submit"><b><?php echo __('Install &raquo;'); ?></b></button>
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
