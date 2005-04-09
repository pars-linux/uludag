<?php

  require('cfg/sys.define.php');
  require('sys/sys.gettext.php');
  require('sys/sys.database.php');
  require('sys/sys.procedures.php');
  require('sys/sys.pconf.php');
  require('sys/sys.session.php');

  require('class/class.template.php');

  $arr_errors = array();
  if (isset($_POST['login'])) {
    if (strlen($_POST['username']) == 0) {
      $arr_errors['username'] = __('Username should be written.');
    }
    
    if (strlen($_POST['password']) == 0) {
      $arr_errors['password'] = __('Password should be written.');
    }

    if (strlen($_POST['username']) > 0 && strlen($_POST['password']) > 0) {
      $mix_user = database_query_scalar(sprintf('SELECT id FROM users WHERE username="%s" AND password="%s"', addslashes($_POST['username']), md5($_POST['password'])));
      if ($mix_user === false) {
        // Hatalı ise, geçici şifreyle karşılaştır
        $mix_user = database_query_scalar(sprintf('SELECT users.id FROM temp_passwords INNER JOIN users ON users.id=temp_passwords.user WHERE users.username="%s" AND temp_passwords.password="%s"', addslashes($_POST['username']), addslashes($_POST['password'])));
        if ($mix_user !== false) {
          // Bilgiler  doğru
          $str_session = proc_session_update($mix_user);
          setcookie('pardil', $str_session);
          header('Location: index.php');
          exit;
        }
        else {
          $arr_errors['password'] = __('Wrong username or password.');
        }
      }
      else {
        $int_activation = database_query_scalar(sprintf('SELECT status FROM activation WHERE user=%d', $mix_user));
        $str_act_required = getop('register_activation_required');
        if ($int_activation == 0 && $str_act_required == 'true') {
          // Aktivasyon gerek.
          $arr_errors['password'] = __('User account is not activated.');
        }
        else {
          // Bilgiler doğru
          $str_session = proc_session_init($mix_user);
          setcookie('pardil', $str_session);
          header('Location: index.php');
          exit;
        }
      }
    }
  }

  if (!isset($_POST['login']) || count($arr_errors) > 0) {
    $_PCONF['title'] = getop('site_name') . ' - ' . __('User Login');
    $obj_page = new template('tpl/tpl.login.php');
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->flush();
  }
?>
