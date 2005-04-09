<?php
  include('tpl.header.php');
?>
      <div id="menubar">
        <span class="arrowL">&#171;</span>
        <span class="arrowR">&#187;</span>
        <span class="title"><?php echo __('Account Activation'); ?></span>
      </div>
      <div id="content">
        <div class="proposal">
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
            <b>&raquo;</b> <a href="login.php"><?php echo __('Go to login page'); ?></a>
          </p>
        </div>
      </div>
<?php
  include('tpl.footer.php');
?>
