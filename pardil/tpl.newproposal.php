<?php
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
    <title><?php echo _('New Proposal'); ?></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" href="style.css" type="text/css" />
    <script type="text/javascript">
      function p_escape(str_in) {
        var str_out = '';
        for (var i = 0; i < str_in.length; i++) {
          if ((33 <= str_in.charCodeAt(i) && str_in.charCodeAt(i) <= 47) || (58 <= str_in.charCodeAt(i) && str_in.charCodeAt(i) <= 64) || (91 <= str_in.charCodeAt(i) && str_in.charCodeAt(i) <= 96) || (123 <= str_in.charCodeAt(i) && str_in.charCodeAt(i) <= 127)) {
            str_out += escape(str_in.charAt(i));
          }
          else {
            str_out += str_in.charAt(i);
          }
        }
        return str_out;
      }
      function new_section() {
        if (document.getElementById('new_content_title').value != '') {
          document.getElementById('new_content_i').value = parseInt(document.getElementById('new_content_i').value) + 1;
          document.getElementById('new_content_title').name = 'new_content[' + p_escape(document.getElementById('new_content_i').value + '_' + document.getElementById('new_content_title').value) + ']';
          document.getElementById('new_content_title').value = '';
        }
      }
    </script>
  </head>
  <body>
    <div id="container">
      <div id="header">
        <img src="images/logo2.png" alt="Pardil"/>
      </div>
      <div id="menubar">
        <span class="arrowL">&#171;</span>
        <span class="arrowR">&#187;</span>
        <span class="title"><?php echo _('New Proposal'); ?></span>
      </div>
      <div id="content">
        <div class="proposal">
          <form action="newproposal.php" method="post">
            <input type="hidden" name="new_proposal" value="1"/>
            <table class="form">
              <tr>
                <td class="label"><?php echo _('Title:'); ?></td>
                <td>
                  <input type="text" name="new_title" size="25" style="width: 400px;" value="<?php echo (!isset($arr_errors['new_title'])) ? $_POST['new_title'] : ''; ?>"/>
                </td>
              </tr>
              <?php print_error('new_title'); ?>
              <tr>
                <td class="label"><?php echo _('Abstract:'); ?></td>
                <td>
                  <textarea name="new_abstract" cols="25" rows="7" style="width: 400px; height: 200px;"></textarea>
                </td>
              </tr>
              <?php print_error('new_abstract'); ?>
              <tr>
                <td class="label">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <?php
              /*
                JS destekli dinamik bölüm oluşturma ile ilgili not:
                ===================================================

                Eğer, bölüm adresi ilgili alana yazıldıktan sonra, "Ekle >>" (ya da "Add >>") düğmesine basılırsa, 
                "new_content[başlık]" adında bir form elemanı yaratılır ve form gönderimi yapılır. Form gönderiminin 
                ardından sayfa yeniden yüklendiğinde, "new_content" dizisinin her elemanı için bir textarea oluşturulur. 
              */
              ?>
              <tr>
                <td class="label"><?php echo _('New Section:'); ?></td>
                <td>
                  <input type="hidden" id="new_content_i" name="new_content_i" value="<?php printf('%d', (isset($_POST['new_content_i']) ? $_POST['new_content_i'] : 0)); ?>"/>
                  <input type="text" id="new_content_title" size="25" style="width: 340px;" onkeypress="if (event.which == 13 || event.keyCode == 13) { document.getElementById('new_content_title_add').click(); }"/>
                  <button id="new_content_title_add" type="submit" name="new_content_title_add" value="true" onclick="new_section();"><?php echo _('Add &raquo;'); ?></button>
                </td>
              </tr>
              <tr>
                <td class="label">&nbsp;</td>
                <td class="info"><?php echo _('Proposal should be written in sections.<br/>Write section title and then push "Add &raquo;" button.'); ?></td>
              </tr>
              <?php print_error('new_content_title'); ?>
              <tr>
                <td class="label">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <?php
                if (isset($_POST['new_content'])) {
                  $arr_keys = array_keys($_POST['new_content']);
                  natsort($arr_keys);
                  foreach ($arr_keys as $str_title) {
                    $str_body = $_POST['new_content'][$str_title];
              ?>
                <tr>
                  <td class="label">
                    <?php
                      $str_title2 = substr($str_title, strpos($str_title, '_') + 1, strlen($str_title) - strpos($str_title, '_') - 1);
                      printf(_('Section: %s'), urldecode($str_title2));
                    ?>
                    <a href="javascript:if (confirm('<?php printf(_('Section \\\'%s\\\' will be removed.\\nAre you sure?'), $str_title2); ?>')) { var el = document.getElementById('new_content[<?php printf('%s', addslashes($str_title)); ?>]'); el.name = ''; el.value = ''; document.getElementById('new_content_title_add').value = ''; document.getElementById('new_content_title').value = ''; document.getElementById('new_content_title_add').click(); }" title="<?php echo _('Remove Section'); ?>">[x]</a>
                  </td>
                  <td>
                    <textarea id="new_content[<?php echo $str_title; ?>]" name="new_content[<?php echo $str_title; ?>]" cols="25" rows="7" style="width: 400px; height: 200px;"><?php printf('%s', htmlspecialchars($str_body)); ?></textarea>
                  </td>
                </tr>
              <?php      
                    print_error('new_content', $str_title);
                  }
                }
              ?>
              <tr>
                <td class="label">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td class="label"><?php echo _('Notes:');  ?></td>
                <td>
                  <textarea name="new_notes" cols="25" rows="7" style="width: 400px; height: 120px;"><?php if (!isset($arr_errors['new_notes'])) printf('%s', htmlspecialchars($_POST['new_notes'])); ?></textarea>
                </td>
              </tr>
              <?php print_error('new_notes'); ?>
              <tr>
                <td class="label">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td class="label"><?php echo _('Release Info:'); ?></td>
                <td>
                  <input type="text" name="new_info" size="25" style="width: 400px;" value="<?php if (!isset($arr_errors['new_info'])) printf('%s', $_POST['new_info']); ?>"/>
                </td>
              </tr>
              <?php print_error('new_info'); ?>
              <tr>
                <td class="label">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td class="label">&nbsp;</td>
                <td class="info">
                  <button type="reset" onclick="return confirm('<?php echo _('Are you sure?'); ?>');"><?php echo _('Reset Form'); ?></button>
                  <button type="submit"><b><?php echo _('Submit &raquo;'); ?></b></button>
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
