<?php
  require('sys.define.php');
  require('sys.database.php');
  require('sys.procedures.php');
  require('sys.gettext.php');
  
  require('class.template.php');
  
  // Denetimler
  $arr_errors = array();
  if (isset($_POST['new_proposal']) && !isset($_POST['new_content_title_add'])) {
    // Başlık
    if (strlen($_POST['new_title']) == 0) {
      $arr_errors['new_title'] = _('Title should be written.');
    }
    // Özet
    if (strlen($_POST['new_abstract']) == 0) {
      $arr_errors['new_abstract'] = _('Abstract should be written.');
    }
    // Bölümler
    if (isset($_POST['new_content'])) {
      foreach ($_POST['new_content'] as $str_title => $str_body) {
        if (strlen($str_body) == 0) {
          $str_title2 = substr($str_title, strpos($str_title, '_') + 1, strlen($str_title) - strpos($str_title, '_') + 1);
          $arr_errors['new_content'][$str_title] = sprintf(_('Section %s should be written. If you don\'t want it, remove it.'), urldecode($str_title2));
        }
      }
    }
    else {
      $arr_errors['new_content_title'] = _('At least one section should be created.');
    }
    // Sürüm Notları
    if (strlen($_POST['new_info']) == 0) {
      $arr_errors['new_info'] = _('Release info should be written.');
    }
  }

  if (count($arr_errors) == 0 && isset($_POST['new_proposal']) && !isset($_POST['new_content_title_add'])) {
    // Öneri ekleme işlemleri...
    echo 'Öneri ekle...';
  }
  else {
    // Formu göster...
    $obj_page = new template('tpl.newproposal.php');
    $obj_page->setvar('arr_errors', $arr_errors);
    $obj_page->flush();
  }

?>
