<?php

  // Yeni kullanıcı ekle
  function proc_user_new($str_username, $str_password, $str_email, $str_name, $int_level) {
    $str_username = addslashes($str_username); // Metindeki tırnak işaretleri sorun yatarmasın...
    $str_password = md5($str_password);
    $str_email = addslashes($str_email);
    $str_name = addslashes($str_name);

    $str_sql = sprintf('INSERT INTO users (username, password, email, name, level) VALUES ("%s", "%s", "%s", "%s", %d)', $str_username, $str_password, $str_email, $str_name, $int_level);
    mysql_query($str_sql);
    return mysql_insert_id();
  }

  // Kullanıcı sil
  function proc_users_delete($int_user) {
    // 1 numaralı sistem yöneticisi hesabı silinemez.
    if ($int_user == 1) {
      return false;
    }
    // Kullanıcı, bir önerinin bakıcısı ise silinemez.
    $str_sql = sprintf('SELECT user FROM pardil_maintainers WHERE user=%d', $int_user);
    $res_sql = mysql_query($res_sql);
    if (mysql_num_rows($res_sql) > 0) {
      return false;
    }

    $str_sql = sprintf('UPDATE pardil_main SET sender=%d WHERE sender=%d', 1, $int_user);
    $res_sql = mysql_query($res_sql);
    
    $str_sql = sprintf('UPDATE pardil_revisions SET revisor=%d WHERE revisor=%d', 1, $int_user);
    $res_sql = mysql_query($res_sql);

    $str_sql = sprintf('DELETE FROM pardil_r_roles where user=%d"', $int_user);
    mysql_query($str_sql);
    
    return true;
  }

  // Kullanıcı bilgilerini güncelle
  /*
    INFO: proc.pardil_status.php dosyasındaki benzer
    isimli fonksiyona gözatın.
  */
  function proc_user_update($int_user, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE users SET %s WHERE id=%d', $str_set, $int_user);
    mysql_query($str_sql);
    return true;
  }

?>
