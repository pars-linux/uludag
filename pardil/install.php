<?php

  require('cfg/sys.define.php');
  require('sys/sys.gettext.php');
  require('sys/sys.database.php');
  require('sys/sys.procedures.php');
  require('sys/sys.pconf.php');

  require('class/class.template.php');

  $arr_errors = array();
  if (isset($_POST['install'])) {
  }


  if (isset($_POST['install']) && count($arr_errors) == 0) {
    // İşlem

  }
  else {
    $_PCONF['title'] = getop('site_name') . ' - ' . __('Installination');
    $obj_page = new template('tpl/tpl.install.php');
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->flush();
  }
?>
