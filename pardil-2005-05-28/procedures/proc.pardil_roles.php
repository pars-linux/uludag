<?php

  // Yeni proje ekibi rolü oluşturma
  function proc_role_new($str_role, $int_level) {
    $str_role = addslashes($str_role); // Metindeki tırnak işaretleri sorun yatarmasın...

    $str_sql = sprintf('INSERT INTO pardil_roles (name, level) VALUES ("%s", %d)', $str_role, $int_level);
    mysql_query($str_sql);
    return mysql_insert_id();
  }

  // Proje ekibi rolü silme
  function proc_role_delete($int_role) {
    // Rol, bir öneri ile ilişkili ise silinemez.
    $str_sql = sprintf('SELECT id FROM pardil_r_roles WHERE role=%d', $int_role);
    $res_sql = mysql_query($res_sql);
    if (mysql_num_rows($res_sql) > 0) {
      return false;
    }
    else {
      $str_sql = sprintf('DELETE FROM pardil_roles where id=%d"', $int_role);
      mysql_query($str_sql);
      return true;
    }
  }

  // Proje ekibi bilgisi güncelleme
  /*
    INFO: proc.pardil_status.php dosyasındaki benzer 
    isimli fonksiyona gözatın.
  */
  function proc_role_update($int_role, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_roles SET %s WHERE id=%d', $str_set, $role);
    $res_sql = mysql_query($res_sql);
    return true;
  }

  // Öneri - Rol ilişkileri
  // Aynı anda birden fazla rol bir öneriye bağlı olabilir, yeni ilişki eklenirken bir önceki ilişkinin sonlandırılması gerekmez.

  // Öneri - Kişi - Rol ilişkisi ekle
  function proc_r_roles_new($int_pardil, $int_user, $int_role) {
    $str_dateB = date('Y-m-d H:i:s');
    $str_dateE = '9999.12.31 23:59:59';
    $str_sql = sprintf('INSERT INTO pardil_r_roles (proposal, user, role, timestampB, timestampE) VALUES (%d, %d, %d, "%s", "%s")', $int_pardil, $int_user, $int_role, $str_dateB, $str_dateE);
    mysql_query($str_sql);
    return mysql_insert_id();
  }

  // Öneri - Kişi - Rol ilişkisi sonlandır
  function proc_r_roles_delete($int_id) {
    // Bu ilişki silinemez, bitiş tarihini bugüne eşitlenir, ilişkiyi sonlandırılır.
    return proc_r_roles_update($int_id, array('timestampE' => date('Y-m-d H:i:s')));
  }

  // Öneri - Kişi - Rol ilişkisini değiştir
  /*
    INFO: proc.pardil_status.php dosyasındaki benzer
    isimli fonksiyona gözatın.
  */
  function proc_r_roles_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_r_roles SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }
?>
