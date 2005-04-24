<?php

  require('sys.common.php');
  
  require('class/class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Access Denied');
  $obj_page = new template('tpl/tpl.denied.php');
  $obj_page->flush();
?>
