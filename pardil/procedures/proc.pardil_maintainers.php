<?php

  // Öneriye bakıcı (sorumlu) ekle
  function proc_maintainers_new($int_pardil, $int_user) {
    $str_dateB = date('Y-m-d H:i:s');
    $str_dateE = '9999.12.31 23:59:59';
    $str_sql = sprintf('INSERT INTO pardil_maintainers (proposal, user, timestampB, timestampE) VALUES (%d, %d, "%s", "%s")', $int_pardil, $int_user, $str_dateB, $str_dateE);
    mysql_query($str_sql);
    return mysql_insert_id();
  }

  // Öneri - Bakıcı ilişkisini sonlandır
  function proc_maintainers_delete($int_id) {
    // Bu ilişki silinemez, bitiş tarihini bugüne eşitlenir, ilişkiyi sonlandırılır.
    return proc_maintainers_update($int_id, array('timestampE' => date('Y-m-d H:i:s')));
  }

  // Öneri - Bakıcı ilişkisini değiştir
  function proc_maintainers_update($int_id, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_maintainers SET %s WHERE id=%d', $str_set, $int_id);
    mysql_query($str_sql);
    return true;
  }

?>
