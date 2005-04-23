<?php

  require('cfg/sys.define.php');
  require('sys/sys.gettext.php');
  require('sys/sys.database.php');
  require('sys/sys.procedures.php');
  require('sys/sys.pconf.php');
  require('sys/sys.session.php');

  require('class/class.template.php');

  // ID & sürüm kontrolü
  if (!isset($_GET['id'])) {
    header('Location: notfound.php');
    exit;
  }
  if (isset($_GET['rev'])) {
    $int_count = database_query_scalar(sprintf('SELECT Count(*) FROM pardil_revisions WHERE proposal=%d', $_GET['id']));
    if ($int_count == 0) {
      header('Location: notfound.php');
      exit;
    }
  }

  // Öneri No
  $int_pardil_id = $_GET['id'];

  // Son Revizyon:
  $str_sql = sprintf('SELECT pardil_revisions.version FROM pardil_main INNER JOIN pardil_revisions ON pardil_main.id=pardil_revisions.proposal WHERE pardil_main.id=%d ORDER BY pardil_revisions.id DESC', $int_pardil_id);
  $res_sql = mysql_query($str_sql);
  $arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC);
  $dbl_pardil_lastrev = $arr_fetch['version'];

  // Revizyon:
  $dbl_pardil_rev = (isset($_GET['rev'])) ? $_GET['rev'] : $dbl_pardil_lastrev;

  // Önceki ve sonraki öneriler:
  $str_sql = sprintf('SELECT pardil_main.id, pardil_main.title FROM pardil_main INNER JOIN pardil_r_status ON pardil_r_status.proposal=pardil_main.id WHERE pardil_r_status.status=2 AND pardil_main.id<%d ORDER BY pardil_main.id DESC LIMIT 1', $int_pardil_id);
  $res_sql = mysql_query($str_sql);
  if (mysql_num_rows($res_sql) == 1) {
    $arr_pardil_prev = mysql_fetch_array($res_sql, MYSQL_ASSOC);
  }
  $str_sql = sprintf('SELECT pardil_main.id, pardil_main.title FROM pardil_main INNER JOIN pardil_r_status ON pardil_r_status.proposal=pardil_main.id WHERE pardil_r_status.status=2 AND pardil_main.id>%d ORDER BY pardil_main.id ASC LIMIT 1', $int_pardil_id);
  $res_sql = mysql_query($str_sql);
  if (mysql_num_rows($res_sql) == 1) {
    $arr_pardil_next = mysql_fetch_array($res_sql, MYSQL_ASSOC);
  }

  // Öneri:
  $str_time = date('Y-m-d H:i:s');
  $str_sql = sprintf('SELECT pardil_main.id, pardil_main.title, pardil_main.abstract, pardil_revisions.content, pardil_revisions.notes, pardil_revisions.version, pardil_revisions.timestamp FROM pardil_main INNER JOIN pardil_revisions ON pardil_main.id=pardil_revisions.proposal WHERE pardil_main.id=%d AND pardil_revisions.version=%f', $int_pardil_id, $dbl_pardil_rev);
  $res_sql = mysql_query($str_sql);
  $arr_pardil_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC);

  //
  // $arr_pardil_fetch['abstract'] = htmlspecialchars($arr_pardil_fetch['abstract']);
  //

  // Öneri İçeriği ve İçindekiler Listesi:
  $arr_pardil_fetch['content'] = '<?xml version="1.0" encoding="utf-8"?><pardil>' . $arr_pardil_fetch['content'] . '</pardil>';
  $res_xml = simplexml_load_string($arr_pardil_fetch['content']);
  $int_pardil_content = 1;
  $arr_pardil_content = array();
  foreach ($res_xml->children() as $res_node) {
    $str_title = $res_node->title;
    $str_body = substr($res_node->body->asXML(), 6, strlen($res_node->body->asXML()) - 13);
    //
    // $str_title = htmlspecialchars($str_title);
    // $str_body = htmlspecialchars($str_body);
    //
    $arr_pardil_content[] = array('no' => $int_pardil_content, 'title' => $str_title, 'body' => $str_body);
    $int_pardil_content++;
  }
  // ÖNEMLİ NOT:
  // Şimdilik, veritabanından gelen kod aynen ekrana yazdırılıyor, çünkü
  // HTML kodu içeriyor. Bu XSS saldırılarına sebep olabilir. İleride, 
  // veritabanından gelen kod XSL'den geçirilecek ve çıktısı ekrana 
  // yazdırılacak. XSL dönüşümü öncesi tabii ki DTD kullanılacak.
  // Aynı mevzu "Öneri Notları" için de geçerli.

  // Öneri Notları
  $arr_pardil_fetch['notes'] = '<?xml version="1.0" encoding="utf-8"?><notes>' . $arr_pardil_fetch['notes'] . '</notes>';
  $res_xml = simplexml_load_string($arr_pardil_fetch['notes']);
  $int_pardil_notes = 1;
  $arr_pardil_notes = array();
  foreach ($res_xml->children() as $res_node) {
    $str_body = substr($res_node->asXML(), 6, strlen($res_node->asXML()) - 13);
    //
    // $str_body = htmlspecialchars($str_body);
    //
    $arr_pardil_notes[] = array('no' => $int_pardil_notes, 'body' => $str_body);
    $int_pardil_notes++;
  }

  // Bağlantılı Başlıklar:
  $str_sql = sprintf('SELECT pardil_main2.id, pardil_main2.title FROM pardil_main INNER JOIN pardil_r_releated ON pardil_r_releated.proposal=pardil_main.id INNER JOIN pardil_main AS pardil_main2 ON pardil_main2.id=pardil_r_releated.proposal2 WHERE pardil_main.id=%d AND pardil_r_releated.timestampB<="%s" AND pardil_r_releated.timestampE>="%s"', $int_pardil_id, $str_time, $str_time);
  $res_sql = mysql_query($str_sql);
  $arr_releated_list = array();
  while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
    $arr_releated_list[] = $arr_fetch;
  }
  $str_sql = sprintf('SELECT pardil_main.id, pardil_main.title FROM pardil_main INNER JOIN pardil_r_releated ON pardil_r_releated.proposal=pardil_main.id INNER JOIN pardil_main AS pardil_main2 ON pardil_main2.id=pardil_r_releated.proposal2 WHERE pardil_main2.id=%d AND pardil_r_releated.timestampB<="%s" AND pardil_r_releated.timestampE>="%s"', $int_pardil_id, $str_time, $str_time);
  $res_sql = mysql_query($str_sql);
  while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
    $arr_releated_list[] = $arr_fetch;
  }

  // Öneri Durumu:
  $str_sql = sprintf('SELECT pardil_status.name FROM pardil_main INNER JOIN pardil_r_status ON pardil_r_status.proposal=pardil_main.id INNER JOIN pardil_status ON pardil_r_status.status=pardil_status.id WHERE pardil_main.id=%d AND timestampB<="%s" AND timestampE>="%s"', $int_pardil_id, $str_time, $str_time);
  $res_sql = mysql_query($str_sql);
  $arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC);
  $str_pardil_status = $arr_fetch['name'];


  // Sorumlular:
  $str_sql = sprintf('SELECT name, email FROM pardil_main INNER JOIN pardil_maintainers ON pardil_maintainers.proposal=pardil_main.id INNER JOIN users ON users.id=pardil_maintainers.user WHERE pardil_main.id=%d AND pardil_maintainers.timestampB<="%s" AND pardil_maintainers.timestampE>="%s"', $int_pardil_id, $str_time, $str_time);
  $res_sql = mysql_query($str_sql);
  $arr_maintainer_list = array();
  while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
    $arr_maintainer_list[] = $arr_fetch;
  }

  // Sürüm Geçmişi:
  $str_sql = sprintf('SELECT pardil_revisions.version, pardil_revisions.info, pardil_revisions_r_users.name AS pardil_revisor, pardil_revisions_r_users.email AS pardil_revisor_mail, pardil_revisions.timestamp FROM pardil_revisions INNER JOIN users AS pardil_revisions_r_users ON pardil_revisions_r_users.id=pardil_revisions.revisor WHERE pardil_revisions.proposal=%d ORDER BY pardil_revisions.timestamp DESC', $int_pardil_id);
  $res_sql = mysql_query($str_sql);
  $arr_revisions_list = array();
  while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
    $arr_revisions_list[] = $arr_fetch;
  }

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . $arr_pardil_fetch['title'];

  $obj_page = new template('tpl/tpl.proposal.php');
  
  $obj_page->setvar('arr_proposal', $arr_pardil_fetch);
  $obj_page->setvar('arr_proposal_prev', $arr_pardil_prev);
  $obj_page->setvar('arr_proposal_next', $arr_pardil_next);
  $obj_page->setvar('str_proposal_status', $str_pardil_status);
  $obj_page->setvar('arr_proposal_content', $arr_pardil_content);
  $obj_page->setvar('arr_maintainers', $arr_maintainer_list);
  $obj_page->setvar('arr_releated', $arr_releated_list);
  $obj_page->setvar('arr_notes', $arr_pardil_notes);
  $obj_page->setvar('arr_revisions', $arr_revisions_list);
  
  $obj_page->flush();
?>
