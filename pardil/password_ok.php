<?php

  require('sys.define.php');
  require('sys.gettext.php');
  require('sys.database.php');
  require('sys.procedures.php');
  require('sys.pconf.php');

  require('class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Change Password');
  $obj_page = new template('tpl.password_ok.php');
  $obj_page->setvar('bln_mail', !isset($_GET['nomail']));
  $obj_page->flush();
?>
