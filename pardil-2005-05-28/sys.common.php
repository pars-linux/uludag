<?php
  // Min. konfigürasyonu yükle.
  require(dirname(__FILE__) . '/cfg/sys.define.php');
  
  // Özel fonksiyonları yükle.
  require(dirname(__FILE__) . '/sys/sys.lib.php');
  
  // Yerelleştirme dosyasını yükle.
  require(dirname(__FILE__) . '/sys/sys.gettext.php');
  
  // Veritabanı bağlantı dosyasını yükle.
  require(dirname(__FILE__) . '/sys/sys.database.php');
  
  // Veritabanı prosedürlerini & sorgularını yükle.
  require(dirname(__FILE__) . '/sys/sys.procedures.php');
 
  // Veritabanına kaydedilen konfigürasyonu yükle.
  require(dirname(__FILE__) . '/sys/sys.pconf.php');

  // Aksi belirtilmediyse oturum yönetim dosyasını yükle.
  if (!isset($_NOSESSION)) {
    require(dirname(__FILE__) . '/sys/sys.session.php');
  }

  // PHP konfigürasyonunu kontrol et.
  if (get_magic_quotes_gpc() == 1) {
    die(__('PHP\'s Magic Quotes option is set to ON, this is bad. It seems that this web server does not read .htaccess file. Please contact your server administrator.'));
  }
?>
