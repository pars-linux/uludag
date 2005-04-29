<?php
  require(dirname(__FILE__). '/sys.common.php');
  
  require(dirname(__FILE__) . '/class/class.template.php');

  // Erişim seviyesi
  $int_level = getop('level_proposal_edit');

  // Bu liste, Pardil'i test etmek isteyenler için oluşturulan geçici bir liste.
  $str_sql = sprintf('SELECT pardil_main.id, pardil_main.title FROM pardil_main');
  $res_sql = mysql_query($str_sql);
  $arr_list = array();
  while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
    // Bakıcı mı değil mi?
    $bln_maintainer = query_proposal_is_maintainer($arr_fetch['id'], $_PSESSION['id']);
    // Seviyesi yeterli değilse veya bakıcı değilse izin verme
    if ($int_level > $_PSESSION['level'] && !$bln_maintainer) {
      $arr_fetch['edit'] = false;
    }
    else {
      $arr_fetch['edit'] = true;
    }
    $arr_list[] = $arr_fetch;
  }

  $_PCONF['title'] = $_PCONF['site_title'];
  $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.index.php');
  $obj_page->setvar('_PSESSION', $_PSESSION);
  $obj_page->setvar('arr_list', $arr_list);
  $obj_page->flush();
?>
