<?php
  include('tpl.header.php');
?>
      <div id="content">
        <form action="activation.php" method="post">
          <fieldset>
            <label for=""><?php echo __('E-Mail Address:'); ?></label>
            <br/>
            <input type="text" name="activation_email" size="25" value="" />
            <br/>
            <?php print_error('<div class="error">%s</div>', 'activation_email'); ?>
            <br/>
            <button type="submit" name="activation" value="1"><b><?php echo __('Request Code &raquo;'); ?></b></button>
          </fieldset>
        </form>
      </div>
<?php
  include('tpl.footer.php');
?>
