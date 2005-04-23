<?php
  include('tpl.header.php');
?>
      <div id="menubar">
        <span class="arrowL">&#171;</span>
        <span class="arrowR">&#187;</span>
        <span class="title"><?php echo $_PCONF['title']; ?></span>
      </div>
      <div id="menu">
        &nbsp;
      </div>
      <div id="content">
        <p>
          <b>&raquo;</b> <a href="login.php"><?php echo __('User Login'); ?></a>
          <br/>
          <b>&raquo;</b> <a href="newproposal.php"><?php echo __('New Proposal'); ?></a>
          <br/>
          <b>&raquo;</b> <a href="proposal.php"><?php echo __('Proposals'); ?></a>
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
