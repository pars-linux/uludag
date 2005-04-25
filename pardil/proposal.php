<?php

  require(dirname(__FILE__) . '/sys.common.php');

  require(dirname(__FILE__) . '/class/class.template.php');

  // ID & sürüm kontrolü
  if (!isset($_GET['id'])) {
    header('Location: notfound.php');
    exit;
  }
  elseif (!query_proposal_exists($_GET['id'])) {
    header('Location: notfound.php');
    exit;
  }
  if (isset($_GET['rev']) && !query_revision_exists($_GET['id'], $_GET['rev'])) {
    header('Location: notfound.php');
    exit;
  }

  // Öneri No
  $int_pardil_id = $_GET['id'];

  // Son Revizyon:
  $dbl_pardil_lastrev = query_revision_latest($int_pardil_id);

  // Revizyon:
  $dbl_pardil_rev = (isset($_GET['rev'])) ? $_GET['rev'] : $dbl_pardil_lastrev;

  // Önceki ve sonraki öneriler:
  // İleri - Geri türü bağlantılar kullanılabilir...
  /*
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
  */

  // Öneri:
  $arr_pardil_fetch = query_proposal_data($int_pardil_id, $dbl_pardil_rev);

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


  // Bağlantılı Başlıklar:
  $arr_releated_list = query_proposal_releated($int_pardil_id);

  // Öneri Durumu:
  $str_pardil_status = query_proposal_status($int_pardil_id);

  // Sorumlular:
  $arr_maintainer_list = query_proposal_maintainers($int_pardil_id);

  // Sürüm Geçmişi:
  $arr_revisions_list = query_proposal_revisions($int_pardil_id);

  // Temayı yükle
  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . $arr_pardil_fetch['title'];
  $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.proposal.php');

  $obj_page->setvar('arr_proposal', $arr_pardil_fetch);
  /*
  $obj_page->setvar('arr_proposal_prev', $arr_pardil_prev);
  $obj_page->setvar('arr_proposal_next', $arr_pardil_next);
  */
  $obj_page->setvar('str_proposal_status', $str_pardil_status);
  $obj_page->setvar('arr_proposal_content', $arr_pardil_content);
  $obj_page->setvar('arr_maintainers', $arr_maintainer_list);
  $obj_page->setvar('arr_releated', $arr_releated_list);
  $obj_page->setvar('arr_revisions', $arr_revisions_list);
  
  $obj_page->flush();
?>
