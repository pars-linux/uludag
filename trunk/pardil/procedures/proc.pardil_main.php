<?php

  // Pardil_Main, Pardil_Revisions

  // Yeni öneri ekle
  function proc_main_new($int_sender, $str_title, $str_abstract, $str_content, $str_info, $bln_approve=false, $str_date='') {
    $str_title = addslashes($str_title); // Metindeki tırnak işaretleri sorun yatarmasın...
    $str_abstract = addslashes($str_abstract);
    $str_contente = addslashes($str_contents);
    $str_info = addslashes($str_info);
    $str_date = addslashes($str_date);
    
    $str_sql = sprintf('INSERT INTO pardil_main (sender, title, abstract) VALUES (%d, "%s","%s")', $int_sender, $str_title, $str_abstract);
    mysql_query($str_sql);
    $int_pardil_id = mysql_insert_id();

    $str_date = ($str_date != '') ? $str_date : date('Y-m-d H:i:s');
    $dbl_version = 1.0;
    $str_sql = sprintf('INSERT INTO pardil_revisions (proposal, revisor, version, content, info, timestamp) VALUES (%d, %d, %f, "%s", "%s", "%s")', $int_pardil_id, $int_sender, $dbl_version, $str_content, $str_info, $str_date);
    mysql_query($str_sql);

    $int_status = ($bln_approve) ? 2 : 1;
    proc_r_status_new($int_pardil_id, $int_status, $str_date);

    return $int_pardil_id;
  }

  // Öneri bilgilerini değiştir
  function proc_main_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_main SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }

  // Öneriye yeni revizyon ekle
  function proc_revision_new($int_pardil, $int_revisor, $dbl_version, $str_content, $str_info, $str_date='') {
    $str_content = addslashes($str_content); // Metindeki tırnak işaretleri sorun yatarmasın...
    $str_info = addslashes($str_info);
    $str_date = addslashes($str_date);
  
    $str_date = ($str_date != '') ? $str_date : date('Y-m-d H:i:s');
    $str_sql = sprintf('INSERT INTO pardil_revisions (proposal, revisor, version, content, info, timestamp) VALUES (%d, %d, %f, "%s", "%s", "%s")', $int_pardil, $int_revisor, $dbl_version, $str_content, $str_info, $str_date);
    mysql_query($str_sql);
    return mysql_insert_id();
  }

  // Revizyon bilgilerini değiştir
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
    // TODO: Yapılacak
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

?>
