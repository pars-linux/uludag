<?php
  require('sys.define.php');
  require('sys.gettext.php');
  require('sys.database.php');
  require('sys.procedures.php');
  require('sys.session.php');
  
  require('class.template.php');

  $_PCONF['title'] = CONF_NAME . ' - ' . _('Access Denied');
  $obj_page = new template('tpl.denied.php');
  $obj_page->flush();
?>
