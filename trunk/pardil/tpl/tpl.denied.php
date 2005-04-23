<?php
  include('tpl.header.php');
?>
      <div id="menubar">
        <span class="arrowL">&#171;</span>
        <span class="arrowR">&#187;</span>
        <span class="title"><?php echo __('Access Denied'); ?></span>
      </div>
      <div id="menu">
        &nbsp;
      </div>
      <div id="content">
        <h2><?php echo __('Access Denied'); ?></h2>
        <p>
          <?php echo __('You are not allowed to perform this operation.'); ?>
        </p>
      </div>
<?php
  include('tpl.footer.php');
?>
