<?php
  require('cfg/sys.define.php');
  require('sys/sys.gettext.php');
  require('sys/sys.database.php');
  require('sys/sys.procedures.php');
  require('sys/sys.pconf.php');
  require('sys/sys.session.php');
  
  require('class/class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Proposal Not Found');
  $obj_page = new template('tpl/tpl.notfound.php');
  $obj_page->flush();
?>
