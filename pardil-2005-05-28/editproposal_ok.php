<?php

  require(dirname(__FILE__) . '/sys.common.php');

  require(dirname(__FILE__) . '/class/class.template.php');

  $_PCONF['title'] = getop('site_name') . ' - ' . __('Proposal Updated');
  $obj_page = new template(dirname(__FILE__) . '/tpl/tpl.editproposal_ok.php');
  $obj_page->setvar('int_proposal', $_GET['proposal']);
  $obj_page->setvar('dbl_revision', $_GET['revision']);
  $obj_page->setvar('bln_newrevision', ($_GET['newrevision'] == 1));
  $obj_page->flush();
?>
