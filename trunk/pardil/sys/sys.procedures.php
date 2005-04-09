<?php

  // 'procedures' dizini altındaki tüm prosedür tanımlarını yükle
  $arr_files = scandir('procedures');
  for ($i = 0; $i < count($arr_files); $i++) {
    if (substr($arr_files[$i], 0, 5) == 'proc.') {
      include('procedures/' . $arr_files[$i]);
    }
  }

?>
