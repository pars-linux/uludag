<?php

  // Öneri durumları
  // 1 - Onay Bekleyen, 2 - Onaylanmış, 3 - Kilitli

  // Yeni durum oluşturma
  function proc_status_new($str_status) {
    $str_status = addslashes($str_status);  // Metindeki tırnak işaretleri sorun yatarmasın...
    
    $str_sql = sprintf('INSERT INTO pardil_status (name) VALUES ("%s")', $str_status);
    mysql_query($str_sql);
    return mysql_insert_id();
  }

  // Durum silme
  function proc_status_delete($int_status) {
    // <=3 durumlar silinemez.
    if ($int_status <= 3) {
      return false;
    }
    // Durum, bir öneri ile ilişkili ise silinemez.
    $str_sql = sprintf('SELECT id FROM pardil_r_status WHERE status=%d', $int_status);
    $res_sql = mysql_query($res_sql);
    if (mysql_num_rows($res_sql) > 0) {
      return false;
    }
    else {
      $str_sql = sprintf('DELETE FROM pardil_status where id=%d"', $int_status);
      mysql_query($str_sql);
      return true;
    }
  }

  // Durum bilgisini güncelleme
  /*
    TODO: Burada değiştirilecek alanlar, sütun adlarıyla
    birlikte bir dizi içinde fonksiyona gönderiliyor.
    Daha sağlıklı bir yol izlenmeli.
  */
  function proc_status_update($int_status, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_status SET %s WHERE id=%d', $str_set, $int_status);
    $res_sql = mysql_query($res_sql);
    return true;
  }

  // Öneri - Durum ilişkisi
  // Öneri, aynı anda sadece bir durumda olabilir. Bu yüzden yeni durum eklerken, bir önceki durumun sonlandırılması gerekir.

  // Öneri - Durum ilişkisi ekle
  function proc_r_status_new($int_pardil, $int_status) {
    $str_dateB = date('Y-m-d H:i:s');
    $str_dateE = '9999.12.31 23:59:59';
    // Bir önceki durumu sonlandır
    $int_prev_id = database_query_scalar(sprintf('SELECT id FROM pardil_r_status WHERE proposal=%d AND timestampB<="%s" AND "%s"<=timestampE', $int_pardil, $str_dateB, $str_dateB));
    proc_r_status_update($int_prev_id, array('timestampE' => $str_dateB));
    // Yeni durum ekle
    $str_sql = sprintf('INSERT INTO pardil_r_status (proposal, status, timestampB, timestampE) VALUES (%d, %d, "%s", "%s")', $int_pardil, $int_status, $str_dateB, $str_dateE);
    mysql_query($str_sql);
    return mysql_insert_id();
  }

  // Öneri - Durum ilişkisi sonlandır
  function proc_r_status_delete($int_id) {
    // Bu ilişki silinemez, bitiş tarihini bugüne eşitlenir, ilişkiyi sonlandırılır.
    return proc_r_status_update($int_id, array('timestampE' => date('Y-m-d H:i:s')));
  }

  // Öneri - Durum ilişkisi değiştir
  function proc_r_status_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_r_status SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }
?>
