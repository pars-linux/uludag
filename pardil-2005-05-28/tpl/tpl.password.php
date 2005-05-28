<?php
  include(dirname(__FILE__) . '/tpl.header.php');
?>
      <div id="content">
        <p>
          <?php __e('In this page, you can create a temporary password. With this temporary password, you can login to your account to change your primary password.'); ?>
        </p>
        <p>
          <?php printf(__('This temporary password does not effect your primary password, and will be disabled after %d seconds.'), getop('temp_password_timeout')); ?>
        </p>
        <form action="<?php echo $_PCONF['site_url']; ?>password.php" method="post">
          <fieldset>
            <label for=""><?php echo __('E-Mail Address:'); ?></label>
            <br/>
            <input type="text" name="password_email" size="25" value="" />
            <br/>
            <?php print_error('<div class="error">%s</div>', 'password_email'); ?>
            <br/>
            <button type="submit" name="password" value="1"><b><?php echo __('Submit &raquo;'); ?></b></button>
          </fieldset>
        </form>
      </div>
<?php
  include(dirname(__FILE__) . '/tpl.footer.php');
?>
