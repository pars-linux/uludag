<?php

  require('sys.common.php');

  require('class/class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Logged Out');
  $obj_page = new template('tpl/tpl.logout.php');
  $obj_page->flush();
?>
