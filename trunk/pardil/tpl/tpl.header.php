<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="tr">
  <head>
    <title><?php echo $_PCONF['title'] ?></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" href="<?php echo $_PCONF['site_url']; ?>style.css" type="text/css" />
    <link rel="stylesheet" href="<?php echo $_PCONF['site_url']; ?>proposal.css" type="text/css" />
    <link rel="icon" type="image/png" href="<?php echo $_PCONF['site_url']; ?>images/favicon.png"/>
    <script type="text/javascript" src="<?php echo $_PCONF['site_url']; ?>class/m_xhr.js"></script>
    <script>
      function tr_session() {
        // Belirli periyotlarla oturumu güncelleyen XHR süreci
        // Bir sayfada, uzun süre hareketsiz kalındığında oturumun 
        // kapanmasını engellemek için kulanılıyor.
        // TODO: Fare & klavye hareketlerine duyarlı hale getirilecek...
        xhr_php_process('<?php echo $_PCONF['site_url']; ?>xhr/xhr.session.php', 'session', '', 'cb_session');
      }
      function cb_session(op, req, obj) {
        if (obj == 'true') {
          setTimeout('tr_session()', 10000);
          // Oturum bilgileri bir kutuya yazdırılabilir...
          /*
          window.status = new Date().toString();
          */
        }
      }
      
      function init() {
        setTimeout('tr_session()', 10000);
      }
    </script>
  </head>
  <body onload="init()">
    <div id="container">
      <div id="header">
        <div id="logo"><a href="<?php echo $_PCONF['site_url']; ?>index.php"><img src="<?php echo $_PCONF['site_url']; ?>images/logo2.png" alt="Pardil"/></a></div>
      </div>
      <div id="menu">
        &nbsp;
      </div>
