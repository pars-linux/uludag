<?php
  include(dirname(__FILE__) . '/tpl.header.php');
?>
      <div id="content">
        <h2><?php echo __('Activation Code Sent'); ?></h2>
        <?php if ($bln_mail) { ?>
        <p>
          <?php echo __('You need to activate your account by clicking (or visiting) the URL sent to your e-mail address.'); ?>
        </p>
        <?php } else { ?>
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
