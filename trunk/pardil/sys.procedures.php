<?php
  // INSERT & UPDATE & DELETE

  // UGO_Status
  // Durum çeşitleri
  // 1 - Onay Bekleyen,2 - Onaylanmış, 3 - Askıya Alınan
  function proc_status_new($str_status) {
    $str_sql = sprintf('INSERT INTO ugo_status (name) VALUES ("%s")', $str_status);
    mysql_query($str_sql);
    return mysql_insert_id();
  }
  function proc_status_delete($int_status) {
    // <=3 durumlar silinemez.
    if ($int_status <= 3) {
      return false;
    }
    // Durum, bir öneri ile ilişkili ise silinemez.
    $str_sql = sprintf('SELECT id FROM ugo_r_status WHERE status=%d', $int_status);
    $res_sql = mysql_query($res_sql);
    if (mysql_num_rows($res_sql) > 0) {
      return false;
    }
    else {
      $str_sql = sprintf('DELETE FROM ugo_status where id=%d"', $int_status);
      mysql_query($str_sql);
      return true;
    }
  }
  function proc_status_update($int_status, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE ugo_status SET %s WHERE id=%d', $str_set, $int_status);
    $res_sql = mysql_query($res_sql);
    return true;
  }

  // UGO_Roles
  // Proje ekibindeki roller
  function proc_role_new($str_role, $int_level) {
    $str_sql = sprintf('INSERT INTO ugo_roles (name, level) VALUES ("%s", %d)', $str_role, $int_level);
    mysql_query($str_sql);
    return mysql_insert_id();
  }
  function proc_role_delete($int_role) {
    // Rol, bir öneri ile ilişkili ise silinemez.
    $str_sql = sprintf('SELECT id FROM ugo_r_roles WHERE role=%d', $int_role);
    $res_sql = mysql_query($res_sql);
    if (mysql_num_rows($res_sql) > 0) {
      return false;
    }
    else {
      $str_sql = sprintf('DELETE FROM ugo_roles where id=%d"', $int_role);
      mysql_query($str_sql);
      return true;
    }
  }
  function proc_role_update($int_role, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE ugo_roles SET %s WHERE id=%d', $str_set, $role);
    $res_sql = mysql_query($res_sql);
    return true;
  }

  // Users
  // Sistem kullanıcıları
  function proc_user_new($str_username, $str_password, $str_email, $str_name, $int_level) {
    $str_sql = sprintf('INSERT INTO users (username, password, email, name, level) VALUES ("%s", "%s", "%s", "%s", %d)', $str_username, $str_password, $str_email, $str_name, $int_level);
    mysql_query($str_sql);
    return mysql_insert_id();
  }
  function proc_users_delete($int_user) {
    // 1 numaralı sistem yöneticisi hesabı silinemez.
    if ($int_user == 1) {
      return false;
    }
    // Kullanıcı, bir önerinin bakıcısı ise silinemez.
    $str_sql = sprintf('SELECT user FROM ugo_maintainers WHERE user=%d', $int_user);
    $res_sql = mysql_query($res_sql);
    if (mysql_num_rows($res_sql) > 0) {
      return false;
    }

    $str_sql = sprintf('UPDATE ugo_main SET sender=%d WHERE sender=%d', 1, $int_user);
    $res_sql = mysql_query($res_sql);
    
    $str_sql = sprintf('UPDATE ugo_revisions SET revisor=%d WHERE revisor=%d', 1, $int_user);
    $res_sql = mysql_query($res_sql);

    $str_sql = sprintf('DELETE FROM ugo_r_roles where user=%d"', $int_user);
    mysql_query($str_sql);
    
    return true;
  }
  function proc_user_update($int_user, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE users SET %s WHERE id=%d', $str_set, $int_user);
    mysql_query($str_sql);
    return true;
  }

  // Ugo_Images
  // Önerilere ait resim dosyaları
  function proc_image_new($int_ugo, $str_filecontent, $str_contenttype) {
    $str_sql = sprintf('INSERT INTO ugo_images (ugo, image, content_type) VALUES (%d, "%s", "%s")', $int_ugo, $str_filecontent, $str_contenttype);
    mysql_query($str_sql);
    return mysql_insert_id();
  }
  function proc_image_delete($int_image) {
    $str_sql = sprintf('DELETE FROM ugo_images WHERE id=%d', $int_image);
    mysql_query($str_sql);
    return true;
  }
  function proc_image_update($int_image, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE ugo_images SET %s WHERE id=%d', $str_set, $int_image);
    mysql_query($str_sql);
    return true;
  }

  // Ugo_R_Releated
  // Bağlantılı öneriler
  // Aynı anda birden fazla öneri birbirine bağlı olabilir, yeni ilişki eklenirken bir önceki ilişkinin sonlandırılması gerekmez.
  function proc_r_relation_new($int_ugo1, $int_ugo2) {
    $str_dateB = date('Y.m.d H:i:s');
    $str_dateE = '9999.12.31 23:59:59';
    $str_sql = sprintf('INSERT INTO ugo_r_releated (ugo, ugo2, timestampB, timestampE) VALUES (%d, %d, "%s", "%s")', $int_ugo, $int_ugo2, $str_dateB, $str_dateE);
    mysql_query($str_sql);
    return mysql_insert_id();
  }
  function proc_r_relation_delete($int_id) {
    // Bu ilişki silinemez,, bitiş tarihini bugüne eşitlenir, ilişkiyi sonlandırılır.
    return proc_r_relation_update($int_id, array('timestampE' => date('Y.m.d H:i:s')));
  }
  function proc_r_relation_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE ugo_r_releated SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }

  // UGO_R_Roles
  // Öneri - Rol ilişkileri
  // Aynı anda birden fazla rol bir öneriye bağlı olabilir, yeni ilişki eklenirken bir önceki ilişkinin sonlandırılması gerekmez.
  function proc_r_roles_new($int_ugo, $int_user, $int_role) {
    $str_dateB = date('Y.m.d H:i:s');
    $str_dateE = '9999.12.31 23:59:59';
    $str_sql = sprintf('INSERT INTO ugo_r_roles (ugo, user, role, timestampB, timestampE) VALUES (%d, %d, %d, "%s", "%s")', $int_ugo, $int_user, $int_role, $str_dateB, $str_dateE);
    mysql_query($str_sql);
    return mysql_insert_id();
  }
  function proc_r_roles_delete($int_id) {
    // Bu ilişki silinemez,, bitiş tarihini bugüne eşitlenir, ilişkiyi sonlandırılır.
    return proc_r_roles_update($int_id, array('timestampE' => date('Y.m.d H:i:s')));
  }
  function proc_r_roles_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE ugo_r_roles SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }

  // UGO_R_Status
  // Öneri - Durum ilişkisi
  // Öneri, aynı anda sadece bir durumda olabilir. Bu yüzden yeni durum eklerken, bir önceki durumun sonlandırılması gerekir.
  function proc_r_status_new($int_ugo, $int_status) {
    $str_dateB = date('Y.m.d H:i:s');
    $str_dateE = '9999.12.31 23:59:59';
    // Bir önceki durumu sonlandır
    $int_prev_id = database_query_scalar(sprintf('SELECT id FROM ugo_r_status WHERE ugo=%d AND timestampB<="%s" AND "%s"<=timestampE', $int_ugo, $str_dateB, $str_dateB));
    proc_r_status_update($int_prev_id, array('timestampE' => $str_dateB));
    // Yeni durum ekle
    $str_sql = sprintf('INSERT INTO ugo_r_status (ugo, status, timestampB, timestampE) VALUES (%d, %d, "%s", "%s")', $int_ugo, $int_status, $str_dateB, $str_dateE);
    mysql_query($str_sql);
    return mysql_insert_id();
  }
  function proc_r_status_delete($int_id) {
    // Bu ilişki silinemez,, bitiş tarihini bugüne eşitlenir, ilişkiyi sonlandırılır.
    return proc_r_status_update($int_id, array('timestampE' => date('Y.m.d H:i:s')));
  }
  function proc_r_status_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE ugo_r_status SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }
  
  // UGO_Maintainers
  function proc_maintainers_new($int_ugo, $int_user) {
    $str_dateB = date('Y.m.d H:i:s');
    $str_dateE = '9999.12.31 23:59:59';
    $str_sql = sprintf('INSERT INTO ugo_maintainers (ugo, user, timestampB, timestampE) VALUES (%d, %d, "%s", "%s")', $int_ugo, $int_user, $str_dateB, $str_dateE);
    mysql_query($str_sql);
    return mysql_insert_id();
  }
  function proc_maintainers_delete($int_id) {
    // Bu ilişki silinemez,, bitiş tarihini bugüne eşitlenir, ilişkiyi sonlandırılır.
    return proc_maintainers_update($int_id, array('timestampE' => date('Y.m.d H:i:s')));
  }
  function proc_maintainers_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE ugo_maintainers SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }

  // UGO_Main, UGO_Revisions
  function proc_main_new($int_sender, $str_title, $str_abstract, $str_content, $str_notes, $str_info, $bln_approve=false, $str_date='') {
    $str_sql = sprintf('INSERT INTO ugo_main (sender, title, abstract) VALUES (%d, "%s","%s")', $int_sender, $str_title, $str_abstract);
    mysql_query($str_sql);
    $int_ugo_id = mysql_insert_id();

    $str_date = ($str_date != '') ? $str_date : date('Y.m.d H:i:s');
    $dbl_version = 1.0;
    $str_sql = sprintf('INSERT INTO ugo_revisions (ugo, revisor, version, content, notes, info, timestamp) VALUES (%d, %d, %f, "%s","%s", "%s", "%s")', $int_ugo_id, $int_sender, $dbl_version, $str_content, $str_notes, $str_info, $str_date);
    mysql_query($str_sql);

    $int_status = ($bln_approve) ? 2 : 1;
    proc_r_status_new($int_ugo_id, $int_status, $str_date);

    return $int_ugo_id;
  }
  function proc_main_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE ugo_main SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }

  function proc_revision_new($int_ugo, $int_revisor, $dbl_version, $str_content, $str_notes, $str_info, $str_date='') {
    $str_date = ($str_date != '') ? $str_date : date('Y.m.d H:i:s');
    $str_sql = sprintf('INSERT INTO ugo_revisions (ugo, revisor, version, content, notes, info, timestamp) VALUES (%d, %d, %f, "%s","%s", "%s", "%s")', $int_ugo, $int_sender, $dbl_version, $str_content, $str_notes, $str_info, $str_date);
    mysql_query($str_sql);
    return mysql_insert_id();
  }
  function proc_revision_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE ugo_revisions SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }


  // Test: DELETE Revision
  // Bir öneriye ait revizyonu silen prosedür.
  function proc_revision_delete($int_id) {
    return false;
  }
  
  // Test: DELETE UGO
  // Öneri ve ilgili tüm kayıtları silen prosedür.
  function proc_ugo_delete($int_ugo, $bln_approve=false) {
    return false;
    if (!$bln_approve) {
      return false;
    }
    // UGO_Images
    $str_sql = sprintf('DELETE FROM ugo_images WHERE ugo=%d', $int_ugo);
    mysql_query($str_sql);
    // UGO_Maintainers
    $str_sql = sprintf('DELETE FROM ugo_maintainers WHERE ugo=%d', $int_ugo);
    mysql_query($str_sql);
    // UGO_R_Releated
    $str_sql = sprintf('DELETE FROM ugo_r_releated WHERE ugo=%d OR ugo2=%d', $int_ugo, $int_ugo);
    mysql_query($str_sql);
    // UGO_R_Roles
    $str_sql = sprintf('DELETE FROM ugo_r_releated WHERE ugo=%d', $int_ugo);
    mysql_query($str_sql);
    // UGO_R_Status
    $str_sql = sprintf('DELETE FROM ugo_r_status WHERE ugo=%d', $int_ugo);
    mysql_query($str_sql);
    // UGO_Revisions
    $str_sql = sprintf('DELETE FROM ugo_revisions WHERE ugo=%d', $int_ugo);
    mysql_query($str_sql);
    // UGO_Main
    $str_sql = sprintf('DELETE FROM ugo_main WHERE id=%d', $int_ugo);
    mysql_query($str_sql);
    
    return true;
  }
?>
