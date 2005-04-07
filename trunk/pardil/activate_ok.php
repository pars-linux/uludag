<?php

  require('sys.define.php');
  require('sys.gettext.php');
  require('sys.database.php');
  require('sys.procedures.php');
  require('sys.pconf.php');

  require('class.template.php');

  $_PCONF['title'] = getop('site_name') . ' - ' . __('Account Activation');
  $obj_page = new template('tpl.activate_ok.php');
  $obj_page->flush();
?>
