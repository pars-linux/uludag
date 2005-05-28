<?php
  
  if (defined('CONF_DATABASE_HOST')) {
    mysql_connect(CONF_DATABASE_HOST, CONF_DATABASE_USER, CONF_DATABASE_PASS) or die(__('Could not connect to database server.'));
    mysql_select_db(CONF_DATABASE_NAME) or die(__('Could not select database.'));
    
    $str_mysql_version = '4.1.0';
    if (version_compare($str_mysql_version, mysql_get_server_info()) == 1) {
      mysql_query('SET NAMES utf8');
    }
    else {
      //die(sprintf(__('MySQL %s or higher required.'), $str_mysql_version));
    }
  }
  else {
    die(__e('Missing configuration.'));
  }

  /*
    Yanıtı bir skaler veri olan sorgularda kullanılabilecek fonksiyon.
    Değer dönmezse "false" değerini verir.
  */
  function database_query_scalar($str_sql) {
    $res_sql = mysql_query($str_sql);
    if (mysql_num_rows($res_sql) == 1) {
      $arr_fetch = mysql_fetch_array($res_sql, MYSQL_NUM);
      return $arr_fetch[0];
    }
    else {
      return false;
    }
  }
  
  /*
    array('sütun' => 'yeni değer', ...) şeklindeki diziyi
    UPDATE sorgusunda kullanılabilen "sütun='yeni değer', ..." formatına
    çeviren fonksiyon
  */
  function database_updateStr($arr_update) {
    $arr_tmp = array();
    foreach ($arr_update as $str_column => $mix_value) {
      $arr_tmp[] = sprintf('%s="%s"', $str_column, addslashes($mix_value));
    }
    return join(', ', $arr_tmp);
  }

?>
