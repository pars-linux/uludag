<?php

  require(dirname(__FILE__) . '/sys.common.php');

  require(dirname(__FILE__) . '/class/class.template.php');

  $arr_errors = array();
  if (isset($_GET['code'])) {
    if (!isset($_GET['user']) || strlen($_GET['code']) != 32) {
      $arr_errors['activation_code'] = __('Invalid activation data. Please double check URL.');
    }
    $mix_status = query_activation_status_uc($_GET['user'], $_GET['code']);
    if ($mix_status === false) {
      $arr_errors['activation_code'] = __('Activation code is not valid.');
    }
    elseif ($mix_status == 1) {
      $arr_errors['activation_code'] = __('Account is already activated.');
    }
  }


  if (isset($_GET['code']) && isset($_GET['user']) && strlen($_GET['code']) == 32 && count($arr_errors) == 0) {
    // İşlem
    proc_activation_update($_GET['user'], 1);
    header('Location: activate_ok.php');
    exit;
  }
  else {
    $_PCONF['title'] = getop('site_name') . ' - ' . __('Account Activation');
    $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.activate.php');
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->flush();
  }
?>
