<?php
  define('CONF_DATABASE_HOST', 'localhost');
  define('CONF_DATABASE_USER', 'ugo');
  define('CONF_DATABASE_PASS', '123456aaa');
  define('CONF_DATABASE_NAME', 'ugos');

  define('CONF_LOCALE', 'tr_TR.utf8');

  define('MSG_DATABASE_CONNECT_ERROR', '<b>Ölümcül Hata:</b> Veritabaný baðlantýsý kurulamadý.');
  define('MSG_DATABASE_SELECT_ERROR', '<b>Ölümcül Hata:</b> Veritabaný seçimi yapýlamadý.');


  // l10n
  setlocale(LC_ALL, CONF_LOCALE);
?>
