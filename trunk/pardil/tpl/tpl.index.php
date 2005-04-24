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
