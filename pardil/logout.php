<?php

  require('sys.define.php');
  require('sys.gettext.php');
  require('sys.database.php');
  require('sys.procedures.php');
  require('sys.pconf.php');

  require('class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Logged Out');
  $obj_page = new template('tpl.logout.php');
  $obj_page->flush();
?>
