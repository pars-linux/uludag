<?php
  // Min. konfigürasyonu yükle.
  require(dirname(__FILE__) . '/cfg/sys.define.php');
  
  // 
  require(dirname(__FILE__) . '/sys/sys.lib.php');
  
  // Yerelleştirme dosyasını yükle.
  require(dirname(__FILE__) . '/sys/sys.gettext.php');
  
  // Veritabanı bağlantı dosyasını yükle.
  require(dirname(__FILE__) . '/sys/sys.database.php');
  
  // Veritabanı prosedürlerini & sorgularını yükle.
  require(dirname(__FILE__) . '/sys/sys.procedures.php');
 
  // Veritabanına kaydedilen konfigürasyonu yükle.
  require(dirname(__FILE__) . '/sys/sys.pconf.php');

  // Aksi belirtilmedikçe oturum yönetim dosyasını yükle.
  if (!isset($_NOSESSION)) {
    require(dirname(__FILE__) . '/sys/sys.session.php');
  }
?>
