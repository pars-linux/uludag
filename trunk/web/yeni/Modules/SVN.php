<?php
   
    header("Content-Type: application/xml; charset=UTF-8");
    $SvnServer = 'http://svn.pardus.org.tr/';
    $Limit = 5;
    function getLogs($Repo) {
#        global $SvnServer,$Limit;
#        exec ('svn log '.$SvnServer.$Repo.' --xml --limit '.$Limit.' > /tmp/svnlog-'.$Repo);
        $logFile = '/tmp/svnlog-'.$Repo;
        $filePointer = @fopen($logFile,'r');
        echo fread($filePointer,filesize($logFile));
    }

    if ($_GET['Repo']==='pardus' OR $_GET['Repo']==='uludag')
        getLogs($_GET['Repo']);
   
?>
