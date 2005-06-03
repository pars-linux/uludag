<?php

  function logout() {
    setcookie('ajax_session', '');
  }

  require '../ajax_base/xhr.php';
  $obj_xhr = new xhr();
  $obj_xhr->register('logout');
  $obj_xhr->handle();
?>
