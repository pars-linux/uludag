<?php
  include('tpl.header.php');
?>
      <div id="menubar">
        <span class="arrowL">&#171;</span>
        <span class="arrowR">&#187;</span>
        <span class="title"><?php echo __('Account Activation'); ?></span>
      </div>
      <div id="menu">
        &nbsp;
      </div>
      <div id="content">
        <p>
          <?php print_error('%s', 'activation_code'); ?>
        </p>
      </div>
<?php
  include('tpl.footer.php');
?>
