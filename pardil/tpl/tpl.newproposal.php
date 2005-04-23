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
      function xhr_htmlspecialchars(s) {
        s = s.replace(/&/g, '&amp;')
        s = s.replace(/</g, '&lt;')
        s = s.replace(/>/g, '&gt;')
        s = s.replace(/"/g, '&quot;')
        return s;
      }
    
      function new_section() {
        var title = document.getElementById('new_content_new_title').value;
        var count = parseInt(document.getElementById('new_content_count').value);
        
        count++;
        document.getElementById('new_content_count').value = count;

        var el_sections = document.getElementById('sections');
        el_sections.innerHTML += ' \
                  <table width="100%" class="form" id="section_' + count + '"> \
                    <tr> \
                      <td class="label"> \
                        <?php printf(__('Section:')); ?> ' + xhr_htmlspecialchars(title) + ' \
                        <a href="javascript:remove_section(\'section_' + count + '\')" title="<?php __e('Remove section'); ?>">[x]</a> \
                      </td> \
                      <td> \
                        <input type="hidden" name="new_content_title[' + count + ']" value="' + title + '" /> \
                        <textarea name="new_content_body[' + count + ']" cols="25" rows="7" style="width: 400px; height: 200px;"></textarea> \
                      </td> \
                    </tr> \
                  </table>';
                  
        document.getElementById('new_content_new_title').value = '';
      }
      function remove_section(id) {
        if (confirm('<?php __e('Remove section?'); ?>')) {
          var el_sections = document.getElementById('sections');
          var el_table = document.getElementById(id);
          el_sections.removeChild(el_table);
        }
      }
    </script>
      <div id="menubar">
        <span class="arrowL">&#171;</span>
        <span class="arrowR">&#187;</span>
        <span class="title"><?php echo __('New Proposal'); ?></span>
      </div>
      <div id="content">
        <div class="proposal">
          <p>&nbsp;</p>
          <form action="newproposal.php" method="post">
            <fieldset>
              <input type="hidden" name="new_proposal" value="1"/>
              <table class="form">
                <tr>
                  <td class="label"><?php echo __('Title:'); ?></td>
                  <td>
                    <input type="text" name="new_title" size="25" style="width: 400px;" value="<?php echo (!isset($arr_errors['new_title'])) ? htmlspecialchars($_POST['new_title'], ENT_QUOTES) : ''; ?>"/>
                  </td>
                </tr>
                <?php print_error('new_title'); ?>
                <tr>
                  <td class="label"><?php echo __('Abstract:'); ?></td>
                  <td>
                    <textarea name="new_abstract" cols="25" rows="7" style="width: 400px; height: 200px;"><?php echo (!isset($arr_errors['new_abstract'])) ? htmlspecialchars($_POST['new_abstract'], ENT_QUOTES) : ''; ?></textarea>
                  </td>
                </tr>
                <?php print_error('new_abstract'); ?>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td class="label"><?php echo __('New Section:'); ?></td>
                  <td>
                    <input type="hidden" id="new_content_count" name="new_content_count" value="<?php printf('%d', (isset($_POST['new_content_count']) ? $_POST['new_content_count'] : 0)); ?>"/>
                    <input type="text" id="new_content_new_title" size="25" style="width: 340px;" onkeypress="if (event.which == 13 || event.keyCode == 13) { new_section(); }"/>
                    <button type="button" onclick="new_section();"><?php echo __('Add &raquo;'); ?></button>
                  </td>
                </tr>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td class="info"><?php echo __('Proposal should be written in sections.<br/>Write section title and then push "Add &raquo;" button.'); ?></td>
                </tr>
                <?php print_error('new_content_new_title'); ?>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td style="padding: 0px;" colspan="2">
                  <div id="sections">
                <?php
                  if (isset($_POST['new_content_title'])) {
                    $arr_keys = array_keys($_POST['new_content_title']);
                    foreach ($arr_keys as $int_num) {
                      $str_title = $_POST['new_content_title'][$int_num];
                      $str_body = $_POST['new_content_body'][$int_num];
                ?>
                  <table width="100%" class="form" id="section_<?php echo $int_num; ?>">
                    <tr>
                      <td class="label">
                        <?php
                          echo __('Section:') . ' ' . htmlspecialchars($str_title);
                        ?>
                        <a href="javascript:remove_section('section_<?php echo $int_num; ?>')" title="<?php __e('Remove section'); ?>">[x]</a>
                      </td>
                      <td>
                        <input type="hidden" name="new_content_title[<?php echo $int_num; ?>]" value="<?php echo htmlspecialchars($str_title); ?>" />
                        <textarea name="new_content_body[<?php echo $int_num; ?>]" cols="25" rows="7" style="width: 400px; height: 200px;"><?php echo htmlspecialchars($str_body); ?></textarea>
                      </td>
                    </tr>
                    <?php
                      print_error('new_content_title', $int_num);
                    ?>
                  </table>
                <?php      
                    }
                  }
                ?>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td class="label">&nbsp;</td>
                  <td>&nbsp;</td>
                </tr>
                <tr>
                  <td class="label"><?php echo __('Notes:');  ?></td>
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
                  <td class="label"><?php echo __('Release Info:'); ?></td>
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
                    <button type="reset" onclick="return confirm('<?php echo __('Are you sure?'); ?>');"><?php echo __('Reset Form'); ?></button>
                    <button type="submit"><b><?php echo __('Submit &raquo;'); ?></b></button>
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
