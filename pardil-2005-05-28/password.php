<?php

  require(dirname(__FILE__) . '/sys.common.php');

  require(dirname(__FILE__) . '/class/class.template.php');

  //
  $int_floodcontrol_t = 10 * 60;
  $int_floodcontrol_m = 3;
  proc_floodcontrol_expire('password', $int_floodcontrol_t);

  $arr_errors = array();

  if (isset($_POST['password'])) {
    if (proc_floodcontrol_check('password', $_SERVER['REMOTE_ADDR']) >= $int_floodcontrol_m) {
      $arr_errors['password_email'] = sprintf(__('You are allowed to use this form at most %1$d times in %2$d seconds.'), $int_floodcontrol_m, $int_floodcontrol_t);
    }
    elseif (strlen($_POST['password_email']) == 0) {
      $arr_errors['password_email'] = __('E-mail address should be written.');
    }
    elseif (!preg_match('/^.+@.+(\..+)*$/', $_POST['password_email'])) {
      $arr_errors['password_email'] = __('E-mail address should be valid.');
    }
    else {
      $mix_userno = query_user_e2i($_POST['password_email']);
      if ($mix_userno === false) {
        $arr_errors['password_email'] = __('E-mail address not found in database.');
      }
    }
  }

  if (isset($_POST['password']) && count($arr_errors) == 0) {
    // Şifre gönderildiğinde, flood kayıtlarıne ekle.
    proc_floodcontrol_add('password', $_SERVER['REMOTE_ADDR']);

    // İşlem
    $int_userno = query_user_e2i($_POST['password_email']);
    $str_code = proc_password_new($int_userno);
    
    $str_subject = sprintf(__('%s Temporary Password'), getop('site_name'));
    $str_body = sprintf(__("Hello,\n\nYou have requested a temporary password for your account at %1\$s.\n\nYour temporary password is: %2\$s\n\nThis temporary password does not effect your primary password.\n\nThanks,\n%3\$s Team"), getop('site_url'), $str_code, getop('site_name'));
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
    $_PCONF['title'] = getop('site_name') . ' - ' . __('Create Temporary Password');
    $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.password.php');
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->flush();
  }
?>
