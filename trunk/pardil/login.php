<?php

  require('sys.define.php');
  require('sys.gettext.php');
  require('sys.database.php');
  require('sys.procedures.php');

  require('class.template.php');

  $arr_errors = array();
  if (isset($_POST['login'])) {
    if (strlen($_POST['username']) == 0) {
      $arr_errors['username'] = _('Username should be written.');
    }
    
    if (strlen($_POST['password']) == 0) {
      $arr_errors['password'] = _('Password should be written.');
    }

    if (strlen($_POST['username']) > 0 && strlen($_POST['password']) > 0) {
      $mix_user = database_query_scalar(sprintf('SELECT id FROM users WHERE username="%s" AND password="%s"', addslashes($_POST['username']), md5(addslashes($_POST['password']))));
      if ($mix_user === false) {
        $arr_errors['password'] = _('Wrong username or password.');
      }
      else {
        $str_session = proc_session_update($mix_user);
        setcookie('pardil_session', $str_session);
        header('Location: index.php');
        exit;
      }
    }
  }

  if (!isset($_POST['login']) || count($arr_errors) > 0) {
    $_PCONF['title'] = CONF_NAME . ' - ' . _('User Login');
    $obj_page = new template('tpl.login.php');
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->flush();
  }
?>
