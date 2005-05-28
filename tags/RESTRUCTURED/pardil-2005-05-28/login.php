<?php

  require(dirname(__FILE__) . '/sys.common.php');

  require(dirname(__FILE__) . '/class/class.template.php');

  $arr_errors = array();
  if (isset($_POST['login'])) {
    if (strlen($_POST['username']) == 0) {
      $arr_errors['username'] = __('Username should be written.');
    }
    
    if (strlen($_POST['password']) == 0) {
      $arr_errors['password'] = __('Password should be written.');
    }

    if (strlen($_POST['username']) > 0 && strlen($_POST['password']) > 0) {
      $mix_user = query_user_validate($_POST['username'], $_POST['password']);
      if ($mix_user === false) {
        // Hatalı ise, geçici şifreyle karşılaştır
        $mix_user = query_user_validate_tmp($_POST['username'], $_POST['password']);
        if ($mix_user !== false) {
          // Bilgiler  doğru
          $str_session = proc_session_init($mix_user);
          setcookie('pardil', $str_session);
          header('Location: index.php');
          exit;
        }
        else {
          $arr_errors['password'] = __('Wrong username or password.');
        }
      }
      else {
        $int_activation = query_activation_status_i($mix_user);
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
    $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.login.php');
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->flush();
  }
?>
