<?php

  require(dirname(__FILE__) . '/sys/sys.session.php');

  require(dirname(__FILE__) . '/class/class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Create Temporary Password');
  $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.password_ok.php');
  $obj_page->setvar('bln_mail', !isset($_GET['nomail']));
  $obj_page->flush();
?>
