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

  include('tpl.header.php');
?>
    <script type="text/javascript">
      /*
        JS'nin escape() fonksiyonu UTF-8 formatındaki harfleri de kodluyor,
        ki bu hiç hoşuma gitmiyor...
      */
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
          return true;
        }
        else {
          return false;
        }
      }
      function delete_section(id, msg) {
        if (confirm(msg)) {
          var el = document.getElementById(id);
          el.name = '';
          el.value = '';
          document.getElementById('new_content_title_add').value = '';
          document.getElementById('new_content_title').value = '';
          document.getElementById('new_content_title_add').click();
        }
      }
    </script>
      <div id="menubar">
        <span class="arrowL">&#171;</span>
        <span class="arrowR">&#187;</span>
        <span class="title"><?php echo _('New Proposal'); ?></span>
      </div>
      <div id="content">
        <div class="proposal">
          <form action="newproposal.php" method="post">
            <fieldset>
              <input type="hidden" name="new_proposal" value="1"/>
              <table class="form">
                <tr>
                  <td class="label"><?php echo _('Title:'); ?></td>
                  <td>
                    <input type="text" name="new_title" size="25" style="width: 400px;" value="<?php echo (!isset($arr_errors['new_title'])) ? htmlspecialchars($_POST['new_title'], ENT_QUOTES) : ''; ?>"/>
                  </td>
                </tr>
                <?php print_error('new_title'); ?>
                <tr>
                  <td class="label"><?php echo _('Abstract:'); ?></td>
                  <td>
                    <textarea name="new_abstract" cols="25" rows="7" style="width: 400px; height: 200px;"><?php echo (!isset($arr_errors['new_abstract'])) ? htmlspecialchars($_POST['new_abstract'], ENT_QUOTES) : ''; ?></textarea>
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
                    <button id="new_content_title_add" type="submit" name="new_content_title_add" value="true" onclick="return new_section();"><?php echo _('Add &raquo;'); ?></button>
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
                        $str_title1 = substr($str_title, 0, strpos($str_title, '_'));
                        $str_title2 = substr($str_title, strpos($str_title, '_') + 1, strlen($str_title) - strpos($str_title, '_') - 1);
                        printf(_('Section: %s'), urldecode($str_title2));
                      ?>
                      <a href="javascript:delete_section('new_content_<?php echo $str_title1; ?>', '<?php printf(_('Section \\\'%s\\\' will be removed.\\nAre you sure?'), $str_title2); ?>');" title="<?php echo _('Remove Section'); ?>">[x]</a>
                    </td>
                    <td>
                      <textarea id="new_content_<?php echo $str_title1; ?>" name="new_content[<?php echo $str_title; ?>]" cols="25" rows="7" style="width: 400px; height: 200px;"><?php echo htmlspecialchars($str_body, ENT_QUOTES); ?></textarea>
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
                    <textarea name="new_notes" cols="25" rows="7" style="width: 400px; height: 120px;"><?php echo (!isset($arr_errors['new_notes'])) ? htmlspecialchars($_POST['new_notes'], ENT_QUOTES) : ''; ?></textarea>
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
                    <input type="text" name="new_info" size="25" style="width: 400px;" value="<?php echo (!isset($arr_errors['new_info'])) ? htmlspecialchars($_POST['new_info'], ENT_QUOTES) : ''; ?>"/>
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
            </fieldset>
          </form>
        </div>
      </div>
<?php
  include('tpl.footer.php');
?>
