<?php
  require(dirname(__FILE__) . '/sys.common.php');

  // Erişim seviyesi kontrolü
  $int_level = getop('level_proposal_new');
  if ($int_level > $_PSESSION['level']) {
    header('Location: denied.php');
    exit;
  }

  require(dirname(__FILE__) . '/class/class.template.php');

  // Denetimler
  $arr_errors = array();
  if (isset($_POST['new_proposal'])) {
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
  }

  if (count($arr_errors) == 0 && isset($_POST['new_proposal'])) {
    // Öneri ekleme işlemleri...

    $str_content = '';
    foreach ($_POST['new_content_title'] as $int_num => $str_title) {
      $str_body = $_POST['new_content_body'][$int_num];
      $str_content .= sprintf('<section><title>%s</title><body>%s</body></section>', $str_title, $str_body);
    }

    if ($_PSESSION['level'] >= getop('level_proposal_new_approved')) {
      $bln_approve = true;
    }
    else {
      $bln_approve = false;
    }
    $int_proposal = proc_main_new($_PSESSION['id'], $_POST['new_title'], $_POST['new_abstract'], $str_content, $_POST['new_info'], $bln_approve, '');

    if ($bln_approve) {
      // Onay yetkisi varsa, sorumlu olarak ata.
      proc_maintainers_new($int_proposal, $_PSESSION['id']);
    }

    header('Location: newproposal_ok.php?proposal=' . $int_proposal . '&approved=' . ($bln_approve ? 1 : 0));
    exit;
  }
  else {
    // Formu göster...
    $_PCONF['title'] = getop('site_name') . ' - ' . __('New Proposal');
    $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.newproposal.php');
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->flush();
  }

?>
