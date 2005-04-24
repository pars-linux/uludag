<?php

  require('sys.common.php');

  require('class/class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Registration Complete');
  $obj_page = new template('tpl/tpl.register_ok.php');
  $obj_page->setvar('bln_activation', (getop('register_activation_required') == 'true'));
  $obj_page->setvar('bln_mail', !isset($_GET['nomail']));
  $obj_page->flush();
?>
