<?php
  if (defined('CONF_DATABASE_HOST')) {
    mysql_connect(CONF_DATABASE_HOST, CONF_DATABASE_USER, CONF_DATABASE_PASS) or die(MSG_DATABASE_CONNECT_ERROR);
    mysql_select_db(CONF_DATABASE_NAME) or die(MSG_DATABASE_SELECT_ERROR);
  }
  else {
    die('Configuration error.');
  }

  function database_query_scalar($str_sql) {
    $res_sql = mysql_query($str_sql);
    $arr_fetch = mysql_fetch_array($res_sql, MYSQL_NUM);
    return $arr_fetch[0];
  }
  
  function database_updateStr($arr_update) {
    $arr_tmp = array();
    foreach ($arr_update as $str_column => $mix_value) {
      $arr_tmp[] = sprintf('%s="%s"', $str_column, $mix_value);
    }
    return join(', ', $arr_tmp);
  }

?>
