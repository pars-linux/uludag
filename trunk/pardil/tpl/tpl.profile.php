<?php
  include('tpl.header.php');
?>
      <div id="content">
        <form action="profile.php" method="post">
          <fieldset>
            <?php if ($bln_first) { ?>
              <label for=""><?php echo __('Name:'); ?></label>
              <br/>
              <input type="text" name="profile_name" size="25" value="<?php echo htmlspecialchars($arr_user['name'], ENT_QUOTES); ?>" />
              <br/>
              <br/>
              <label for=""><?php echo __('E-Mail Address:'); ?></label>
              <br/>
              <input type="text" name="profile_email" size="25" value="<?php echo htmlspecialchars($arr_user['email'], ENT_QUOTES); ?>" />
              <br/>
              <br/>
              <label for=""><?php echo __('Password:'); ?></label>
              <br/>
              <input type="password" name="profile_password" size="25" value="" />
              <br/>
              <input type="password" name="profile_password2" size="25" value="" />
              <br/>
              <div class="info"><?php echo __('If you don\'t want to change your password, leave these two fields empty.'); ?></div>
              <br/>
              <br/>
            <?php } else { ?>
              <label for=""><?php echo __('Name:'); ?></label>
              <br/>
              <input type="text" name="profile_name" size="25" value="<?php echo (!isset($arr_errors['profile_name'])) ? htmlspecialchars($_POST['profile_name'], ENT_QUOTES) : ''; ?>" />
              <br/>
              <?php print_error('<div class="error">%s</div>', 'profile_name'); ?>
              <br/>
              <label for=""><?php echo __('E-Mail Address:'); ?></label>
              <br/>
              <input type="text" name="profile_email" size="25" value="<?php echo (!isset($arr_errors['profile_email'])) ? htmlspecialchars($_POST['profile_email'], ENT_QUOTES) : ''; ?>" />
              <br/>
              <?php print_error('<div class="error">%s</div>', 'profile_email'); ?>
              <br/>
              <label for=""><?php echo __('Password:'); ?></label>
              <br/>
              <input type="password" name="profile_password" size="25" value="<?php echo (!isset($arr_errors['profile_password'])) ? htmlspecialchars($_POST['profile_password'], ENT_QUOTES) : ''; ?>" />
              <br/>
              <input type="password" name="profile_password2" size="25" value="<?php echo (!isset($arr_errors['profile_password'])) ? htmlspecialchars($_POST['profile_password'], ENT_QUOTES) : ''; ?>" />
              <br/>
              <div class="info"><?php echo __('If you don\'t want to change your password, leave these two fields empty.'); ?></div>
              <?php print_error('<div class="error">%s</div>', 'profile_password'); ?>
              <br/>
            <?php } ?>
            <button type="submit" name="profile" value="1"><?php echo __('Update &raquo;'); ?></button>
          </fieldset>
        </form>
      </div>
<?php
  include('tpl.footer.php');
?>
