<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html40/loose.dtd">
<!-- The Interactive Interface to PCI ID's (c) 2001-2002 Martin Mares <mj@ucw.cz> -->

<html><head>
<title>The Linux PCI ID Repository: Batch Submit</title>
</head><body>
<pre>Hello, this is SubmitServer speaking.
<?php
/*
 *  The Interactive Interface to PCI ID's: Batch Submit
 *  (c) 2001--2002 Martin Mares <mj@ucw.cz>
 *  Can be freely distributed and used according to the GNU GPL.
 */

/* Open the database */
include("../../cf/db.conf");
$db = mysql_connect($db_server, $db_user, $db_password) or die("Unable to connect to the database!");
mysql_select_db("pciids") or die("Unable to select the database!");

/* Iterate over submissions */
$author = $HTTP_POST_VARS["author"];
$notice = $HTTP_POST_VARS["notice"];
foreach ($HTTP_POST_VARS as $k => $v)
	if (ereg('^a([0-9a-f]+)$', $k, $a)) {
		$id = $a[1];
		if (strlen($id) == 16) $type = 's';
		elseif (strlen($id) == 8) $type = 'd';
		elseif (strlen($id) == 4) $type = 'v';
		else continue;
		list($name,$cmt) = explode("\t", $v);
		print "$id: ";
		$qr = mysql_query("select recid from ids where id='$id' and name=binary '" . mysql_escape_string($name) . "' and comment=binary '" . mysql_escape_string($cmt) . "'");
		if ($qr && mysql_fetch_array($qr))
			print "Already present\n";
		else {
			if (mysql_query("insert into ids (id,name,status,comment,type,author) values ('$id','" . mysql_escape_string($name) . "',1,'" . mysql_escape_string($cmt) . "','$type','" . mysql_escape_string($author) . "')")) {
				print "Added\n";
				$recid = mysql_insert_id();
				if (!$cmt) $cmt=$notice;
				idlog("Batch submit: $recid $id '" . mysql_escape_string($name) . "' '" . mysql_escape_string($cmt) . "' '" . mysql_escape_string($author) . "'");
			} else
				print "FAILED\n";
		}
	}

print "Submit OK\n";
return;

function idlog($msg)
{
	global $logfile, $username, $HTTP_SERVER_VARS;
	$now = time();
	$who = "?";
	$ip = $HTTP_SERVER_VARS["REMOTE_ADDR"];
	if (!isset($logfile)) $logfile = fopen("log", "a");
	fputs($logfile, "$now $who $ip $msg\n");
	fflush($logfile);
}

?>
</pre>
</body></html>
