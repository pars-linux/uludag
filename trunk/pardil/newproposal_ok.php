<?php

  require('sys.common.php');

  require('class/class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('New Proposal Submitted');
  $obj_page = new template('tpl/tpl.newproposal_ok.php');
  $obj_page->setvar('bln_approved', ($_GET['approved'] == 1));
  $obj_page->setvar('int_proposal', $_GET['proposal']);
  $obj_page->flush();
?>
