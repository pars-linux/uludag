<?php
  $_PSESSION = array();
  
  // 900 saniye hareketsiz olan oturumları kaldır.
  proc_session_expire(900);

  if (isset($_COOKIE['pardil_session']) && strlen($_COOKIE['pardil_session']) == 32) {
    $str_sql = sprintf('SELECT users.id, sessions.id AS session, users.username, users.email, users.name, users.level FROM users INNER JOIN sessions ON users.id=sessions.user WHERE sessions.id="%s"', addslashes($_COOKIE['pardil_session']));
    $res_sql = mysql_query($str_sql);
    if (mysql_num_rows($res_sql) == 1) {
      if (isset($_GET['exit']) || isset($_GET['logout']) || isset($_GET['quit'])) {
        proc_session_delete($_PSESSION['session']);
        setcookie('pardil_session', '');
        header('Location: login.php');
        exit;
      }
      $_PSESSION = mysql_fetch_array($res_sql, MYSQL_ASSOC);
      // Oturum bilgisini güncelle.
      proc_session_update($_PSESSION['id']);
    }
  }

  
?>
