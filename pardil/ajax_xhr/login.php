<?php

  function login($arr_data) {
    $str_user = $arr_data['user'];
    $str_pass = $arr_data['pass'];
    $str_session = md5(time() . $str_user);
    if ($str_user == 'Pardus' && $str_pass == 'Linüks') {
      return array('session' => $str_session, 'user' => $str_user);
    }
    return 'h';
  }

  require '../ajax_base/xhr.php';
  $obj_xhr = new xhr();
  $obj_xhr->register('login');
  $obj_xhr->handle();
?>
