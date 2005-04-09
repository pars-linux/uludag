<?php
  require('sys.define.php');
  require('sys.gettext.php');
  require('sys.database.php');
  require('sys.procedures.php');
  require('sys.pconf.php');
  require('sys.session.php');

  // Erişim seviyesi kontrolü
  $int_level = getop('level_proposal_new');
  if ($int_level > $_PSESSION['level']) {
    header('Location: denied.php');
    exit;
  }

  require('class.template.php');

  // Denetimler
  $arr_errors = array();
  if (isset($_POST['new_proposal']) && !isset($_POST['new_content_title_add'])) {
    // Başlık
    if (strlen($_POST['new_title']) == 0) {
      $arr_errors['new_title'] = __('Title should be written.');
    }
    // Özet
    if (strlen($_POST['new_abstract']) == 0) {
      $arr_errors['new_abstract'] = __('Abstract should be written.');
    }
    // Bölümler
    if (isset($_POST['new_content'])) {
      foreach ($_POST['new_content'] as $str_title => $str_body) {
        if (strlen($str_body) == 0) {
          $str_title2 = substr($str_title, strpos($str_title, '_') + 1, strlen($str_title) - strpos($str_title, '_') + 1);
          $arr_errors['new_content'][$str_title] = sprintf(__('Section "%s" should be written. If you don\'t want it, remove it.'), htmlspecialchars(urldecode($str_title2)));
        }
      }
    }
    else {
      $arr_errors['new_content_title'] = __('At least one section should be created.');
    }
    // Sürüm Notları
    if (strlen($_POST['new_info']) == 0) {
      $arr_errors['new_info'] = __('Release info should be written.');
    }
  }

  if (count($arr_errors) == 0 && isset($_POST['new_proposal']) && !isset($_POST['new_content_title_add'])) {
    // Öneri ekleme işlemleri...

    $int_level = getop('level_proposal_new_approved');

    printf('<b>Başlık:</b> %s<br/>', htmlspecialchars($_POST['new_title']));
    printf('<b>Özet:</b> %s<br/>', htmlspecialchars($_POST['new_abstract']));
    $str_content = '';
    foreach ($_POST['new_content'] as $str_title => $str_body) {
      $str_title2 = substr($str_title, strpos($str_title, '_') + 1, strlen($str_title) - strpos($str_title, '_') - 1);
      $str_content .= sprintf('<section><title>%s</title><body>%s</body></section>', urldecode($str_title2), $str_body);
    }
    printf('<b>Bölümler:</b> %s<br/>', htmlspecialchars($str_content));
    $arr_notes = explode("\n", str_replace("\r", '', $_POST['new_notes']));
    $str_notes = '';
    foreach ($arr_notes as $str_note) {
      $str_notes .= sprintf('<note>%s</note>', $str_note);
    }
    printf('<b>Notlar:</b> %s<br/>', htmlspecialchars($str_notes));
    printf('<b>Sürüm Bilgisi:</b> %s<br/>', htmlspecialchars($_POST['new_info']));
    printf('<b>Öneri Durumu:</b> %s<br/>', (($int_level > $_PSESSION['level']) ? 'Onaylanması gerek' :'Otomatik onaylancak'));
  }
  else {
    // Formu göster...
    $_PCONF['title'] = getop('site_name') . ' - ' . __('New Proposal');
    $obj_page = new template('tpl.newproposal.php');
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->flush();
  }

?>
