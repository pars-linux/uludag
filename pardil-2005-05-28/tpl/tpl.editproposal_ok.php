<?php
  include('tpl.header.php');
?>
      <div id="content">
        <h2><?php echo __('Proposal Updated'); ?></h2>
        <p>
          <?php echo __('You\'ve successfully updated a proposal.'); ?>
        </p>
        <?php if ($bln_newrevision) { ?>
        <p>
          <?php echo __('This updated is saved as a new revision of proposal.'); ?>
        </p>
        <?php } ?>
        <p>
          <b>&raquo;</b> <a href="proposal.php?id=<?php echo $int_proposal; ?>&amp;rev=<?php echo $dbl_revision; ?>"><?php echo __('View proposal'); ?></a>
        </p>
      </div>
<?php
  include('tpl.footer.php');
?>
