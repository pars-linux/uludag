<?php

  require('sys.define.php');
  require('sys.gettext.php');
  require('sys.database.php');
  require('sys.procedures.php');
  require('sys.pconf.php');

  require('class.template.php');

  $arr_errors = array();

  if (isset($_POST['password'])) {
    if (strlen($_POST['password_email']) == 0) {
      $arr_errors['password_email'] = __('E-mail address should be written.');
    }
    elseif (!preg_match('/^.+@.+(\..+)*$/', $_POST['password_email'])) {
      $arr_errors['password_email'] = __('E-mail address should be valid.');
    }
    else {
      $mix_userno = database_query_scalar(sprintf('SELECT id FROM users WHERE email="%s"', addslashes($_POST['password_email'])));
      if ($mix_userno === false) {
        $arr_errors['password_email'] = __('E-mail address not found in database.');
      }
    }
  }

  if (isset($_POST['password']) && count($arr_errors) == 0) {
    // İşlem
    $int_userno = database_query_scalar(sprintf('SELECT id FROM users WHERE email="%s"', addslashes($_POST['password_email'])));
    $str_code = proc_password_new($int_userno);
    
    $str_subject = sprintf(__('%s Temporary Password'), $_PCONF['site_name']);
    $str_body = sprintf(__("Hello,\n\nYou have requested a temporary password for your account at %1\$s.\n\nYour temporary password is: %2\$s\n\nThis temporary password does not effect your primary password.\n\nThanks,\n%3\$s Team"), $_PCONF['site_url'], $str_code, $_PCONF['site_name']);
    $bln_mail = mail($_POST['password_email'], $str_subject, $str_body);
      
    if ($bln_mail) {
      header('Location: password_ok.php');
      exit;
    }
    else {
      header('Location: password_ok.php?nomail=1');
      exit;
    }
  }
  else {
    $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Create Temporary Password');
    $obj_page = new template('tpl.password.php');
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->flush();
  }
?>
