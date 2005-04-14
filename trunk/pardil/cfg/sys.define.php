<?php
  define('CONF_DATABASE_HOST', 'localhost');
  define('CONF_DATABASE_USER', 'pardil_user');
  define('CONF_DATABASE_PASS', '');
  define('CONF_DATABASE_NAME', 'pardil');

  define('MSG_DATABASE_CONNECT_ERROR', '<b>Ölümcül Hata:</b> Veritabanı bağlantısı kurulamadı.');
  define('MSG_DATABASE_SELECT_ERROR', '<b>Ölümcül Hata:</b> Veritabanı seçimi yapılamadı.');

  define('CONF_DOMAIN', 'pardil');
  define('CONF_LOCALE', 'tr_TR.utf8');

  $_PCONF = array();

  $_PCONF['root'] = realpath(dirname(__FILE__) . '/..');

?>
