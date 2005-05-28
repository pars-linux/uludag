<?php
  include(dirname(__FILE__) . '/tpl.header.php');
?>
      <div id="content">
        <h2><?php echo __('You Have Logged Out'); ?></h2>
        <p>
          <?php echo __('You have successfully logged out'); ?>
        </p>
        <p>
          <b>&raquo;</b> <a href="<?php echo $_PCONF['site_url']; ?>index.php"><?php echo __('Go to main page'); ?></a>
          <br/>
          <b>&raquo;</b> <a href="<?php echo $_PCONF['site_url']; ?>login.php"><?php echo __('Go to login page'); ?></a>
        </p>
      </div>
<?php
  include(dirname(__FILE__) . '/tpl.footer.php');
?>
