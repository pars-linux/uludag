<?php

  require('sys.define.php');
  require('sys.gettext.php');
  require('sys.database.php');
  require('sys.procedures.php');

  require('class.template.php');

  $_PCONF['title'] = CONF_NAME . ' - ' . _('Registration Complete');
  $obj_page = new template('tpl.register_ok.php');
  $obj_page->flush();
?>
