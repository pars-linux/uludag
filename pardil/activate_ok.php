<?php

  require('sys.common.php');

  require('class/class.template.php');

  $_PCONF['title'] = getop('site_name') . ' - ' . __('Account Activation');
  $obj_page = new template('tpl/tpl.activate_ok.php');
  $obj_page->flush();
?>
