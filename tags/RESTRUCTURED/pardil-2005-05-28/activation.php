<?php

  require(dirname(__FILE__) . '/sys.common.php');

  require(dirname(__FILE__) . '/class/class.template.php');

  $int_floodcontrol_t = 10 * 60;
  $int_floodcontrol_m = 3;
  proc_floodcontrol_expire('activation', $int_floodcontrol_t);

  $arr_errors = array();
  if (isset($_POST['activation'])) {
    $mix_status = query_activation_status_e($_POST['activation_email']);
    if (proc_floodcontrol_check('activation', $_SERVER['REMOTE_ADDR']) >= $int_floodcontrol_m) {
      $arr_errors['activation_email'] = sprintf(__('You are allowed to use this form at most %1$d times in %2$d seconds.'), $int_floodcontrol_m, $int_floodcontrol_t);
    }
    elseif (getop('register_activation_required') != 'true') {
      $arr_errors['activation_email'] = __('Activation is not required.');
    }
    elseif (strlen($_POST['activation_email']) == 0) {
      $arr_errors['activation_email'] = __('E-mail address should be written.');
    }
    elseif (!preg_match('/^.+@.+(\..+)*$/', $_POST['activation_email'])) {
      $arr_errors['activation_email'] = __('E-mail address should be valid.');
    }
    elseif (!isset($arr_errors['activation_email']) && $mix_status === false) {
      $arr_errors['activation_email'] = __('E-mail address does not exist in database.');
    }
    elseif ($mix_status == 1) {
      $arr_errors['activation_email'] = __('Account is already activated.');
    }
  }


  if (isset($_POST['activation']) && count($arr_errors) == 0) {
    // Flood kayıtlarına ekle
    proc_floodcontrol_add('activation', $_SERVER['REMOTE_ADDR']);
  
    // İşlem

    $int_user = query_user_e2i($_POST['activation_email']);
    $str_code = proc_activation_renew($int_user);

    // E-posta gönderimi
    $str_subject = sprintf(__('%s Account Activation'), getop('site_name'));
    $str_url = $_PCONF['site_url'] . 'activate.php?code=' . $str_code . '&user=' . $int_user;
    $str_body = sprintf(__("Hello,\n\nTo complete your registration at %1\$s, please visit the address below:\n\n%2\$s\n\nThanks,\n%3\$s Team"), getop('site_url'), $str_url, getop('site_name'));
    $bln_mail = mail($_POST['activation_email'], $str_subject, $str_body);
      
    if ($bln_mail) {
      header('Location: activation_ok.php');
      exit;
    }
    else {
      header('Location: activation_ok.php?nomail=1');
      exit;
    }
  }
  else {
    $_PCONF['title'] = getop('site_name') . ' - ' . __('Account Activation');
    $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.activation.php');
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->flush();
  }
?>
