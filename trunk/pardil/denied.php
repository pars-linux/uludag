<?php
  require('sys.define.php');
  require('sys.gettext.php');
  require('sys.database.php');
  require('sys.procedures.php');
  require('sys.pconf.php');
  require('sys.session.php');
  
  require('class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Access Denied');
  $obj_page = new template('tpl.denied.php');
  $obj_page->flush();
?>
