<?php

  // 'procedures' dizini altındaki tüm prosedür tanımlarını yükle

  if (function_exists('scandir')) {
    $arr_files = scandir('procedures');
    for ($i = 0; $i < count($arr_files); $i++) {
      if (substr($arr_files[$i], 0, 5) == 'proc.') {
        include('procedures/' . $arr_files[$i]);
      }
    }
    $arr_files = scandir('queries');
    for ($i = 0; $i < count($arr_files); $i++) {
      if (substr($arr_files[$i], 0, 2) == 'q.') {
        include('queries/' . $arr_files[$i]);
      }
    }
  }
  else {
    $str_dir = 'procedures';
    $res_dir  = opendir($str_dir);
    while (false !== ($str_fname = readdir($res_dir))) {
      if (substr($str_fname, 0, 5) == 'proc.') {
        include('procedures/' . $str_fname);
      }
    }
    $str_dir = 'queries';
    $res_dir  = opendir($str_dir);
    while (false !== ($str_fname = readdir($res_dir))) {
      if (substr($str_fname, 0, 2) == 'q.') {
        include('procedures/' . $str_fname);
      }
    }
  }

?>
