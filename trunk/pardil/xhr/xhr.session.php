<?php
  
  require(dirname(__FILE__) . '/../sys.common.php');
  require(dirname(__FILE__) . '/../class/class.xmlhttprequest.php');

  function session($str_o) {
    // Bu dosya, oturum yönetimi kodunu içeriyor,
    // başka birşey yapmaya gerek yok :)
    return "true";
  }

  $obj_xhr = new xmlhttprequest();
  $obj_xhr->register_func('session');
  $obj_xhr->handle_request();
?>
