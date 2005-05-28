<?php

  // Kullanıcı oturumları

  // Oturum açma & oturum bilgisi güncelleme
  function proc_session_init($int_user) {
    $str_date = date('Y-m-d H:i:s');
    $mix_sessionid = database_query_scalar(sprintf('SELECT id FROM sessions WHERE user=%d', $int_user));
    if ($mix_sessionid === false) {
      return proc_session_create($int_user);
    }
    else {
      $str_sql = sprintf('UPDATE sessions SET timestamp="%s" WHERE user=%d', $str_date, $int_user);
      mysql_query($str_sql);
      return $mix_sessionid;
    }
  }

  // Yeni oturum yaratma
  function proc_session_create($int_user) {
    $str_id = md5(microtime() . $int_user);
    $str_date = date('Y-m-d H:i:s');
    $str_sql = sprintf('INSERT INTO sessions (id, user, timestamp) VALUES ("%s", %d, "%s")', $str_id, $int_user, $str_date);
    mysql_query($str_sql);
    return $str_id;
  }

  // Belirtilen oturumu sonlandırma
  function proc_session_delete($str_session) {
    $str_sql = sprintf('DELETE FROM sessions WHERE id=%d', $str_session);
    mysql_query($str_sql);
    return true;
  }

  // Süresi geçen oturumları sonlandırma
  function proc_session_expire($int_timeout) {
    $str_date = date('Y-m-d H:i:s');
    $str_sql = sprintf('DELETE FROM sessions WHERE Unix_Timestamp("%s")-Unix_Timestamp(timestamp) > %d', $str_date, $int_timeout);
    mysql_query($str_sql);
    return true;
  }


?>
