<?php

  // Kullanıcı için aktivasyon kaydı yaratma
  // İkinci argüman 1 ise, hesap aktive edilmiş olarak işaretlenir
  function proc_activation_new($int_user, $int_status) {
    $str_date = date('Y-m-d H:i:s');
    $str_code = md5(microtime() . $int_user);
    $str_sql = sprintf('INSERT INTO activation (user, code, status, timestamp) VALUES (%d, "%s", %d, "%s")', $int_user, $str_code, $int_status, $str_date);
    mysql_query($str_sql);
    return $str_code;
  }
  
  // Kullanıcının aktivasyon durumunu değiştirme
  function proc_activation_update($int_user, $int_status) {
    $str_date = date('Y-m-d H:i:s');
    $str_sql = sprintf('UPDATE activation SET status=%d,timestamp="%s" WHERE user=%d', $int_status, $str_date, $int_user);
    mysql_query($str_sql);
    return true;
  }
  
  // Aktivasyon kodunu güncelleme
  function proc_activation_renew($int_user) {
    $str_date = date('Y-m-d H:i:s');
    $str_code = md5(microtime() . $int_user);
    $str_sql = sprintf('UPDATE activation SET code="%s",timestamp="%s" WHERE user=%d', $str_code, $str_date, $int_user);
    mysql_query($str_sql);
    return $str_code;
  }

  // Süresi geçmiş aktivasyon bilgilerine bakarak kullanıcı hesabını yoketme
  function proc_activation_expire($int_timeout) {
    // TODO
  }

?>
