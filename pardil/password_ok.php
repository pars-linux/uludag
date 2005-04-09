<?php

  require('cfg/sys.define.php');
  require('sys/sys.gettext.php');
  require('sys/sys.database.php');
  require('sys/sys.procedures.php');
  require('sys/sys.pconf.php');

  require('class/class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Create Temporary Password');
  $obj_page = new template('tpl/tpl.password_ok.php');
  $obj_page->setvar('bln_mail', !isset($_GET['nomail']));
  $obj_page->flush();
?>
