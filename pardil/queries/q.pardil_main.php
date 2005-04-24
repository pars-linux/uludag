<?php

  // Böyle bir öneri var mı...
  function query_proposal_exists($int_id) {
    $str_sql = sprintf('SELECT Count(*) FROM pardil_revisions WHERE proposal=%d', $int_id);
    return (database_query_scalar($str_sql) > 0);
  }

  // Bu sürüme sahip bir öneri var mı...
  function query_revision_exists($int_id, $dbl_rev) {
    $str_sql = sprintf('SELECT Count(*) FROM pardil_revisions WHERE proposal=%d AND version=%f', $int_id, $dbl_rev);
    return (database_query_scalar($str_sql) == 1);
  }
  
  // Son revizyon numarası
  function query_revision_latest($int_id) {
    $str_sql = sprintf('SELECT pardil_revisions.version FROM pardil_main INNER JOIN pardil_revisions ON pardil_main.id=pardil_revisions.proposal WHERE pardil_main.id=%d ORDER BY pardil_revisions.id DESC LIMIT 1', $int_id);
    return database_query_scalar($str_sql);
  }

  // Öneri
  function query_proposal_data($int_id, $dbl_rev) {
    $str_sql = sprintf('SELECT pardil_main.id, pardil_main.title, pardil_main.abstract, pardil_revisions.content, pardil_revisions.version, pardil_revisions.timestamp, pardil_revisions.info FROM pardil_main INNER JOIN pardil_revisions ON pardil_main.id=pardil_revisions.proposal WHERE pardil_main.id=%d AND pardil_revisions.version=%f', $int_id, $dbl_rev);
    $res_sql = mysql_query($str_sql);
    return mysql_fetch_array($res_sql, MYSQL_ASSOC);
  }
  
  // Bağlantılı Başlıklar:
  function query_proposal_releated($int_id) {
    $str_date = date('Y-m-d H:i:s');
    $str_sql = sprintf('SELECT pardil_main2.id, pardil_main2.title FROM pardil_main INNER JOIN pardil_r_releated ON pardil_r_releated.proposal=pardil_main.id INNER JOIN pardil_main AS pardil_main2 ON pardil_main2.id=pardil_r_releated.proposal2 WHERE pardil_main.id=%1$d AND pardil_r_releated.timestampB<="%2$s" AND pardil_r_releated.timestampE>="%2$s"', $int_id, $str_date);
    $res_sql = mysql_query($str_sql);
    $arr_releated_list = array();
    while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
      $arr_releated_list[] = $arr_fetch;
    }
    $str_sql = sprintf('SELECT pardil_main.id, pardil_main.title FROM pardil_main INNER JOIN pardil_r_releated ON pardil_r_releated.proposal=pardil_main.id INNER JOIN pardil_main AS pardil_main2 ON pardil_main2.id=pardil_r_releated.proposal2 WHERE pardil_main2.id=%1$d AND pardil_r_releated.timestampB<="%2$s" AND pardil_r_releated.timestampE>="%2$s"', $int_id, $str_date);
    $res_sql = mysql_query($str_sql);
    while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
      $arr_releated_list[] = $arr_fetch;
    }
    return $arr_releated_list; 
  }

  // Öneri Durumu:
  function query_proposal_status($int_id) {
    $str_date = date('Y-m-d H:i:s');
    $str_sql = sprintf('SELECT pardil_status.name FROM pardil_main INNER JOIN pardil_r_status ON pardil_r_status.proposal=pardil_main.id INNER JOIN pardil_status ON pardil_r_status.status=pardil_status.id WHERE pardil_main.id=%1$d AND timestampB<="%2$s" AND timestampE>="%2$s"', $int_id, $str_date);
    return database_query_scalar($str_sql);
  }

  // Sorumlular:
  function query_proposal_maintainers($int_id) {
    $str_date = date('Y-m-d H:i:s');
    $str_sql = sprintf('SELECT name, email FROM pardil_main INNER JOIN pardil_maintainers ON pardil_maintainers.proposal=pardil_main.id INNER JOIN users ON users.id=pardil_maintainers.user WHERE pardil_main.id=%1$d AND pardil_maintainers.timestampb<="%2$s" AND pardil_maintainers.timestampe>="%2$s"', $int_id, $str_date);
    $res_sql = mysql_query($str_sql);
    $arr_maintainer_list = array();
    while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
      $arr_maintainer_list[] = $arr_fetch;
    }
    return $arr_maintainer_list; 
  }

  // Sorumlu mu değil mi...
  function query_proposal_is_maintainer($int_id, $int_user) {
    $str_date = date('Y-m-d H:i:s');
    $str_sql = sprintf('SELECT Count(*) FROM pardil_maintainers WHERE TimestampB<="%1$s" AND "%1$s" <=TimestampE AND user=%2$d AND proposal=%3$d', $str_date, $int_user, $int_id);
    return (database_query_scalar($str_sql) == 1);
  }
 
  // Sürüm Geçmişi:
  function query_proposal_revisions($int_id) {
    $str_sql = sprintf('SELECT pardil_revisions.version, pardil_revisions.info, pardil_revisions_r_users.name AS pardil_revisor, pardil_revisions_r_users.email AS pardil_revisor_mail, pardil_revisions.timestamp FROM pardil_revisions INNER JOIN users AS pardil_revisions_r_users ON pardil_revisions_r_users.id=pardil_revisions.revisor WHERE pardil_revisions.proposal=%d ORDER BY pardil_revisions.timestamp DESC', $int_id);
    $res_sql = mysql_query($str_sql);
    $arr_revisions_list = array();
    while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
      $arr_revisions_list[] = $arr_fetch;
    }
    return $arr_revisions_list;
  }

?>
