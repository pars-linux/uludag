<?php
  include(dirname(__FILE__) . '/tpl.header.php');
?>
      <div id="content">
        <h2><?php echo __('Account Activated'); ?></h2>
        <p>
          <?php echo __('Your registration is now complete.'); ?>
        </p>
        <p>
          <b>&raquo;</b> <a href="<?php echo $_PCONF['site_url']; ?>login.php"><?php echo __('Go to login page'); ?></a>
        </p>
      </div>
<?php
  include(dirname(__FILE__) . '/tpl.footer.php');
?>
