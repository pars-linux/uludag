<?php

  require(dirname(__FILE__) . '/sys.common.php');

  require(dirname(__FILE__) . '/class/class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Logged Out');
  $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.logout.php');
  $obj_page->flush();
?>
