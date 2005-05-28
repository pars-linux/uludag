<?php
  include(dirname(__FILE__) . '/tpl.header.php');
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

        if (title.length == 0) {
          return;
        }
        
        var count = parseInt(document.getElementById('new_content_count').value);
        
        count++;
        document.getElementById('new_content_count').value = count;

        var el_newsection = document.createElement('DIV');
        var el_sections = document.getElementById('sections');
        el_sections.appendChild(el_newsection);

        el_newsection.id = 'section_' + count;
        el_newsection.innerHTML = ' \
                    <label for=""> \
                      <?php printf(__('Section:')); ?> ' + xhr_htmlspecialchars(title) + ' \
                      <a href="javascript:remove_section(\'section_' + count + '\')" title="<?php __e('Remove section'); ?>">[x]</a> \
                    </label> \
                    <br/> \
                    <input type="hidden" name="new_content_title[' + count + ']" value="' + title + '" /> \
                    <textarea name="new_content_body[' + count + ']" cols="25" rows="7" style="width: 400px; height: 200px;"></textarea> \
                    <br/>';

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
      <div id="content">
        <form action="<?php echo $_PCONF['site_url']; ?>newproposal.php" method="post">
          <fieldset>
            <label for=""><?php echo __('Title:'); ?></label>
            <br/>
            <input type="text" name="new_title" size="25" style="width: 400px;" value="<?php echo (!isset($arr_errors['new_title'])) ? htmlspecialchars($_POST['new_title'], ENT_QUOTES) : ''; ?>"/>
            <br/>
            <?php print_error('<div class="error">%s</div>', 'new_title'); ?>
            <br/>
            <label for=""><?php echo __('Abstract:'); ?></label>
            <br/>
            <textarea name="new_abstract" cols="25" rows="7" style="width: 400px; height: 200px;"><?php echo (!isset($arr_errors['new_abstract'])) ? htmlspecialchars($_POST['new_abstract'], ENT_QUOTES) : ''; ?></textarea>
            <br/>
            <?php print_error('<div class="error">%s</div>', 'new_abstract'); ?>
            <br/>
            <label for=""><?php echo __('New Section:'); ?></label>
            <br/>
            <input type="hidden" id="new_content_count" name="new_content_count" value="<?php printf('%d', (isset($_POST['new_content_count']) ? $_POST['new_content_count'] : 0)); ?>"/>
            <input type="text" id="new_content_new_title" size="25" style="width: 340px;" onkeypress="if (event.which == 13 || event.keyCode == 13) { new_section(); }"/>
            <button type="button" onclick="new_section();"><?php echo __('Add &raquo;'); ?></button>
            <div class="info">
              <?php echo __('Proposal should be written in sections.<br/>Write section title and then push "Add &raquo;" button.'); ?>
            </div>
            <?php print_error('<div class="error">%s</div>', 'new_content_new_title'); ?>
            <br/>
            <div id="sections">
              <?php
                if (isset($_POST['new_content_title'])) {
                  $arr_keys = array_keys($_POST['new_content_title']);
                  foreach ($arr_keys as $int_num) {
                    $str_title = $_POST['new_content_title'][$int_num];
                    $str_body = $_POST['new_content_body'][$int_num];
                ?>
                  <div id="section_<?php echo $int_num; ?>">
                    <label for="">
                      <?php echo __('Section:') . ' ' . htmlspecialchars($str_title); ?>
                      <a href="javascript:remove_section('section_<?php echo $int_num; ?>')" title="<?php __e('Remove section'); ?>">[x]</a>
                    </label>
                    <br/>
                    <input type="hidden" name="new_content_title[<?php echo $int_num; ?>]" value="<?php echo htmlspecialchars($str_title); ?>" />
                    <textarea name="new_content_body[<?php echo $int_num; ?>]" cols="25" rows="7" style="width: 400px; height: 200px;"><?php echo htmlspecialchars($str_body); ?></textarea>
                    <br/>
                    <?php print_error('<div class="error">%s</div>', 'new_content_title', $int_num); ?>
                  </div>
              <?php      
                  }
                }
              ?>
            </div>
            <br/>
            <label for=""><?php echo __('Release Info:'); ?></label>
            <br/>
            <input type="text" name="new_info" size="25" style="width: 400px;" value="<?php echo (!isset($arr_errors['new_info'])) ? htmlspecialchars($_POST['new_info'], ENT_QUOTES) : ''; ?>"/>
            <br/>
            <?php print_error('<div class="error">%s</div>', 'new_info'); ?>
            <br/>
            <button type="reset" onclick="return confirm('<?php echo __('Are you sure?'); ?>');"><?php echo __('Reset Form'); ?></button>
            <button type="submit" name="new_proposal" value="1"><?php echo __('Submit &raquo;'); ?></button>
          </fieldset>
        </form>
      </div>
<?php
  include(dirname(__FILE__) . '/tpl.footer.php');
?>
