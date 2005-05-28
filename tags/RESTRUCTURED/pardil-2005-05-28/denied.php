<?php

  require(dirname(__FILE__) . '/sys.common.php');
  
  require(dirname(__FILE__) . '/class/class.template.php');

  $_PCONF['title'] = getop('site_name') . ' - ' . __('Access Denied');
  $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.denied.php');
  $obj_page->flush();
?>
