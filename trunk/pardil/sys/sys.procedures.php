<?php

  // 'procedures' dizini altındaki tüm prosedür tanımlarını yükle

  if (function_exists('scandir')) {
    $arr_files = scandir(dirname(__FILE__) . '/../procedures');
    for ($i = 0; $i < count($arr_files); $i++) {
      if (substr($arr_files[$i], 0, 5) == 'proc.') {
        include(dirname(__FILE__) . '/../procedures/' . $arr_files[$i]);
      }
    }
    $arr_files = scandir(dirname(__FILE__) . '/../queries');
    for ($i = 0; $i < count($arr_files); $i++) {
      if (substr($arr_files[$i], 0, 2) == 'q.') {
        include(dirname(__FILE__) . '/../queries/' . $arr_files[$i]);
      }
    }
  }
  else {
    $str_dir = dirname(__FILE__) . '/../procedures';
    $res_dir  = opendir($str_dir);
    while (false !== ($str_fname = readdir($res_dir))) {
      if (substr($str_fname, 0, 5) == 'proc.') {
        include($str_dir . '/' . $str_fname);
      }
    }
    $str_dir = dirname(__FILE__) . '/../queries';
    $res_dir  = opendir($str_dir);
    while (false !== ($str_fname = readdir($res_dir))) {
      if (substr($str_fname, 0, 2) == 'q.') {
        include($str_dir . '/' . $str_fname);
      }
    }
  }

?>
