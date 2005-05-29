<?php

  function msg($str_text) {
    $str_line = $_SERVER['REMOTE_ADDR'] . ':' . nl2br(htmlspecialchars($str_text)) . "\n";
    $res_file = fopen('sohbet.log', 'a');
    fwrite($res_file, $str_line);
    fclose($res_file);
    return 1;
  }

  function getmsg($int_startfrom) {
    $arr_lines = explode("\n", file_get_contents('sohbet.log'));
    $arr_list = array();
    for ($i = $int_startfrom; $i < count($arr_lines) - 1; $i++) {
      $str_ip = substr($arr_lines[$i], 0, strpos($arr_lines[$i], ':'));
      $str_msg = substr($arr_lines[$i], strpos($arr_lines[$i], ':') + 1, strlen($arr_lines[$i]) - strpos($arr_lines[$i], ':') - 1);
      $arr_list[] = array('id' => $i, 'ip' => $str_ip, 'msg' => $str_msg);
    }

    return $arr_list;
  }


  require 'xhr.php';
  $obj_xhr = new xhr();
  $obj_xhr->register('msg');
  $obj_xhr->register('getmsg');
  $obj_xhr->handle();
?>
