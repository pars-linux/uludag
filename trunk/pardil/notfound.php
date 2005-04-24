<?php
  require('sys.common.php');
  
  require('class/class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Proposal Not Found');
  $obj_page = new template('tpl/tpl.notfound.php');
  $obj_page->flush();
?>
