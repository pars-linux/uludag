<?php
  include('tpl.header.php');
?>
      <div id="content">
        <form action="login.php" method="post">
          <fieldset>
            <label for=""><?php echo __('Username:'); ?></label>
            <br/>
            <input type="text" name="username" size="25" value="<?php echo (!isset($arr_errors['username'])) ? htmlspecialchars($_POST['username'], ENT_QUOTES) : ''; ?>" />
            <br/>
            <?php print_error('<div class="error">%s</div>', 'username'); ?>
            <br/>
            <label for=""><?php echo __('Password:'); ?></label>
            <br/>
            <input type="password" name="password" size="25" value="<?php echo (!isset($arr_errors['password'])) ? htmlspecialchars($_POST['password'], ENT_QUOTES) : ''; ?>" />
            <br/>
            <?php print_error('<div class="error">%s</div>', 'password'); ?>
            <br/>
            <button type="submit" name="login" value="1"><b><?php echo __('Login &raquo;'); ?></b></button>
            <p>
              <b>&raquo;</b> <a href="password.php"><?php echo __('Forgot your password?'); ?></a>
              <br/>
              <b>&raquo;</b> <a href="activation.php"><?php echo __('Need activation?'); ?></a>
              <br/>
              <b>&raquo;</b> <a href="register.php"><?php echo __('Not a registered user?'); ?></a>
            </p>
          </fieldset>
        </form>
      </div>
<?php
  include('tpl.footer.php');
?>
