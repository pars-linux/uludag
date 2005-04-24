<?php
  require('cfg/sys.define.php');
  require('sys/sys.lib.php');
  require('sys/sys.gettext.php');
  require('sys/sys.database.php');
  require('sys/sys.procedures.php');
  require('sys/sys.pconf.php');
  if (!isset($_NOSESSION)) {
    require('sys/sys.session.php');
  }
?>
