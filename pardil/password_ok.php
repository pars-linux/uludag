<?php

  require('sys/sys.session.php');

  require('class/class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Create Temporary Password');
  $obj_page = new template('tpl/tpl.password_ok.php');
  $obj_page->setvar('bln_mail', !isset($_GET['nomail']));
  $obj_page->flush();
?>
