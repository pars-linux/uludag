<?php
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
?>
