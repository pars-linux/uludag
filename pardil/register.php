<?php

  require('sys.define.php');
  require('sys.gettext.php');
  require('sys.database.php');
  require('sys.procedures.php');

  require('class.template.php');

  $arr_errors = array();
  if (isset($_POST['register'])) {
    if (strlen($_POST['register_name']) == 0) {
      $arr_errors['register_name'] = _('Real name should be written.');
    }
    
    if (strlen($_POST['register_username']) == 0) {
      $arr_errors['register_username'] = _('Username should be written.');
    }
    else {
      $mix_userno = database_query_scalar(sprintf('SELECT id FROM users WHERE username="%s"', addslashes($_POST['register_username'])));
      if ($mix_userno !== false) {
        $arr_errors['register_username'] = _('Username is in use.');
      }
    }
    
    if (strlen($_POST['register_password']) == 0 || strlen($_POST['register_password2']) == 0) {
      $arr_errors['register_password'] = _('Password should be written twice.');
    }
    elseif ($_POST['register_password'] != $_POST['register_password2']) {
      $arr_errors['register_password'] = _('Passwords should be same.');
    }

    if (strlen($_POST['register_email']) == 0) {
      $arr_errors['register_email'] = _('E-mail address should be written.');
    }
    elseif (!preg_match('/^.+@.+(\..+)*$/', $_POST['register_email'])) {
      $arr_errors['register_email'] = _('E-mail address should be valid.');
    }
  }

  if (isset($_POST['register']) && count($arr_errors) == 0) {
    // İşlem
    // ...
    header('Location: register_ok.php');
  }
  else {
    $_PCONF['title'] = CONF_NAME . ' - ' . _('User Registration');
    $obj_page = new template('tpl.register.php');
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->flush();
  }
?>
