<?php

  function query_activation_status_uc($int_user, $str_code) {
    $str_sql = sprintf('SELECT status FROM activation INNER JOIN users ON users.id = activation.user WHERE users.id=%d AND activation.code="%s"', addslashes($int_user), addslashes($str_code));
    return database_query_scalar($str_sql);
  }
  
  function query_activation_status_e($str_email) {
    $str_sql = sprintf('SELECT status FROM activation INNER JOIN users ON users.id = activation.user WHERE users.email="%s"', addslashes($str_email));
    return database_query_scalar($str_sql);
  }
  
  function query_activation_status_i($int_user) {
    $str_sql = sprintf('SELECT status FROM activation WHERE user=%d', $int_user);
    return database_query_scalar($str_sql);
  }
?>
