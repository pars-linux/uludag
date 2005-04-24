<?php
  include('tpl.header.php');
?>
      <div id="content">
        <p>
          <b>&raquo;</b> <a href="login.php"><?php echo __('User Login'); ?></a>
          <br/>
          <b>&raquo;</b> <a href="newproposal.php"><?php echo __('New Proposal'); ?></a>
          <br/>
          <!--
          <b>&raquo;</b> <a href="proposal.php"><?php echo __('Proposals'); ?></a>
          -->
        </p>
        <p>
          <b><?php echo __('Proposals:'); ?></b>
        </p>
        <ul>
          <?php
            foreach ($arr_list as $arr_item) {
              printf('<li><a href="proposal.php?id=%d">%s</a></li>', $arr_item['id'], $arr_item['title']);
            }
          ?>
        </ul>
        <p>
          <b><?php echo __('Session Information:'); ?></b>
        </p>
        <?php
          echo '<pre>';
          print_r($_PSESSION);
          echo '</pre>';
        ?>
      </div>
<?php
  include('tpl.footer.php');
?>
