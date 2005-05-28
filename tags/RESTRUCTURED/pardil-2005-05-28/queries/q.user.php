<?php

  // Kullanıcı bilgileri
  function query_user_data($int_id) {
    $str_sql = sprintf('SELECT email, name FROM users WHERE id=%d', $int_id);
    $res_sql = mysql_query($str_sql);
    return mysql_fetch_array($res_sql, MYSQL_ASSOC);
  }

  // Email -> ID
  function query_user_e2i($str_email) {
    $str_sql = sprintf('SELECT id FROM users WHERE email="%s"', addslashes($str_email));
    return database_query_scalar($str_sql);
  }
  
  // Username -> ID
  function query_user_u2i($str_username) {
    $str_sql = sprintf('SELECT id FROM users WHERE username="%s"', addslashes($str_username));
    return database_query_scalar($str_sql);
  }

  // Kullanıcı adı & şifre denetimi
  function query_user_validate($str_username, $str_password) {
    $str_sql = sprintf('SELECT id FROM users WHERE username="%s" AND password="%s"', addslashes($str_username), md5($str_password));
    return database_query_scalar($str_sql);
  }

  // Kullanıcı adı & geçici şifre enetimi
  function query_user_validate_tmp($str_username, $str_password) {
    $str_sql = sprintf('SELECT users.id FROM temp_passwords INNER JOIN users ON users.id=temp_passwords.user WHERE users.username="%s" AND temp_passwords.password="%s"', addslashes($str_username), md5($str_password));
    return database_query_scalar($str_sql);
  }
?>
