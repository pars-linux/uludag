<?php

    require_once ("etc/config.php");
    require_once ("lib/functions.php");
    $Sql = "DELETE FROM {$config['db']['users_table']} WHERE UserState='N'";
    db_connection('connect', $config['db']['host'].':'.$config['db']['port'], $config['db']['user'], $config['db']['pass'], $config['db']['dbname'], $config['db']['ctype']);
    mysql_query($Sql);

?>
