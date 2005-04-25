<?php

  require(dirname(__FILE__) . '/sys.common.php');

  require(dirname(__FILE__) . '/class/class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Registration Complete');
  $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.register_ok.php');
  $obj_page->setvar('bln_activation', (getop('register_activation_required') == 'true'));
  $obj_page->setvar('bln_mail', !isset($_GET['nomail']));
  $obj_page->flush();
?>
