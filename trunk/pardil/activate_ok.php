<?php

  require('cfg/sys.define.php');
  require('sys/sys.gettext.php');
  require('sys/sys.database.php');
  require('sys/sys.procedures.php');
  require('sys/sys.pconf.php');

  require('class/class.template.php');

  $_PCONF['title'] = getop('site_name') . ' - ' . __('Account Activation');
  $obj_page = new template('tpl/tpl.activate_ok.php');
  $obj_page->flush();
?>
