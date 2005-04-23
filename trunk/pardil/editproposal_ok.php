<?php

  require('cfg/sys.define.php');
  require('sys/sys.gettext.php');
  require('sys/sys.database.php');
  require('sys/sys.procedures.php');
  require('sys/sys.pconf.php');

  require('class/class.template.php');

  $_PCONF['title'] = $_PCONF['site_name'] . ' - ' . __('Proposal Updated');
  $obj_page = new template('tpl/tpl.editproposal_ok.php');
  $obj_page->setvar('int_proposal', $_GET['proposal']);
  $obj_page->setvar('dbl_revision', $_GET['revision']);
  $obj_page->setvar('bln_newrevision', ($_GET['newrevision'] == 1));
  $obj_page->flush();
?>
