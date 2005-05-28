<?php

  require(dirname(__FILE__) . '/sys.common.php');

  require(dirname(__FILE__) . '/class/class.template.php');

  $_PCONF['title'] = getop('site_name') . ' - ' . __('Account Activation');
  $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.activate_ok.php');
  $obj_page->flush();
?>
