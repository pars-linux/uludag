<?php
  include('tpl.header.php');
?>
      <div id="menubar">
        <span class="arrowL">&#171;</span>
        <span class="arrowR">&#187;</span>
        <span class="title"><?php echo __('Logged Out'); ?></span>
      </div>
      <div id="content">
        <div class="proposal">
          <h2><?php echo __('You Have Logged Out'); ?></h2>
          <p>
            <?php echo __('You have successfully logged out'); ?>
          </p>
          <p>
            <b>&raquo;</b> <a href="index.php"><?php echo __('Go to main page'); ?></a>
            <br/>
            <b>&raquo;</b> <a href="login.php"><?php echo __('Go to login page'); ?></a>
          </p>
        </div>
      </div>
<?php
  include('tpl.footer.php');
?>
