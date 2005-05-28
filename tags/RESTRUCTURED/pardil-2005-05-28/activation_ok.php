<?php

  require(dirname(__FILE__) . '/sys.common.php');

  require(dirname(__FILE__) . '/class/class.template.php');

  $_PCONF['title'] = getop('site_name') . ' - ' . __('Account Activation');
  $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.activation_ok.php');
  $obj_page->setvar('bln_mail', !isset($_GET['nomail']));
  $obj_page->flush();
?>
