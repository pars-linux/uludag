<?php
  require('sys.define.php');
  require('sys.database.php');
  require('sys.procedures.php');

  // Denetimler
  $arr_errors = array();
  if (isset($_POST['pardil_new']) && !isset($_POST['pardil_new_content_title_add'])) {
    // Başlık
    if (strlen($_POST['pardil_new_title']) == 0) {
      $arr_errors['pardil_new_title'] = 'Başlık boş bırakılamaz.';
    }
    // Özet
    if (strlen($_POST['pardil_new_abstract']) == 0) {
      $arr_errors['pardil_new_abstract'] = 'Özet boş bırakılamaz.';
    }
    // Bölümler
    foreach ($_POST['pardil_new_content'] as $str_title => $str_body) {
      if (strlen($str_body) == 0) {
        $arr_errors['pardil_new_content'][$str_title] = 'Bölüm boş bırakılamaz, bölümü kullanmak istemiyorsanız kaldırın.';
      }
    }
    // Notlar
    if (strlen($_POST['pardil_new_notes']) == 0) {
      $arr_errors['pardil_new_notes'] = 'Notlar boş bırakılamaz.';
    }
    // Sürüm Notları
    if (strlen($_POST['pardil_new_tip']) == 0) {
      $arr_errors['pardil_new_tip'] = 'Sürüm notu boş bırakılamaz.';
    }
  }

  function print_error($str_name, $str_sub='') {
    global $arr_errors;
    if ($str_sub == '') {
      if (isset($arr_errors[$str_name])) {
        printf('<tr><td class="label">&nbsp;</td><td class="error">%s</td></tr>', $arr_errors[$str_name]);
      }
    }
    else {
      if (isset($arr_errors[$str_name][$str_sub])) {
        printf('<tr><td class="label">&nbsp;</td><td class="error">%s</td></tr>', $arr_errors[$str_name][$str_sub]);
      }
    }
  }

?>
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="tr">
  <head>
    <title>Yeni Öneri</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" href="style.css" type="text/css" />
  </head>
  <body>
    <div id="container">
      <div id="header">
        <img src="images/logo2.png" alt="pardilS"/>
      </div>
      <div id="menubar">
        <span class="arrowL">&#171;</span>
        <span class="arrowR">&#187;</span>
        <span class="title">Yeni pardil</span>
      </div>
      <div id="content">
        <div class="proposal">
          <h1>ÜGÖ Ekle</h1>
          <p>&nbsp;</p>
          <form action="new.php" method="post">
            <input type="hidden" name="pardil_new" value="1"/>
            <table class="form">
              <tr>
                <td class="label">Başlık</td>
                <td>
                  <input type="text" name="pardil_new_title" size="25" style="width: 400px;" value="<?php if (!isset($arr_errors['pardil_new_title'])) printf('%s', $_POST['pardil_new_title']); ?>"/>
                </td>
              </tr>
              <?php print_error('pardil_new_title'); ?>
              <tr>
                <td class="label">Özet</td>
                <td>
                  <textarea name="pardil_new_abstract" cols="25" rows="7" style="width: 400px; height: 200px;"><?php if (!isset($arr_errors['pardil_new_abstract'])) printf('%s', htmlspecialchars($_POST['pardil_new_abstract'])); ?></textarea>
                </td>
              </tr>
              <?php print_error('pardil_new_abstract'); ?>
              <tr>
                <td class="label">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td class="label">Yeni Bölüm</td>
                <td>
                  <input type="hidden" id="pardil_new_content_i" name="pardil_new_content_i" value="<?php printf('%d', (isset($_POST['pardil_new_content_i']) ? $_POST['pardil_new_content_i'] : 0)); ?>"/>
                  <input type="text" id="pardil_new_content_title" size="25" style="width: 340px;" onkeypress="if (event.which == 13 || event.keyCode == 13) { document.getElementById('pardil_new_content_title_add').click(); }"/>
                  <button id="pardil_new_content_title_add" type="submit" name="pardil_new_content_title_add" value="true" onclick="if (document.getElementById('pardil_new_content_title').value != '') { document.getElementById('pardil_new_content_i').value = parseInt(document.getElementById('pardil_new_content_i').value) + 1; document.getElementById('pardil_new_content_title').name = 'pardil_new_content[' + document.getElementById('pardil_new_content_i').value + '_' + document.getElementById('pardil_new_content_title').value + ']'; document.getElementById('pardil_new_content_title').value = '' ; }">Ekle &raquo;</button>
                </td>
              </tr>
              <tr>
                <td class="label">&nbsp;</td>
                <td class="info">Öneri metni bölümler halinde yazılmalıdır.<br/>Bölüm başlığını yazdıktan sonra "Ekle &raquo;" düğmesine basın.</td>
              </tr>
              <?php print_error('pardil_new_content_title'); ?>
              <tr>
                <td class="label">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <?php
                if (isset($_POST['pardil_new_content'])) {
                  $arr_keys = array_keys($_POST['pardil_new_content']);
                  natsort($arr_keys);
                  foreach ($arr_keys as $str_title) {
                    $str_body = $_POST['pardil_new_content'][$str_title];
              ?>
                <tr>
                  <td class="label">
                    <?php
                      $str_title2 = substr($str_title, strpos($str_title, '_') + 1, strlen($str_title) - strpos($str_title, '_') + 1);
                      printf('Bölüm: %s', $str_title2);
                    ?>
                    <a href="javascript:if (confirm('Bölüm kaldırılacak.\nEmin misiniz?')) { var el = document.getElementById('pardil_new_content[<?php printf('%s', addslashes($str_title)); ?>]'); el.name = ''; el.value = ''; document.getElementById('pardil_new_content_title_add').value = ''; document.getElementById('pardil_new_content_title').value = ''; document.getElementById('pardil_new_content_title_add').click(); }" title="Bölümü Kaldır">[x]</a>
                  </td>
                  <td>
                    <textarea id="pardil_new_content[<?php printf('%s', addslashes($str_title)); ?>]" name="pardil_new_content[<?php printf('%s', addslashes($str_title)); ?>]" cols="25" rows="7" style="width: 400px; height: 200px;"><?php printf('%s', htmlspecialchars($str_body)); ?></textarea>
                  </td>
                </tr>
              <?php      
                    print_error('pardil_new_content', $str_title);
                  }
                }
              ?>
              <tr>
                <td class="label">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td class="label">Notlar</td>
                <td>
                  <textarea name="pardil_new_notes" cols="25" rows="7" style="width: 400px; height: 120px;"><?php if (!isset($arr_errors['pardil_new_notes'])) printf('%s', htmlspecialchars($_POST['pardil_new_notes'])); ?></textarea>
                </td>
              </tr>
              <?php print_error('pardil_new_notes'); ?>
              <tr>
                <td class="label">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td class="label">Sürüm Notu</td>
                <td>
                  <input type="text" name="pardil_new_tip" size="25" style="width: 400px;" value="<?php if (!isset($arr_errors['pardil_new_tip'])) printf('%s', $_POST['pardil_new_tip']); ?>"/>
                </td>
              </tr>
              <?php print_error('pardil_new_tip'); ?>
              <tr>
                <td class="label">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td class="label">&nbsp;</td>
                <td class="info">
                  <button type="reset" onclick="return confirm('Emin misiniz?');">Temizle</button>
                  <button type="submit"><b>Gönder &raquo;</b></button>
                </td>
              </tr>
            </table>
          </form>
        </div>
      </div>
      <div id="footer">
        &nbsp;
      </div>
    </div>
  </body>
</html>
