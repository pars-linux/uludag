<?php
  include(dirname(__FILE__) . '/tpl.header.php');
?>
      <div id="content">
        <h2><?php echo __('Profile Update Complete'); ?></h2>
        <p>
          <?php echo __('You\'ve successfully updated your profile.'); ?>
        </p>
        <?php if ($bln_activation && $bln_mail) { ?>
        <p>
          <?php echo __('You need to activate your account by clicking (or visiting) the URL sent to your new e-mail address.'); ?>
        </p>
        <?php } elseif ($bln_activation && !$bln_mail) { ?>
        <p>
          <?php echo __('A problem occured in our mail server while sending your activation code. Please contact server administrator.'); ?>
        </p>
        <?php } ?>
        <p>
          <b>&raquo;</b> <a href="<?php echo $_PCONF['site_url']; ?>index.php"><?php echo __('Go to main page'); ?></a>
        </p>
      </div>
<?php
  include(dirname(__FILE__) . '/tpl.footer.php');
?>
