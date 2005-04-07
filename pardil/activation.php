<?php

  require('sys.define.php');
  require('sys.gettext.php');
  require('sys.database.php');
  require('sys.procedures.php');
  require('sys.pconf.php');

  require('class.template.php');

  $arr_errors = array();
  if (isset($_POST['activation'])) {
    if (strlen($_POST['activation_email']) == 0) {
      $arr_errors['activation_email'] = __('E-mail address should be written.');
    }
    elseif (!preg_match('/^.+@.+(\..+)*$/', $_POST['activation_email'])) {
      $arr_errors['activation_email'] = __('E-mail address should be valid.');
    }
    if (getop('register_activation_required') != 'true') {
      $arr_errors['activation_email'] = __('Activation is not required.');
    }
    
    $mix_status = database_query_scalar(sprintf('SELECT status FROM activation INNER JOIN users ON users.id = activation.user WHERE users.email="%s"', addslashes($_POST['activation_email'])));
    if (!isset($arr_errors['activation_email']) && $mix_status === false) {
      $arr_errors['activation_email'] = __('E-mail address does not exist in database.');
    }
    elseif ($mix_status == 1) {
      $arr_errors['activation_email'] = __('Account is already activated.');
    }
  }


  if (isset($_POST['activation']) && count($arr_errors) == 0) {
    // İşlem

    $int_user = database_query_scalar(sprintf('SELECT id FROM users WHERE email="%s"', addslashes($_POST['activation_email'])));
    $str_code = proc_activation_renew($int_user);

    // E-posta gönderimi
    $str_subject = sprintf(__('%s Account Activation'), getop('site_name'));
    $str_url = $_PCONF['site_url'] . '/activate.php?code=' . $str_code . '&user=' . $int_user;
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
    $obj_page = new template('tpl.activation.php');
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->flush();
  }
?>
