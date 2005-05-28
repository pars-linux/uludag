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

  // Erişim seviyesi
  $int_level = getop('level_proposal_edit');

  // Bakıcı mı değil mi?
  $bln_maintainer = query_proposal_is_maintainer($int_pardil_id, $_PSESSION['id']);

  // Seviyesi yeterli değilse ve bakıcı değilse izin verme
  if ($int_level > $_PSESSION['level'] && !$bln_maintainer) {
    header('Location: denied.php');
    exit;
  }


  // Denetimler
  $arr_errors = array();
  if (isset($_POST['edit_proposal'])) {
    // Başlık
    if (strlen($_POST['new_title']) == 0) {
      $arr_errors['new_title'] = __('Title should be written.');
    }
    // Özet
    if (strlen($_POST['new_abstract']) == 0) {
      $arr_errors['new_abstract'] = __('Abstract should be written.');
    }
    // Bölümler
    if (isset($_POST['new_content_title']) && count($_POST['new_content_title']) > 0) {
      foreach ($_POST['new_content_title'] as $int_num => $str_title) {
        $str_body = $_POST['new_content_body'][$int_num];
        if (strlen($str_body) == 0) {
          $arr_errors['new_content_title'][$int_num] = sprintf(__('Section "%s" should be written. If you don\'t want it, remove it.'), htmlspecialchars($str_title));
        }
      }
    }
    else {
      $arr_errors['new_content_new_title'] = __('At least one section should be created.');
    }
    // Sürüm Notları
    if (strlen($_POST['new_info']) == 0) {
      $arr_errors['new_info'] = __('Release info should be written.');
    }
    // Sürüm Numarası
    // Sadece son sürüm üzerinde çalışılıyorsa kontrol et.
    if ($dbl_pardil_rev == $dbl_pardil_lastrev) {
      if (strlen($_POST['new_releaseno']) == 0) {
        $arr_errors['new_releaseno'] = __('Release number should be written.');
      }
      elseif (strval(floatval($_POST['new_releaseno'])) != $_POST['new_releaseno']) {
        $arr_errors['new_releaseno'] = __('Release number is not valid.');
      }
      // Yeni Sürüm
      if ($_POST['new_newrelease'] == 'yes' && floatval($_POST['new_releaseno']) == floatval($_GET['rev'])) {
        $arr_errors['new_releaseno'] = sprintf(__('New release number should be greater than %.2f'), $_GET['rev']);
      }
      elseif ($_POST['new_newrelease'] == 'yes' && floatval($_POST['new_releaseno']) <= $dbl_pardil_lastrev) {
        $arr_errors['new_releaseno'] = sprintf(__('New release number should be greater than latest revision number (%.2f).'), $dbl_pardil_lastrev);
      }
    }
  }

  if (count($arr_errors) == 0 && isset($_POST['edit_proposal'])) {
    // Öneri ekleme işlemleri...

    $str_content = '';
    foreach ($_POST['new_content_title'] as $int_num => $str_title) {
      $str_body = $_POST['new_content_body'][$int_num];
      $str_content .= sprintf('<section><title>%s</title><body>%s</body></section>', $str_title, $str_body);
    }

    if ($_POST['new_newrelease'] == 'yes' && $dbl_pardil_rev == $dbl_pardil_lastrev) {
      // Yeni sürüm

      // Başlık ve özeti güncelle
      $arr_update = array(
                          'title' => $_POST['new_title'],
                          'abstract' => $_POST['new_abstract']
                          );
      proc_main_update($int_pardil_id, $arr_update);
      // Sürümü ekle
      proc_revision_new($int_pardil_id, $_PSESSION['id'], $_POST['new_releaseno'], $str_content, $_POST['new_info'], '');
      
      header('Location: editproposal_ok.php?proposal=' . $int_pardil_id . '&revision=' . $_POST['new_releaseno'] . '&newrevision=1');
      exit;
    }
    else {
      // Düzeltme
      // Başlık ve özeti güncelle
      $arr_update = array(
                          'title' => $_POST['new_title'],
                          'abstract' => $_POST['new_abstract']
                          );
      proc_main_update($int_pardil_id, $arr_update);

      // Sürümü güncelle
      $int_revision_id = query_proposal_revisionid($int_pardil_id, $dbl_pardil_rev);
      $arr_update = array(
                          'content' => $str_content,
                          'info' => $_POST['new_info']
                          );
      proc_revision_update($int_revision_id, $arr_update);

      header('Location: editproposal_ok.php?proposal=' . $int_pardil_id . '&revision=' . $dbl_pardil_rev);
      exit;
    }

  }
  elseif (count($arr_errors) > 0 && isset($_POST['edit_proposal'])) {
    // Formu göster...
    $_PCONF['title'] = getop('site_name') . ' - ' . __('Edit Proposal');
    $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.editproposal.php');
    $obj_page->setvar('int_pardil_id', $int_pardil_id);
    $obj_page->setvar('dbl_pardil_rev', $dbl_pardil_rev);
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->setvar('bln_first', false);
    $obj_page->flush();
  }
  else {
    // Sayfa ilk defa açılıyorsa...

    // Öneri bilgilerini topla...
    $arr_pardil_fetch = query_proposal_data($int_pardil_id, $dbl_pardil_rev);

    // Öneri İçeriği ve İçindekiler Listesi:
    $arr_pardil_fetch['content'] = '<?xml version="1.0" encoding="utf-8"?><pardil>' . $arr_pardil_fetch['content'] . '</pardil>';
    $res_xml = simplexml_load_string($arr_pardil_fetch['content']);
    $int_pardil_content = 1;
    $arr_pardil_content = array();
    foreach ($res_xml->children() as $res_node) {
      $str_title = $res_node->title;
      $str_body = substr($res_node->body->asXML(), 6, strlen($res_node->body->asXML()) - 13);
      $arr_pardil_content[] = array('no' => $int_pardil_content, 'title' => trim($str_title), 'body' => $str_body);
      $int_pardil_content++;
    }
    
    // Formu göster...

    $_PCONF['title'] = getop('site_name') . ' - ' . __('Edit Proposal');
    $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.editproposal.php');
    $obj_page->setvar('int_pardil_id', $int_pardil_id);
    $obj_page->setvar('dbl_pardil_rev', $dbl_pardil_rev);
    $obj_page->setvar('dbl_pardil_lastrev', $dbl_pardil_lastrev);
    $obj_page->setvar('arr_pardil_fetch', $arr_pardil_fetch);
    $obj_page->setvar('arr_pardil_content', $arr_pardil_content);
    $obj_page->setvar('bln_first', true);
    $obj_page->flush();
  }
?>
