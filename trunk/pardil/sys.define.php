<?php
  define('CONF_DATABASE_HOST', 'localhost');
  define('CONF_DATABASE_USER', 'pardil_user');
  define('CONF_DATABASE_PASS', '');
  define('CONF_DATABASE_NAME', 'pardil');

  define('CONF_LOCALE', 'tr_TR.utf8');

  define('MSG_DATABASE_CONNECT_ERROR', '<b>Ölümcül Hata:</b> Veritabaný baðlantýsý kurulamadý.');
  define('MSG_DATABASE_SELECT_ERROR', '<b>Ölümcül Hata:</b> Veritabaný seçimi yapýlamadý.');


  // l10n
  setlocale(LC_ALL, CONF_LOCALE);
?>
