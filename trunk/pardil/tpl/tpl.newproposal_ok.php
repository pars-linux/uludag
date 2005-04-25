<?php
  include(dirname(__FILE__) . '/tpl.header.php');
?>
      <div id="content">
        <h2><?php echo __('New Proposal Submitted'); ?></h2>
        <p>
          <?php echo __('You\'ve successfully submitted a new proposal.'); ?>
        </p>
        <?php if ($bln_approved) { ?>
        <p>
          <?php echo __('New proposal is automatically approved and marked as active.'); ?>
        </p>
        <p>
          <b>&raquo;</b> <a href="<?php echo $_PCONF['site_url']; ?>proposal.php?id=<?php echo $int_proposal; ?>"><?php echo __('View proposal'); ?></a>
        </p>
        <?php } else { ?>
        <p>
          <?php echo __('New proposal marked as pending. It needs to be reviewed by a moderator.'); ?>
        </p>
        <p>
          <b>&raquo;</b> <a href="<?php echo $_PCONF['site_url']; ?>proposal.php?id=<?php echo $int_proposal; ?>"><?php echo __('View proposal'); ?></a>
        </p>
        <?php } ?>
      </div>
<?php
  include(dirname(__FILE__) . '/tpl.footer.php');
?>
