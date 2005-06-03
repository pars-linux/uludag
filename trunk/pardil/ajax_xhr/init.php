<?php

  function ajax_init() {
    if (isset($_COOKIE['ajax_session'])) {
      return array('session' => $str_session, 'user' => 'Pardus');
    }
    return false;
  }

  require '../ajax_base/xhr.php';
  $obj_xhr = new xhr();
  $obj_xhr->register('ajax_init');
  $obj_xhr->handle();
?>
