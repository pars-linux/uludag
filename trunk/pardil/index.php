<?php
  require('cfg/sys.define.php');
  require('sys/sys.gettext.php');
  require('sys/sys.database.php');
  require('sys/sys.procedures.php');
  require('sys/sys.pconf.php');
  require('sys/sys.session.php');
  
  require('class/class.template.php');

  $str_sql = sprintf('SELECT pardil_main.id, pardil_main.title FROM pardil_main');
  $res_sql = mysql_query($str_sql);
  $arr_list = array();
  while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
    $arr_list[] = $arr_fetch;
  }

  $_PCONF['title'] = $_PCONF['site_title'];
  $obj_page = new template('tpl/tpl.index.php');
  $obj_page->setvar('_PSESSION', $_PSESSION);
  $obj_page->setvar('arr_list', $arr_list);
  $obj_page->flush();
?>
