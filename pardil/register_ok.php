<?php

  require('sys.define.php');
  require('sys.gettext.php');
  require('sys.database.php');
  require('sys.procedures.php');
  require('sys.pconf.php');

  require('class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Registration Complete');
  $obj_page = new template('tpl.register_ok.php');
  $obj_page->setvar('bln_activation', (getop('register_activation_required') == 'true'));
  $obj_page->setvar('bln_mail', !isset($_GET['nomail']));
  $obj_page->flush();
?>
