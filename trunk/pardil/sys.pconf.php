<?php

  // Varsayılan değerler:
  $_PCONF = array();

  $_PCONF['site_name'] = 'Pardil';
  $_PCONF['site_title'] = 'Pardus İyileştirme Listesi';
  $_PCONF['site_url'] = 'http://pardil.uludag.org.tr/';
  
  $_PCONF['session_label'] = 'pardil';
  $_PCONF['session_timeout'] = 900;
  
  $_PCONF['temp_password_timeout'] = 900;

  $_PCONF['register_activation_required'] = 'true';
  
  $_PCONF['level_proposal_new'] = 1;
  $_PCONF['level_proposal_new_approved'] = 3;

  // Veritabanından gelen değerler:
  $str_sql = 'SELECT opt,value FROM options';
  $res_sql = mysql_query($str_sql);

  // Veritabanındaki tüm değerleri bir diziye yükle
  while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_NUM)) {
  
    $_PCONF[$arr_fetch[0]] = $arr_fetch[1];

  }

  //
  function getop($str_label) {
  
    global $_PCONF;
    return $_PCONF[$str_label];

  }

?>
