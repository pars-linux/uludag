<?php
  // Süresi geçmiş geçici şifreleri yoket
  proc_password_expire(getop('temp_password_timeout'));
  
  // Süresi geçmiş oturumları yoket
  proc_session_expire(getop('session_timeout'));
  
  // Oturum bilgiler
  $_PSESSION = array();
  
  // Oturum etiketi
  $str_session_label = getop('session_label');

  // Açık oturum var mı, kontrol et
  if (isset($_COOKIE[$str_session_label]) && strlen($_COOKIE[$str_session_label]) == 32) {
  
    // Oturum kodu kontrolü
    $str_sql = sprintf('SELECT users.id, sessions.id AS session, users.username, users.email, users.name, users.level FROM users INNER JOIN sessions ON users.id=sessions.user WHERE sessions.id="%s"', $_COOKIE[$str_session_label]);
    $res_sql = mysql_query($str_sql);
    
    if (mysql_num_rows($res_sql) == 1) {
    
      // Eğer oturum kodu veritabanında buluyorsa:
      // 1. Sorgudan gelen tüm bilgileri bir kenara yaz
      $_PSESSION = mysql_fetch_array($res_sql, MYSQL_ASSOC);
      
      // 2. Oturum bilgisini tazele
      proc_session_init($_PSESSION['id']);
      
    }
    else {
    
      // Oturum kodu veritabanında bulunmuyorsa,
      // 1. Oturum ömrü dolmuştur
      // 2. Sevgili ziyaretçimiz bir iş çevirmektedir
      
    }
    
  }

  // Açık bir oturum varsa ve çıkış isteği yapıldıysa
  if (isset($_PSESSION['id']) && isset($_GET['logout'])) {
    
    // Oturumu yoket
    proc_session_delete($_PSESSION['session']);

    // Çerezi yoket
    setcookie($str_session_label, '');

    // Ziyaretçiyi çıkış sayfasına yönlendir
    header('Location: logout.php');
    exit;
    
  }

?>
