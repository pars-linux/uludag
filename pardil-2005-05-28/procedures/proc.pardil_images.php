<?php

  // Yeni resim dosyası yükle & öneriyle ilişkilendir
  function proc_image_new($int_pardil, $str_filecontent, $str_contenttype) {
    $str_filecontent = addslashes($str_filecontent); // Metindeki tırnak işaretleri sorun yatarmasın...
    $str_contenttype = addslashes($str_contenttype);

    $str_sql = sprintf('INSERT INTO pardil_images (proposal, image, content_type) VALUES (%d, "%s", "%s")', $int_pardil, $str_filecontent, $str_contenttype);
    mysql_query($str_sql);
    return mysql_insert_id();
  }

  // Resim dosyasını sil
  function proc_image_delete($int_image) {
    $str_sql = sprintf('DELETE FROM pardil_images WHERE id=%d', $int_image);
    mysql_query($str_sql);
    return true;
  }

  // Resim dosyası bilgilerini güncelle
  /*
    INFO: proc.pardil_status.php dosyasındaki benzer
    isimli fonksiyona gözatın.
  */
  function proc_image_update($int_image, $arr_update) {
    if (count($arr_update) == 0) {
      return false;
    }
    $str_set = database_updateStr($arr_update);
    $str_sql = sprintf('UPDATE pardil_images SET %s WHERE id=%d', $str_set, $int_image);
    mysql_query($str_sql);
    return true;
  }

?>
