<?php

  // Kullanıcı bilgileri
  function query_user_data($int_id) {
    $str_sql = sprintf('SELECT email, name FROM users WHERE id=%d', $int_id);
    $res_sql = mysql_query($str_sql);
    return mysql_fetch_array($res_sql, MYSQL_ASSOC);
  }

?>
