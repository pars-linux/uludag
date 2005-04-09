<?php

  // İşlemlere zaman sınırlaması koymak için kullanılacak fonksiyonlar

  // Yığına kayıt ekleme
  function proc_floodcontrol_add($str_label, $str_ip) {
    $str_date = date('Y-m-d H:i:s');
    $str_sql = sprintf('INSERT INTO floodcontrol (label, ip, timestamp) VALUES ("%s", "%s", "%s")', $str_label, $str_ip, $str_date);
    mysql_query($str_sql);
    return true;
  }
  
  // Süresi geçen kayıtları yoketme
  function proc_floodcontrol_expire($str_label, $int_timeout) {
    $str_date = date('Y-m-d H:i:s');
    $str_sql = sprintf('DELETE FROM floodcontrol WHERE label="%s" AND Unix_Timestamp("%s")-Unix_Timestamp(timestamp) > %d', $str_label, $str_date, $int_timeout);
    mysql_query($str_sql);
    return true;
  }
  
  // İşlem sayısını öğrenme
  function proc_floodcontrol_check($str_label, $str_ip) {
    $str_sql = sprintf('SELECT Count(*) FROM floodcontrol WHERE label="%s" AND ip="%s"', $str_label, $str_ip);
    return database_query_scalar($str_sql);
  }

  /*
    Bu sistem nasıl kulanılabilir?
    ==============================

    Misal, bir anket sisteminde, bir IP adresinden yapılan bağlantı 
    ile bir kereden fazla oy verilmesini engellemek için, *oy verirken*:

    proc_floodcontrol_add('anket_' . $anketno, $_SERVER['REMOTE_ADDR']);

    komutu kullanılabilir.

    Kaydın 24*60*60 saniye (= 1 Gün) sonra otomatik silinmesi için,

    proc_floodcontrol_expire(24*60*60);

    komutu kullanılabilir, bu fonksiyon, sayfa her açıldığında çalıştırılacak 
    şekilde kod içine yerleştirilmelidir.

    Oy verme işlemi öncesinde, o ip adresinin daha önce oy verip vermediğini 
    anlamak için

    if (proc_floodcontrol_check('anket_' . $anketno, $_SERVER['REMOTE_ADDR']) > 0) {
      ...
    }

    gibi bir ifade yeterli olacaktır.
  */
?>
