<?php
  require('sys.define.php');
  require('sys.gettext.php');
  require('sys.database.php');
  require('sys.procedures.php');
  require('sys.session.php');
  
  require('class.template.php');

  $obj_page = new template('tpl.denied.php');
  $obj_page->flush();
?>
