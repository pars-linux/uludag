<?php

  require('sys.define.php');
  require('sys.gettext.php');
  require('sys.database.php');
  require('sys.procedures.php');
  require('sys.pconf.php');

  require('class.template.php');

  $arr_errors = array();
  if (isset($_POST['register'])) {
    if (strlen($_POST['register_name']) == 0) {
      $arr_errors['register_name'] = __('Real name should be written.');
    }
    
    if (strlen($_POST['register_username']) == 0) {
      $arr_errors['register_username'] = __('Username should be written.');
    }
    else {
      $mix_userno = database_query_scalar(sprintf('SELECT id FROM users WHERE username="%s"', addslashes($_POST['register_username'])));
      if ($mix_userno !== false) {
        $arr_errors['register_username'] = __('Username is in use.');
      }
    }
    
    if (strlen($_POST['register_password']) == 0 || strlen($_POST['register_password2']) == 0) {
      $arr_errors['register_password'] = __('Password should be written twice.');
    }
    elseif ($_POST['register_password'] != $_POST['register_password2']) {
      $arr_errors['register_password'] = __('Passwords should be same.');
    }

    if (strlen($_POST['register_email']) == 0) {
      $arr_errors['register_email'] = __('E-mail address should be written.');
    }
    elseif (!preg_match('/^.+@.+(\..+)*$/', $_POST['register_email'])) {
      $arr_errors['register_email'] = __('E-mail address should be valid.');
    }
  }


  if (isset($_POST['register']) && count($arr_errors) == 0) {
    // İşlem

    $int_status = (proc_getopt('register_activation_required') == 'true') ? 0 : 1;
    $int_user = proc_user_new($_POST['register_username'], md5($_POST['register_password']), $_POST['register_email'], $_POST['register_name'], 1);
    $str_code = proc_activation_new($int_user, $int_status, );

    if ($int_status == 0) {
      // E-posta gönderimi
      $str_subject = sprintf(__('%s Account Activation'), CONF_NAME);
      $str_url = $_PCONF['site_url'] . '/activate.php?code=' . $str_code . '&user=' . $int_user;
      $str_body = sprintf(__("Hello,\nTo complete your registration at %1$s, please visit the address below:\n\n%2$s\n\nThanks,\n%3$s Team"), $_PCONF['site_url'], $str_url, $_PCONF['site_name']);
      $bln_mail = mail($_POST['register_email'], $str_subject, $str_body);
      
      if ($bln_mail) {
        header('Location: register_ok.php');
        exit;
      }
      else {
        header('Location: register_ok.php?nomail=1');
        exit;
      }
    }
  }
  else {
    $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('User Registration');
    $obj_page = new template('tpl.register.php');
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->flush();
  }
?>
