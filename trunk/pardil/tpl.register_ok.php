<?php
  include('tpl.header.php');
?>
      <div id="menubar">
        <span class="arrowL">&#171;</span>
        <span class="arrowR">&#187;</span>
        <span class="title"><?php echo _('Registration Complete'); ?></span>
      </div>
      <div id="content">
        <div class="proposal">
          <h2><?php echo _('Registration Complete'); ?></h2>
          <p>
            <?php echo _('You\'ve successfully registered.'); ?>
          </p>
          <?php if ($bln_activation) { ?>
          <p>
            <?php echo _('You need to activate your account by clicking (or visiting) the URL sent to your e-mail address.'); ?>
          </p>
          <?php } ?>
          <p>
            <b>&raquo;</b> <a href="login.php"><?php echo _('Go to login page'); ?></a>
          </p>
        </div>
      </div>
<?php
  include('tpl.footer.php');
?>
