<?php
  /*
    $arr_errors dizisi içindeki, belirtilen hata metnini istenen
    formatta ekrana yazdırmak için kullanılan fonksiyon.
  */
  function print_error($str_format='%s', $str_name, $str_sub='') {
    global $arr_errors;
    if ($str_sub == '') {
      if (isset($arr_errors[$str_name])) {
        printf($str_format, $arr_errors[$str_name]);
      }
    }
    else {
      if (isset($arr_errors[$str_name][$str_sub])) {
        printf($str_format, $arr_errors[$str_name][$str_sub]);
      }
    }
  }
  /*
    Kullanım:
    =========
    <?php print_error('<div> class="hata">%s</div>', 'kayit_isim'); ?>
  */


  // Mevcut PHP sürümü "scandir" fonksiyonuna sahip değilse oluştur.
  if (!function_exists('scandir')) {
    function scandir($str_dir) {
      $res_dir  = opendir($str_dir);
      $arr_list = array();
      while (false !== ($str_fname = readdir($res_dir))) {
        $arr_list[] = $str_fname;
      }
      return $arr_list;
    }
  }
?>
