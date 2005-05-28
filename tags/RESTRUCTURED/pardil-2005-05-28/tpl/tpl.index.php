<?php
  include(dirname(__FILE__) . '/tpl.header.php');
?>
      <div id="content">
        <p>
          <b>&raquo;</b> <a href="<?php echo $_PCONF['site_url']; ?>login.php"><?php echo __('User Login'); ?></a>
          <br/>
          <b>&raquo;</b> <a href="<?php echo $_PCONF['site_url']; ?>profile.php"><?php echo __('User Profile'); ?></a>
          <br/>
          <b>&raquo;</b> <a href="<?php echo $_PCONF['site_url']; ?>newproposal.php"><?php echo __('New Proposal'); ?></a>
          <br/>
          <!--
          <b>&raquo;</b> <a href="<?php echo $_PCONF['site_url']; ?>proposal.php"><?php echo __('Proposals'); ?></a>
          -->
        </p>
        <p>
          <b><?php echo __('Proposals:'); ?></b>
        </p>
        <ul>
          <?php
            foreach ($arr_list as $arr_item) {
              $str_edit = ($arr_item['edit']) ? sprintf('<a href="%seditproposal.php?id=%d">[Düzenle]</a>', $_PCONF['site_url'], $arr_item['id']) : '';
              printf('<li><a href="%sproposal.php?id=%d">%s</a> %s</li>', $_PCONF['site_url'], $arr_item['id'], $arr_item['title'], $str_edit);
            }
          ?>
        </ul>
      </div>
<?php
  include(dirname(__FILE__) . '/tpl.footer.php');
?>
