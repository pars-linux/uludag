<?php

  require('sys.common.php');

  require('class/class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Profile Update Complete');
  $obj_page = new template('tpl/tpl.profile_ok.php');
  $obj_page->setvar('bln_activation', isset($_GET['activation']));
  $obj_page->setvar('bln_mail', !isset($_GET['nomail']));
  $obj_page->flush();
?>
