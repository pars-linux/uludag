<?php
  include('tpl.header.php');
?>
      <div id="menubar">
        <span class="arrowL">&#171;</span>
        <span class="arrowR">&#187;</span>
        <span class="title"><?php echo CONF_TITLE; ?></span>
      </div>
      <div id="content">
        <div class="proposal">
          <p>
            <b>&raquo;</b> <a href="login.php"><?php echo __('User Login'); ?></a>
          </p>
          <p>
            <b><?php echo __('Session Information:'); ?></b>
          </p>
          <?php
            echo '<pre>';
            print_r($_PSESSION);
            echo '</pre>';
          ?>
        </div>
      </div>
<?php
  include('tpl.footer.php');
?>
