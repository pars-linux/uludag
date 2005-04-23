<?php
  include('tpl.header.php');
?>
      <div id="menubar">
        <span class="arrowL">&#171;</span>
        <span class="arrowR">&#187;</span>
        <span class="title"><?php echo __('User Registration'); ?></span>
      </div>
      <div id="menu">
        &nbsp;
      </div>
      <div id="content">
        <form action="register.php" method="post">
          <fieldset>
            <label for=""><?php echo __('Name:'); ?></label>
            <br/>
            <input type="text" name="register_name" size="25" value="<?php echo (!isset($arr_errors['register_name'])) ? htmlspecialchars($_POST['register_name'], ENT_QUOTES) : ''; ?>" />
            <br/>
            <?php print_error('<div class="error">%s</div>', 'register_name'); ?>
            <br/>
            <label for=""><?php echo __('Username:'); ?></label>
            <br/>
            <input type="text" name="register_username" size="25" value="<?php echo (!isset($arr_errors['register_username'])) ? htmlspecialchars($_POST['register_username'], ENT_QUOTES) : ''; ?>" />
            <br/>
            <?php print_error('<div class="error">%s</div>', 'register_username'); ?>
            <br/>
            <label for=""><?php echo __('E-Mail Address:'); ?></label>
            <br/>
            <input type="text" name="register_email" size="25" value="<?php echo (!isset($arr_errors['register_email'])) ? htmlspecialchars($_POST['register_email'], ENT_QUOTES) : ''; ?>" />
            <br/>
            <?php print_error('<div class="error">%s</div>', 'register_email'); ?>
            <br/>
            <label for=""><?php echo __('Password:'); ?></label>
            <br/>
            <input type="password" name="register_password" size="25" value="<?php echo (!isset($arr_errors['register_password'])) ? htmlspecialchars($_POST['register_password'], ENT_QUOTES) : ''; ?>" />
            <br/>
            <input type="password" name="register_password2" size="25" value="<?php echo (!isset($arr_errors['register_password'])) ? htmlspecialchars($_POST['register_password'], ENT_QUOTES) : ''; ?>" />
            <br/>
            <?php print_error('<div class="error">%s</div>', 'register_password'); ?>
            <br/>
            <button type="submit" name="register" value="1"><?php echo __('Register &raquo;'); ?></button>
          </fieldset>
        </form>
      </div>
<?php
  include('tpl.footer.php');
?>
