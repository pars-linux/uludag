<?php

  require(dirname(__FILE__) . '/sys.common.php');

  require(dirname(__FILE__) . '/class/class.template.php');

  if (!isset($_PSESSION['id'])) {
    header('Location: denied.php');
    exit;
  }

  $arr_errors = array();
  if (isset($_POST['profile'])) {
    if (strlen($_POST['profile_name']) == 0) {
      $arr_errors['profile_name'] = __('Real name should be written.');
    }
    
    if (strlen($_POST['profile_password']) > 0 || strlen($_POST['profile_password2']) > 0) {
      if (strlen($_POST['profile_password']) == 0 || strlen($_POST['profile_password2']) == 0) {
        $arr_errors['profile_password'] = __('Password should be written twice.');
      }
      elseif ($_POST['profile_password'] != $_POST['profile_password2']) {
        $arr_errors['profile_password'] = __('Passwords should be same.');
      }
      elseif (strlen($_POST['profile_password']) < getop('min_password_length')) {
        $arr_errors['profile_password'] = sprintf(__('Password should be at least %d chars long.'), getop('min_password_length'));
      }
    }

    if (strlen($_POST['profile_email']) == 0) {
      $arr_errors['profile_email'] = __('E-mail address should be written.');
    }
    elseif (!preg_match('/^.+@.+(\..+)*$/', $_POST['profile_email'])) {
      $arr_errors['profile_email'] = __('E-mail address should be valid.');
    }
  }


  if (isset($_POST['profile']) && count($arr_errors) == 0) {
    // İşlem

    $int_status = (getop('addresschange_activation_required') == 'true') ? 0 : 1;

    $arr_update = array(
                        'name' => $_POST['profile_name'],
                        'email' => $_POST['profile_email']
                        );
    if (strlen($_POST['profile_password']) > 0) {
      $arr_update['password'] = md5($_POST['profile_password']);
    }
    proc_user_update($_PSESSION['id'], $arr_update);

    if ($int_status == 0 && $_PSESSION['email'] != $_POST['profile_email']) {
      // E-posta gönderimi

      proc_activation_update($_PSESSION['id'], 0);
      $str_code = proc_activation_renew($_PSESSION['id']);

      $str_subject = sprintf(__('%s Account Activation'), getop('site_name'));
      $str_url = $_PCONF['site_url'] . 'activate.php?code=' . $str_code . '&user=' . $_PSESSION['id'];
      $str_body = sprintf(__("Hello,\n\nTo complete your registration at %1\$s, please visit the address below:\n\n%2\$s\n\nThanks,\n%3\$s Team"), getop('site_url'), $str_url, getop('site_name'));
      $bln_mail = mail($_POST['profile_email'], $str_subject, $str_body);

      if ($bln_mail) {
        header('Location: profile_ok.php?activation=1');
        exit;
      }
      else {
        header('Location: profile_ok.php?nomail=1&activation=1');
        exit;
      }
    }
    else {
      header('Location: profile_ok.php');
      exit;
    }

  }
  elseif (isset($_POST['profile']) && count($arr_errors) > 0) {
    // Hata varsa...

    $_PCONF['title'] = getop('site_name') . ' - ' . __('User Profile');
    $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.profile.php');
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->setvar('bln_first', false);
    $obj_page->flush();
  }
  else {
    // Sayfa ilk defa açılıyorsa...
    
    $arr_user = query_user_data($_PSESSION['id']);
    
    $_PCONF['title'] = getop('site_name') . ' - ' . __('User Profile');
    $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.profile.php');
    $obj_page->setvar('bln_first', true);
    $obj_page->setvar('arr_user', $arr_user);
    $obj_page->flush();
  }
?>
