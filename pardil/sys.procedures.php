<?php
  // INSERT & UPDATE & DELETE
  
  /*
    INSERT, UPDATE, DELETE komutları için hazırlanan bu fonksiyonlar, kod içinde 
    doğrudan SQL komutu kullanılmasını engellemek için hazırlanmıştır.
    Ayrıca, ileride Stored Procedure destekli bir veritabanı yöneticisine geçildiğinde 
    fonksiyonların SP'lere dönüştürülmesi zor olmayacaktır.
  */

  // Pardil_Status
  // Durum çeşitleri
  // 1 - Onay Bekleyen, 2 - Onaylanmış, 3 - Kilitli
  function proc_status_new($str_status) {
    $str_status = addslashes($str_status);  // Metindeki tırnak işaretleri sorun yatarmasın...
    
    $str_sql = sprintf('INSERT INTO pardil_status (name) VALUES ("%s")', $str_status);
    mysql_query($str_sql);
    return mysql_insert_id();
  }
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
  function proc_status_update($int_status, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_status SET %s WHERE id=%d', $str_set, $int_status);
    $res_sql = mysql_query($res_sql);
    return true;
  }

  // Pardil_Roles
  // Proje ekibindeki roller
  function proc_role_new($str_role, $int_level) {
    $str_role = addslashes($str_role); // Metindeki tırnak işaretleri sorun yatarmasın...

    $str_sql = sprintf('INSERT INTO pardil_roles (name, level) VALUES ("%s", %d)', $str_role, $int_level);
    mysql_query($str_sql);
    return mysql_insert_id();
  }
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
  function proc_role_update($int_role, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_roles SET %s WHERE id=%d', $str_set, $role);
    $res_sql = mysql_query($res_sql);
    return true;
  }

  // Users
  // Sistem kullanıcıları
  function proc_user_new($str_username, $str_password, $str_email, $str_name, $int_level) {
    $str_username = addslashes($str_username); // Metindeki tırnak işaretleri sorun yatarmasın...
    $str_password = addslashes($str_password);
    $str_email = addslashes($str_email);
    $str_name = addslashes($str_name);

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
  function proc_user_update($int_user, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE users SET %s WHERE id=%d', $str_set, $int_user);
    mysql_query($str_sql);
    return true;
  }

  // Sessions
  // Kullanıcı oturumları
  function proc_session_new($int_user) {
    $str_id = md5(microtime() . $int_user);
    $str_date = date('Y-m-d H:i:s');
    $str_sql = sprintf('INSERT INTO sessions (id, user, timestamp) VALUES ("%s", %d, "%s")', $str_id, $int_user, $str_date);
    mysql_query($str_sql);
    return $str_id;
  }
  function proc_session_delete($str_session) {
    $str_sql = sprintf('DELETE FROM sessions WHERE id=%d', $str_session);
    mysql_query($str_sql);
    return true;
  }
  function proc_session_expire($int_timeout) {
    $str_date = date('Y-m-d H:i:s');
    $str_sql = sprintf('DELETE FROM sessions WHERE Unix_Timestamp("%s")-Unix_Timestamp(timestamp) > %d', $str_date, $int_timeout);
    mysql_query($str_sql);
    return true;
  }
  function proc_session_update($int_user) {
    $str_date = date('Y-m-d H:i:s');
    $mix_sessionid = database_query_scalar(sprintf('SELECT id FROM sessions WHERE user=%d', $int_user));
    if ($mix_sessionid === false) {
      return proc_session_new($int_user);
    }
    else {
      $str_sql = sprintf('UPDATE sessions SET timestamp="%s" WHERE user=%d', $str_date, $int_user);
      mysql_query($str_sql);
      return $mix_sessionid;
    }
  }

  // Activation
  // Aktivasyon kodları & durumları
  function proc_activation_new($int_user, $int_status) {
    $str_date = date('Y-m-d H:i:s');
    $str_code = md5(microtime() . $int_user);
    $str_sql = sprintf('INSERT INTO activation (user, code, status, timestamp) VALUES (%d, "%s", %d, "%s")', $int_user, $str_code, $int_status, $str_date);
    mysql_query($str_sql);
    return true;
  }
  function proc_activation_update($int_user, $int_status) {
    $str_date = date('Y-m-d H:i:s');
    $str_sql = sprintf('UPDATE activation SET status=%d,timestamp="%s" WHERE user=%d', $int_status, $str_date, $int_user);
    mysql_query($str_sql);
    return true;
  }
  function proc_activation_expire($int_timeout) {
    //
  }
  
  // Password
  // Şifre hatırlatma kodları
  function proc_password_new($int_user) {
    $str_date = date('Y-m-d H:i:s');
    $str_code = substr(md5(microtime() . $int_user), 0, 10);
    $str_sql = sprintf('INSERT INTO temp_passwords (user, password, timestamp) VALUES (%d, "%s", "%s")', $int_user, $str_code, $str_date);
    mysql_query($str_sql);
    return $str_code;
  }
  function proc_password_delete($int_user) {
    $str_sql = sprintf('DELETE FROM temp_passwords WHERE user=%d', $int_user);
    mysql_query($str_sql);
    return true;;
  }
  function proc_password_expire($int_timeout) {
    $str_date = date('Y-m-d H:i:s');
    $str_sql = sprintf('DELETE FROM temp_passwords WHERE Unix_Timestamp("%s")-Unix_Timestamp(timestamp) > %d', $str_date, $int_timeout);
    mysql_query($str_sql);
    return true;
  }
  
  
  // Pardil_Images
  // Önerilere ait resim dosyaları
  function proc_image_new($int_pardil, $str_filecontent, $str_contenttype) {
    $str_filecontent = addslashes($str_filecontent); // Metindeki tırnak işaretleri sorun yatarmasın...
    $str_contenttype = addslashes($str_contenttype);

    $str_sql = sprintf('INSERT INTO pardil_images (proposal, image, content_type) VALUES (%d, "%s", "%s")', $int_pardil, $str_filecontent, $str_contenttype);
    mysql_query($str_sql);
    return mysql_insert_id();
  }
  function proc_image_delete($int_image) {
    $str_sql = sprintf('DELETE FROM pardil_images WHERE id=%d', $int_image);
    mysql_query($str_sql);
    return true;
  }
  function proc_image_update($int_image, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_images SET %s WHERE id=%d', $str_set, $int_image);
    mysql_query($str_sql);
    return true;
  }

  // Pardil_R_Releated
  // Bağlantılı öneriler
  // Aynı anda birden fazla öneri birbirine bağlı olabilir, yeni ilişki eklenirken bir önceki ilişkinin sonlandırılması gerekmez.
  function proc_r_relation_new($int_pardil1, $int_pardil2) {
    $str_dateB = date('Y-m-d H:i:s');
    $str_dateE = '9999.12.31 23:59:59';
    $str_sql = sprintf('INSERT INTO pardil_r_releated (proposal, proposal, timestampB, timestampE) VALUES (%d, %d, "%s", "%s")', $int_pardil, $int_pardil2, $str_dateB, $str_dateE);
    mysql_query($str_sql);
    return mysql_insert_id();
  }
  function proc_r_relation_delete($int_id) {
    // Bu ilişki silinemez,, bitiş tarihini bugüne eşitlenir, ilişkiyi sonlandırılır.
    return proc_r_relation_update($int_id, array('timestampE' => date('Y-m-d H:i:s')));
  }
  function proc_r_relation_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_r_releated SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }

  // Pardil_R_Roles
  // Öneri - Rol ilişkileri
  // Aynı anda birden fazla rol bir öneriye bağlı olabilir, yeni ilişki eklenirken bir önceki ilişkinin sonlandırılması gerekmez.
  function proc_r_roles_new($int_pardil, $int_user, $int_role) {
    $str_dateB = date('Y-m-d H:i:s');
    $str_dateE = '9999.12.31 23:59:59';
    $str_sql = sprintf('INSERT INTO pardil_r_roles (proposal, user, role, timestampB, timestampE) VALUES (%d, %d, %d, "%s", "%s")', $int_pardil, $int_user, $int_role, $str_dateB, $str_dateE);
    mysql_query($str_sql);
    return mysql_insert_id();
  }
  function proc_r_roles_delete($int_id) {
    // Bu ilişki silinemez,, bitiş tarihini bugüne eşitlenir, ilişkiyi sonlandırılır.
    return proc_r_roles_update($int_id, array('timestampE' => date('Y-m-d H:i:s')));
  }
  function proc_r_roles_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_r_roles SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }

  // Pardil_R_Status
  // Öneri - Durum ilişkisi
  // Öneri, aynı anda sadece bir durumda olabilir. Bu yüzden yeni durum eklerken, bir önceki durumun sonlandırılması gerekir.
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
  function proc_r_status_delete($int_id) {
    // Bu ilişki silinemez,, bitiş tarihini bugüne eşitlenir, ilişkiyi sonlandırılır.
    return proc_r_status_update($int_id, array('timestampE' => date('Y-m-d H:i:s')));
  }
  function proc_r_status_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_r_status SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }
  
  // Pardil_Maintainers
  function proc_maintainers_new($int_pardil, $int_user) {
    $str_dateB = date('Y-m-d H:i:s');
    $str_dateE = '9999.12.31 23:59:59';
    $str_sql = sprintf('INSERT INTO pardil_maintainers (proposal, user, timestampB, timestampE) VALUES (%d, %d, "%s", "%s")', $int_pardil, $int_user, $str_dateB, $str_dateE);
    mysql_query($str_sql);
    return mysql_insert_id();
  }
  function proc_maintainers_delete($int_id) {
    // Bu ilişki silinemez,, bitiş tarihini bugüne eşitlenir, ilişkiyi sonlandırılır.
    return proc_maintainers_update($int_id, array('timestampE' => date('Y-m-d H:i:s')));
  }
  function proc_maintainers_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_maintainers SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }

  // Pardil_Main, Pardil_Revisions
  function proc_main_new($int_sender, $str_title, $str_abstract, $str_content, $str_notes, $str_info, $bln_approve=false, $str_date='') {
    $str_title = addslashes($str_title); // Metindeki tırnak işaretleri sorun yatarmasın...
    $str_abstract = addslashes($str_abstract);
    $str_contente = addslashes($str_contents);
    $str_notes = addslashes($str_notes);
    $str_info = addslashes($str_info);
    $str_date = addslashes($str_date);
    
    $str_sql = sprintf('INSERT INTO pardil_main (sender, title, abstract) VALUES (%d, "%s","%s")', $int_sender, $str_title, $str_abstract);
    mysql_query($str_sql);
    $int_pardil_id = mysql_insert_id();

    $str_date = ($str_date != '') ? $str_date : date('Y-m-d H:i:s');
    $dbl_version = 1.0;
    $str_sql = sprintf('INSERT INTO pardil_revisions (proposal, revisor, version, content, notes, info, timestamp) VALUES (%d, %d, %f, "%s","%s", "%s", "%s")', $int_pardil_id, $int_sender, $dbl_version, $str_content, $str_notes, $str_info, $str_date);
    mysql_query($str_sql);

    $int_status = ($bln_approve) ? 2 : 1;
    proc_r_status_new($int_pardil_id, $int_status, $str_date);

    return $int_pardil_id;
  }
  function proc_main_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_main SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }

  function proc_revision_new($int_pardil, $int_revisor, $dbl_version, $str_content, $str_notes, $str_info, $str_date='') {
    $str_content = addslashes($str_content); // Metindeki tırnak işaretleri sorun yatarmasın...
    $str_notes = addslashes($str_notes);
    $str_info = addslashes($str_info);
    $str_date = addslashes($str_date);
  
    $str_date = ($str_date != '') ? $str_date : date('Y-m-d H:i:s');
    $str_sql = sprintf('INSERT INTO pardil_revisions (proposal, revisor, version, content, notes, info, timestamp) VALUES (%d, %d, %f, "%s","%s", "%s", "%s")', $int_pardil, $int_sender, $dbl_version, $str_content, $str_notes, $str_info, $str_date);
    mysql_query($str_sql);
    return mysql_insert_id();
  }
  function proc_revision_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_revisions SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }


  // Test: revision_delete
  // Bir öneriye ait revizyonu silen prosedür.
  function proc_revision_delete($int_id) {
    return false;
  }
  
  // Test: pardil_delete
  // Öneri ve ilgili tüm kayıtları silen prosedür.
  function proc_pardil_delete($int_pardil, $bln_approve=false) {
    return false;
    if (!$bln_approve) {
      return false;
    }
    // Pardil_Images
    $str_sql = sprintf('DELETE FROM pardil_images WHERE proposal=%d', $int_pardil);
    mysql_query($str_sql);
    // Pardil_Maintainers
    $str_sql = sprintf('DELETE FROM pardil_maintainers WHERE proposal=%d', $int_pardil);
    mysql_query($str_sql);
    // Pardil_R_Releated
    $str_sql = sprintf('DELETE FROM pardil_r_releated WHERE proposal=%d OR proposal2=%d', $int_pardil, $int_pardil);
    mysql_query($str_sql);
    // Pardil_R_Roles
    $str_sql = sprintf('DELETE FROM pardil_r_releated WHERE proposal=%d', $int_pardil);
    mysql_query($str_sql);
    // Pardil_R_Status
    $str_sql = sprintf('DELETE FROM pardil_r_status WHERE proposal=%d', $int_pardil);
    mysql_query($str_sql);
    // Pardil_Revisions
    $str_sql = sprintf('DELETE FROM pardil_revisions WHERE proposal=%d', $int_pardil);
    mysql_query($str_sql);
    // Pardil_Main
    $str_sql = sprintf('DELETE FROM pardil_main WHERE id=%d', $int_pardil);
    mysql_query($str_sql);
    
    return true;
  }


  /* Ayarlar */

  function proc_getopt($str_key) {
    $str_key = addslashes($str_key); // Metindeki tırnak işaretleri sorun yatarmasın...
    
    return database_query_scalar(sprintf('SELECT value FROM options WHERE opt="%s"', $str_key));
  }
  function proc_setopt($str_key, $str_value) {
    $str_key = addslashes($str_key); // Metindeki tırnak işaretleri sorun yatarmasın...
    $str_value = addslashes($str_value);
    
    $mix_value = database_query_scalar(sprintf('SELECT value FROM options WHERE opt="%s"', $str_key));
    if ($mix_value === false) {
      $str_sql = sprintf('INSERT INTO options (opt,value) VALUES ("%s","%s")', $str_key, $str_value);
    }
    else {
      $str_sql = sprintf('UPDATE options SET value="%s" WHERE opt="%s"', $str_value, $str_key);
    }
    mysql_query($str_sql);
    return true;
  }
?>
