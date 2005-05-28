<?php

  // Bağlantılı öneriler
  // Aynı anda birden fazla öneri birbirine bağlı olabilir, yeni ilişki eklenirken bir önceki ilişkinin sonlandırılması gerekmez.

  // İki öneriyi birbiriyle ilişkilendir
  function proc_r_relation_new($int_pardil1, $int_pardil2) {
    $str_dateB = date('Y-m-d H:i:s');
    $str_dateE = '9999.12.31 23:59:59';
    $str_sql = sprintf('INSERT INTO pardil_r_releated (proposal, proposal, timestampB, timestampE) VALUES (%d, %d, "%s", "%s")', $int_pardil, $int_pardil2, $str_dateB, $str_dateE);
    mysql_query($str_sql);
    return mysql_insert_id();
  }

  // Öneri ilişkisini sonlandır
  function proc_r_relation_delete($int_id) {
    // Bu ilişki silinemez, bitiş tarihini bugüne eşitlenir, ilişkiyi sonlandırılır.
    return proc_r_relation_update($int_id, array('timestampE' => date('Y-m-d H:i:s')));
  }

  // Öneri ilişkisi bilgisini güncelle
  function proc_r_relation_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_r_releated SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }

?>
