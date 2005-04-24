<?php
  require('cfg/sys.define.php');
  require('sys/sys.gettext.php');
  require('sys/sys.database.php');
  require('sys/sys.procedures.php');
  require('sys/sys.pconf.php');
  require('sys/sys.session.php');

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
  $str_sql = sprintf('SELECT pardil_revisions.version FROM pardil_main INNER JOIN pardil_revisions ON pardil_main.id=pardil_revisions.proposal WHERE pardil_main.id=%d ORDER BY pardil_revisions.id DESC', $int_pardil_id);
  $res_sql = mysql_query($str_sql);
  $arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC);
  $dbl_pardil_lastrev = $arr_fetch['version'];

  // Revizyon:
  $dbl_pardil_rev = (isset($_GET['rev'])) ? $_GET['rev'] : $dbl_pardil_lastrev;

  // Erişim seviyesi
  $int_level = getop('level_proposal_edit');

  // Bakıcı mı değil mi?
  $int_count = database_query_scalar(sprintf('SELECT Count(*) FROM pardil_maintainers WHERE TimestampB<=Now() AND Now() <=TimestampE AND user=%d AND proposal=%d', $_PSESSION['id'], $_GET['id']));

  // Seviyesi yeterli değilse veya bakıcı değilse izin verme
  if ($int_level > $_PSESSION['level'] && $int_count == 0) {
    header('Location: denied.php');
    exit;
  }

  require('class/class.template.php');

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

  if (count($arr_errors) == 0 && isset($_POST['edit_proposal'])) {
    // Öneri ekleme işlemleri...

    $str_content = '';
    foreach ($_POST['new_content_title'] as $int_num => $str_title) {
      $str_body = $_POST['new_content_body'][$int_num];
      $str_content .= sprintf('<section><title>%s</title><body>%s</body></section>', $str_title, $str_body);
    }
    $str_notes = '';
    $arr_notes = explode("\n", str_replace("\r", '', $_POST['new_notes']));
    foreach ($arr_notes as $str_note) {
      $str_notes .= sprintf('<note>%s</note>', $str_note);
    }

    if ($_POST['new_newrelease']) {
      // Yeni sürüm

      // Başlık ve özeti güncelle
      $arr_update = array(
                          'title' => $_POST['new_title'],
                          'abstract' => $_POST['new_abstract']
                          );
      proc_main_update($int_pardil_id, $arr_update);
      // Sürümü ekle
      proc_revision_new($int_pardil_id, $_PSESSION['id'], $_POST['new_releaseno'], $str_content, $str_notes, $_POST['new_info'], '');
      
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
      $int_revision_id = database_query_scalar(sprintf('SELECT id FROM pardil_revisions WHERE proposal=%d and version=%f', $int_pardil_id, $dbl_pardil_rev));
      $arr_update = array(
                          'content' => $str_content,
                          'notes' => $str_notes,
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
    $obj_page = new template('tpl/tpl.editproposal.php');
    $obj_page->setvar('int_pardil_id', $int_pardil_id);
    $obj_page->setvar('dbl_pardil_rev', $dbl_pardil_rev);
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->setvar('bln_first', false);
    $obj_page->flush();
  }
  else {
    // Sayfa ilk defa açılıyorsa...
    // Öneri bilgilerini topla...
    $str_time = date('Y-m-d H:i:s');
    $str_sql = sprintf('SELECT pardil_main.id, pardil_main.title, pardil_main.abstract, pardil_revisions.content, pardil_revisions.notes, pardil_revisions.version, pardil_revisions.timestamp, pardil_revisions.info FROM pardil_main INNER JOIN pardil_revisions ON pardil_main.id=pardil_revisions.proposal WHERE pardil_main.id=%d AND pardil_revisions.version=%f', $int_pardil_id, $dbl_pardil_rev);
    $res_sql = mysql_query($str_sql);
    $arr_pardil_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC);

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
    
    // Öneri Notları
    $arr_pardil_fetch['notes'] = '<?xml version="1.0" encoding="utf-8"?><notes>' . $arr_pardil_fetch['notes'] . '</notes>';
    $res_xml = simplexml_load_string($arr_pardil_fetch['notes']);
    $int_pardil_notes = 1;
    $str_pardil_notes = '';
    foreach ($res_xml->children() as $res_node) {
      $str_body = substr($res_node->asXML(), 6, strlen($res_node->asXML()) - 13);
      $arr_pardil_notes[] = trim($str_body);
      $int_pardil_notes++;
    }
    $str_pardil_notes = join("\n", $arr_pardil_notes);

    // Formu göster...
    $_PCONF['title'] = getop('site_name') . ' - ' . __('Edit Proposal');
    $obj_page = new template('tpl/tpl.editproposal.php');
    $obj_page->setvar('int_pardil_id', $int_pardil_id);
    $obj_page->setvar('dbl_pardil_rev', $dbl_pardil_rev);
    $obj_page->setvar('arr_pardil_fetch', $arr_pardil_fetch);
    $obj_page->setvar('arr_pardil_content', $arr_pardil_content);
    $obj_page->setvar('str_pardil_notes', $str_pardil_notes);
    $obj_page->setvar('bln_first', true);
    $obj_page->flush();
  }
?>
