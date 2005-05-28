<?php
  include(dirname(__FILE__) . '/tpl.header.php');
?>
      <div id="content">
        <h2><?php echo __('Registration Complete'); ?></h2>
        <p>
          <?php echo __('You\'ve successfully registered.'); ?>
        </p>
        <?php if ($bln_activation && $bln_mail) { ?>
        <p>
          <?php echo __('You need to activate your account by clicking (or visiting) the URL sent to your e-mail address.'); ?>
        </p>
        <?php } elseif ($bln_activation && !$bln_mail) { ?>
        <p>
          <?php echo __('A problem occured in our mail server while sending your activation code. Please contact server administrator.'); ?>
        </p>
        <?php } ?>
        <p>
          <b>&raquo;</b> <a href="<?php echo $_PCONF['site_url']; ?>login.php"><?php echo __('Go to login page'); ?></a>
        </p>
      </div>
<?php
  include(dirname(__FILE__) . '/tpl.footer.php');
?>
