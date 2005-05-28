<?php

  // 'procedures' dizini altındaki tüm prosedür tanımlarını yükle

  $arr_files = scandir(dirname(__FILE__) . '/../procedures');
  for ($i = 0; $i < count($arr_files); $i++) {
    if (substr($arr_files[$i], 0, 5) == 'proc.') {
      include(dirname(__FILE__) . '/../procedures/' . $arr_files[$i]);
    }
  }
  
  // 'queries' dizini altındaki tüm prosedür tanımlarını yükle
  $arr_files = scandir(dirname(__FILE__) . '/../queries');
  for ($i = 0; $i < count($arr_files); $i++) {
    if (substr($arr_files[$i], 0, 2) == 'q.') {
      include(dirname(__FILE__) . '/../queries/' . $arr_files[$i]);
    }
  }
?>
