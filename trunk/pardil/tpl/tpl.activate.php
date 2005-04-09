<?php
  function print_error($str_name, $str_sub='') {
    global $arr_errors;
    if (isset($arr_errors[$str_name])) {
      printf('%s', $arr_errors[$str_name]);
    }
  }
  
  include('tpl.header.php');
?>
      <div id="menubar">
        <span class="arrowL">&#171;</span>
        <span class="arrowR">&#187;</span>
        <span class="title"><?php echo __('Account Activation'); ?></span>
      </div>
      <div id="content">
        <div class="proposal">
          <p>
            <?php print_error('activation_code'); ?>
          </p>
        </div>
      </div>
<?php
  include('tpl.footer.php');
?>
