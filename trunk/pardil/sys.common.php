<?php
  require(dirname(__FILE__) . '/cfg/sys.define.php');
  require(dirname(__FILE__) . '/sys/sys.lib.php');
  require(dirname(__FILE__) . '/sys/sys.gettext.php');
  require(dirname(__FILE__) . '/sys/sys.database.php');
  require(dirname(__FILE__) . '/sys/sys.procedures.php');
  require(dirname(__FILE__) . '/sys/sys.pconf.php');
  if (!isset($_NOSESSION)) {
    require(dirname(__FILE__) . '/sys/sys.session.php');
  }
?>
