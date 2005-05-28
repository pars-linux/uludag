<?php

  // Kullanıcı için geçici şifre oluşturma
  function proc_password_new($int_user) {
    $str_date = date('Y-m-d H:i:s');
    $str_code = substr(md5(microtime() . $int_user), 0, 10);
    $str_sql = sprintf('INSERT INTO temp_passwords (user, password, timestamp) VALUES (%d, "%s", "%s")', $int_user, $str_code, $str_date);
    mysql_query($str_sql);
    return $str_code;
  }

  // Kullanının geçici şifresini yoketme
  function proc_password_delete($int_user) {
    $str_sql = sprintf('DELETE FROM temp_passwords WHERE user=%d', $int_user);
    mysql_query($str_sql);
    return true;;
  }

  // Süresi geçmiş geçici şifreleri yoketme
  function proc_password_expire($int_timeout) {
    $str_date = date('Y-m-d H:i:s');
    $str_sql = sprintf('DELETE FROM temp_passwords WHERE Unix_Timestamp("%s")-Unix_Timestamp(timestamp) > %d', $str_date, $int_timeout);
    mysql_query($str_sql);
    return true;
  }

?>
