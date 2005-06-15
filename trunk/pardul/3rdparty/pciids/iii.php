<?php
/*
 *  The Interactive Interface to PCI ID's
 *  (c) 2001--2003 Martin Mares <mj@ucw.cz>
 *  Can be freely distributed and used according to the GNU GPL.
 */

/* Parse parameters */
$options = array(
	"i"		=> array ( "var" => "id", "def" => "", "reg" => "[0-9a-fA-F:]*" ),
	"m"		=> array ( "var" => "mode", "def" => 0, "reg" => "[0-9]" ),
	"s"		=> array ( "var" => "sortby", "def" => 0, "reg" => "[0-9]" ),
	"n"		=> array ( "var" => "new", "def" => 0, "reg" => "[01]" ),
	"a"		=> array ( "var" => "approve", "def" => 0, "reg" => "[01]", "inonly" => 1 ),
	"allids"	=> array ( "var" => "approveids", "def" => "", "reg" => "[0-9,]*", "inonly" => 1 ),
	"xall"		=> array ( "var" => "xall", "def" => 0, "reg" => "on", "inonly" => 1 ),
	"dall"		=> array ( "var" => "dall", "def" => 0, "reg" => "on", "inonly" => 1 ),
	"submitted"	=> array ( "var" => "submitted", "def" => 0, "reg" => "[01]", "inonly" => 1 ),
	"newid"		=> array ( "var" => "newid", "def" => "", "reg" => ".*", "inonly" => 1 ),
	"newname"	=> array ( "var" => "newname", "def" => "", "reg" => ".*", "inonly" => 1 ),
	"newcmt"	=> array ( "var" => "newcmt", "def" => "", "reg" => ".*", "inonly" => 1 ),
	"newauthor"	=> array ( "var" => "newauthor", "def" => "", "reg" => ".*", "inonly" => 1 ),
	"sub"		=> array ( "var" => "showsubmit", "def" => 0, "reg" => "[01]", "inonly" => 1 ),
	"edit"		=> array ( "var" => "editid", "def" => "", "reg" => "[0-9]*", "inonly" => 1 ),
	"p"		=> array ( "var" => "page", "def" => "", "reg" => "[0-9A-Za-z*]" )
);
parse_params();

/* Open the database as we'll need it for authentication soon */
include("/var/www/pardul.uludag.org.tr/htdocs/3rdparty/pciids/db_pciids.inc.php");


/* Check modes: 0=default, 1=only approved, 9=admin */
$filter = "";
$admin = 0;
if ($mode == 1) {
	$filter = "and status=0";
} elseif ($mode == 9) {
	if (!admin_auth()) return;
	$admin = 1;
}

/* If we are editing, jump to the right record */
if ($editid) {
	$qr = mysql_query("select id,name,comment,author from pciids where recid=$editid");
	list($newid, $newname, $newcmt, $newauthor) = mysql_fetch_array($qr);
	list($id,$newid) = id_split($newid);
	$showsubmit = 1;
}

/* Prepare table parameters and headings */
$idref = selflink(array("id" => "", "page" => ""));
if ($idref != "?") $idref = "$idref:";
$idref = "${idref}i=";
$order = $sortby ? "name" : "id";
$id = ereg_replace(':', '', strtolower($id));
if (strlen($id) == 4) {
	$type = 'd';
	$showf = '(....)(.*)';
	$showt = "<a href='$idref\\1\\2'>\\2</a>";
	$title = "Vendor $id";
	$etype = 'device';
	$url_up = selflink(array("id" => ""));
	$paged = 0;
} elseif (strlen($id) == 8) {
	$type = 's';
	$showf = '(.*)(....)(....)$';
	$showt = '\2:\3';
	$title = "Subsystems for device " . ereg_replace('(....)(.*)','\1:\2',$id);
	$etype = 'subsystem';
	$url_up = selflink(array("id" => ereg_replace('(....)(.*)', '\1', $id)));
	$paged = 0;
} else {
	$type = 'v';
	$showf = '(.*)';
	$showt = "<a href='$idref\\1'>\\1</a>";
	$title = "All Vendors";
	$etype = 'vendor';
	$url_up = "";
	$paged = 1;
}

/* Need to cripple stylesheets for buggy Netscape 4 */
if (ereg('Mozilla/4', $HTTP_SERVER_VARS["HTTP_USER_AGENT"])) $ssbug = 'bug'; else $ssbug = '';

if ($new)
	$paged = 0;
if (!$paged)
	$page = "";

?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html40/loose.dtd">
<!-- The Interactive Interface to PCI ID's (c) 2001-2003 Martin Mares <mj@ucw.cz> -->

<html><head>
<link rel=stylesheet href='pciids.css' type='text/css'>
<title>The Linux PCI ID Repository: <?php echo "$title"; ?></title>
</head><body>
<?php

/* Structure of the database:
 * +---------+---------------------+------+-----+---------+----------------+
 * | Field   | Type                | Null | Key | Default | Extra          |
 * +---------+---------------------+------+-----+---------+----------------+
 * | recid   | int(10) unsigned    |      | PRI | NULL    | auto_increment |
 * | id      | varchar(16)         |      | MUL |         |                |
 * | name    | varchar(128)        | YES  |     | NULL    |                |
 * | status  | tinyint(3) unsigned | YES  |     | NULL    |                |
 * | comment | varchar(128)        | YES  |     | NULL    |                |
 * | type    | char(1)             | YES  | MUL | NULL    |                |
 * | author  | varchar(64)         | YES  |     | NULL    |                |
 * +---------+---------------------+------+-----+---------+----------------+
*/

$t = $title;
$parent_found = 1;
if ($type != 'v') {
	$qr = mysql_query("select name from pciids where id='$id' order by status") or die("Query failed");
	if ($l = mysql_fetch_array($qr)) { $t = "$title: $l[0]"; } else { $t = "$title: UNKNOWN"; $parent_found = 0; }
}
echo "<div id=headbar$ssbug>
<h1 class=collapse>The Linux PCI ID Repository</h1>
<p class=collapse style='margin-top: 1ex'>The home of the <code>pci.ids</code> file
</div>
<div id=headbox1$ssbug>
<p>";
if ($url_up) { echo "<span class=singline$bug><a href='$url_up'>Go Up</a></span>\n"; }
else { echo "<span class=singline$bug><a href='/'>Go Home</a></span>\n"; }
echo "<span class=singline$bug><a href='", selflink(array()), "'>Reload</a></span>\n";
echo "<span class=singline$bug><a href='", selflink(array("showsubmit" => 1)), "'>New Entry</a></span>\n";
echo "</div>
<div id=headbox2$ssbug>
<p>";

if ($admin) {
	$qr = mysql_query("select count(*) from pciids where id>'$id' and id<'${id}g'");
	$stotal = 0;
	$qr && (list($stotal) = mysql_fetch_array($qr));
	$qr = mysql_query("select count(*) from pciids where id>'$id' and id<'${id}g' and status<>0");
	$snew = 0;
	$qr && (list($snew) = mysql_fetch_array($qr));
	echo "<span class=singline$ssbug><a href='", selflink(array("new" => 0)) ,"'>$stotal entries</a></span>\n";
	echo "<span class=singline$ssbug><a href='", selflink(array("new" => 1)), "'>$snew new</a></span>\n";
} else {
	echo "<span class=singline$ssbug><a href='", selflink(array("mode" => 9)), "'>Admin Mode</a></span>\n";
	echo "<span class=singline$ssbug><a href='", selflink(array("mode" => 1)), "'>Approved Only</a></span>\n";
	echo "<span class=singline$ssbug><a href='mailto:pciids-devel@lists.sourceforge.net'>Feedback</a></span>\n";
}

echo "</div>\n";

if ($approve) {
	approval();
} elseif ($submitted && $newid) {
	$msg = new_record();
	echo "<p>$msg\n";
}

echo "<h2>", htmlspecialchars($t), ($new ? " (new entries)" : ""), "</h2>\n";

if ($showsubmit)
	submit_form();

if ($paged) {
	if ($sortby) $pages = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
	else $pages = "0123456789abcdef";
	if ($page == "")
		$page = substr($pages,0,1);
	if ($page != "*") {
		$lpage = strtolower($page); $lpagen = chr(ord($lpage)+1);
		$upage = strtoupper($page); $upagen = chr(ord($upage)+1);
		if ($sortby)
			$filter = "$filter and (name >= '$lpage' and name < '$lpagen' or name >= '$upage' and name < '$upagen')";
		else
			$filter = "$filter and id >= '$id$lpage' and id < '$id${lpage}g'";
	}
	echo "<p>";
	foreach (explode(" ", ereg_replace('(.)', '\1 ', $pages)) as $p)
		echo "<a href='", selflink(array("page" => $p)), "'>$p</a>\n";
	echo "<a href='", selflink(array("page" => "*")), "'>All</a>\n";
	echo "<p>\n";
}

if ($admin) echo "<form action='iii.php' method=post enctype='application/x-www-form-urlencoded'>\n";
echo "<table class=idtab width='100%'><thead><tr><td><a href='", selflink(array("sortby" => 0, "page" => "")), "'>ID</a></td>";
if ($admin) echo "<td>OK/Del</td>";
echo "<td><a href='", selflink(array("sortby" => 1, "page" => "")), "'>Name</a></td></tr></thead><tbody>\n";
$s=0;
$newids = '';
if ($admin) echo "<tr><td>All:</td><td><input type=checkbox name=xall class=gb><input type=checkbox name=dall class=rb></td></tr>";
if ($new) {
	$qr = mysql_query("select recid,id,name,status,comment,author from pciids where id>'$id' and id<'${id}g' and status<>0 order by id,recid limit 100");
	$lastid = '';
	$counter = 0;
	while (list($xrecid,$xid,$xname,$xstat,$xcmt,$xauth) = mysql_fetch_array($qr)) {
		$lastanc = '';
		$anc = array(substr($xid,0,4), substr($xid,0,8), $xid);
		foreach ($anc as $yid) {
			$rid = substr($yid, strlen($id));
			if ($lastanc == $rid) continue;
			$lastanc = $rid;
			if (strcmp($rid, $lastid) <= 0 && $xid != $yid) continue;
			if ($xid != $yid || $xstat && $rid != $lastid) {
				$qrr = mysql_query("select recid,name,comment,author from pciids where id='$yid' and status=0");
				if (list($yrecid,$yname,$ycmt,$yauth) = mysql_fetch_array($qrr)) {
					if (strlen($yid) != 16)
						$ridref = "<a href='$idref$yid'>$rid</a>";
					else
						$ridref = "$rid";
					show_id_row($s, $yrecid, $yid, $ridref, $yname, 0, $ycmt, $yauth);
					$s = 1-$s;
				}
			}
			if ($xid == $yid) {
				show_id_row($s, $xrecid, $xid, $rid, $xname, $xstat, $xcmt, $xauth);
				$s = 1-$s;
			}
			$lastid = $rid;
		}
		$counter++;
	}
	echo "</tbody></table>\n";
	if ($counter >= 100) echo "<p><em>(More...)</em>\n";
} elseif (!$editid) {
	$qr = mysql_query("select recid,id,name,status,comment,author from pciids where type='$type' and id>'$id' and id<'${id}g' $filter order by $order,status,recid") or die("Query failed");
	while (list($xrecid,$xid,$xname,$xstat,$xcmt,$xauth) = mysql_fetch_array($qr)) {
		show_id_row($s, $xrecid, $xid, ereg_replace($showf, $showt, $xid), $xname, $xstat, $xcmt, $xauth);
		$s = 1-$s;
	}
	echo "</tbody></table>\n";
}
if ($admin) {
	echo "<p><input type=submit name=action value='Submit changes'>\n";
	selfform(array("approve" => 1, "approveids" => substr($newids,1)));
	echo "</form>\n";
	echo "<form action='iii.php' method=post enctype='application/x-www-form-urlencoded'>\n";
	echo "<input type=submit name=action value='Go to'> <input type=text name=i value='$id' size=20 maxlength=16>\n";
	selfform(array("id" => ""));
	echo "</form>\n";
}

echo "
<p>Green entries are new submissions not approved by the maintainers yet.
";

function submit_form()
{
	global $type, $etype, $newid, $newname, $newcmt, $newauthor;
	echo "<p>If you want to add a new $etype entry to this table, just use the form below: fill in the ";
	if ($type == 'v') echo "4-digit vendor ID";
	elseif ($type == 'd') echo "4-digit device ID";
	else echo "'vvvv:dddd' subsystem ID";
	echo " and the full name of the $etype.
<em>Important:</em> Please try to specify as accurate names as you can. ";
	if ($type == 'v') {
		echo "Vendor name should be the full name of the company, for example
<tt>Intel Corporation</tt> or <tt>Yoyodyne Inc</tt>.\n";
	} elseif ($type == 'd') {
		echo "Device name should be the real name of the chip, not of the board
(except maybe custom IC's manufactured for use in a single board). If the chip has
some marketing name, please enclose it in square brackets; use parentheses for
alternative names where appropriate. Example:
<tt>82820 820 [Camino] Chipset Host Bridge (MCH)</tt>.\n";
	} elseif ($type == 's') {
		echo "Please don't include vendor names in subsystem ID descriptions,
they are automatically extracted from the subsystem vendor ID.\n";
	}
	echo "Note that some fraction of the existing entries doesn't obey these rules
yet, so please don't get fooled by them, they are just waiting to be converted.
<p>If you have anything important to mention, write it to the Comment field.
<p>If you want to update an entry, just submit a new entry with the same ID. To delete
an entry, update it to a blank name. <em>In both cases, please use the Comment
to explain the reason for the change.</em>
<p>Please include your e-mail address, it will be available only to our
administrators and used for feedback on your entries.

<form method='post' action='iii.php' enctype='application/x-www-form-urlencoded'>
<p><table align=center border=0 id=querybox>
<tr><td colspan=4 align=center id=qbhead>Submit new $etype entry</td></tr>
<tr><td>ID:</td><td><input class=pciid type=text size=8 name=newid value='", htmlspecialchars($newid, ENT_QUOTES), "'></td></tr>
<tr><td>Name:</td><td><input type=text size=64 name=newname value='", htmlspecialchars($newname, ENT_QUOTES), "'></td></tr>
<tr><td>Comment:</td><td><input type=text size=64 name=newcmt value='", htmlspecialchars($newcmt, ENT_QUOTES), "'></td></tr>
<tr><td>E-mail:</td><td><input type=text size=64 name=newauthor value='", htmlspecialchars($newauthor, ENT_QUOTES), "'></td></tr>
<tr><td colspan=4 align=center><input type='submit' name='action' value='Submit'></td></tr>
</table>
";
	selfform(array("showsubmit" => 1, "submitted" => 1));
	echo "</form>\n";
}

function new_record()
{
	global $parent_found, $newid, $newname, $newcmt, $newauthor, $id, $type;
	$newid = ereg_replace(':', '', strtolower($newid));
	if (!$parent_found) return "Parent entry not found";
	if (!ereg('^[0-9a-f]+$', $newid)) return "Invalid characters in ID";
	if (strlen($newid) != ($type == 's' ? 8 : 4)) return "Invalid ID";
	$newname = ereg_replace('(^ +| +$)', '', $newname);
	$newcmt = ereg_replace('(^ +| +$)', '', $newcmt);
	$newauthor = ereg_replace('(^ +| +$)', '', $newauthor);
	$xid = "$id$newid";
	if (!($qr = mysql_query("select name from pciids where id='$xid' and name=binary '" . mysql_escape_string($newname) . "' and comment=binary '" . mysql_escape_string($newcmt) . "'"))) return "Query failed";
	if (mysql_fetch_array($qr)) return "Record already present";
	if ($type == 's') {
		$xvendor = ereg_replace('(....).*', '\1', $newid);
		if (!(($qr = mysql_query("select name from pciids where id='$xvendor'")) && mysql_fetch_array($qr)))
			return "Vendor $xvendor of this subsystem is not known yet.";
	}
	if (!($qr = mysql_query("insert into ids (id,name,comment,type,status,author) values ('$xid', '" . mysql_escape_string($newname) . "', '" . mysql_escape_string($newcmt) . "', '$type', 1, '" . mysql_escape_string($newauthor) . "')")))
		return "Insert failed";
	$recid = mysql_insert_id();
	idlog("Create $recid $xid '" . mysql_escape_string($newname) . "' '" . mysql_escape_string($newcmt) . "' '" . mysql_escape_string($newauthor) . "'");
	return "Entry added.";
}

function approval()
{
	global $admin, $HTTP_POST_VARS, $xall, $dall, $approveids;
	echo "<h3>Approval results:</h3>\n";
	if (!$admin) { echo "<p>Permission denied. How did you get here?\n"; return; }
	echo "<table class=tabex>\n";
	/* Handle defaults */
	if ($xall || $dall) {
		$xx = $xall ? "x" : "d";
		foreach (explode(',', $approveids) as $k)
			if (!isset($HTTP_POST_VARS["x$k"]) && !isset($HTTP_POST_VARS["d$k"]))
				$HTTP_POST_VARS["$xx$k"] = "on";
	}
	/* Preprocess all operations */
	$adds = array ();
	$dels = array ();
	$names = array ();
	$titles = array ();
	$newcomments = array ();
	$oldcomments = array ();
	$admincomments = array ();
	$authors = array ();
	foreach ($HTTP_POST_VARS as $k => $v) {
		if ($v == "on" && ereg('^([xde])([0-9]+)$', $k, $x)) {
			$xop = $x[1];
			$xrec = $x[2];
			$qr = mysql_query("select id,name,comment,author from pciids where recid='$xrec'") or die("Query failed");
			if (!(list($xid,$xname,$xcmt,$xauth) = mysql_fetch_array($qr))) {
				echo "<tr><td>R$xrec</td><td class=red>NOT FOUND</td></tr>\n";
				continue;
			}
			if ($xop == 'x') {
				$adds["$xid.$xrec"] = $xrec;
				if ($xname == '') $dels["$xid.$xrec"] = $xrec;
			} elseif ($xop == 'd') $dels["$xid.$xrec"] = $xrec;
			$titles[$xrec] = "<td>R$xrec</td><td class=pciids>$xid</td><td>" . htmlspecialchars($xname) . "</td>";
			$oldcomments[$xrec] = $xcmt;
			$authors[$xrec] = $xauth;
		} elseif (ereg('^c([0-9]+)$', $k, $x)) {
			$admincomments[$x[1]] = $newcomments[$x[1]] = ereg_replace('(^ +| +$)', '', $v);
		} elseif (ereg('^n([0-9]+)$', $k, $x)) {
			$names[$x[1]] = ereg_replace('(^ +| +$)', '', $v);
		}
	}
	/* Process comments */
	foreach ($oldcomments as $xrec => $xcmt) {
		if ($xcmt == $admincomments[$xrec])
			$admincomments[$xrec] = '';
	}
	/* Do the additions first */
	ksort($adds, SORT_STRING);
	foreach ($adds as $k => $xrec) {
		echo "<tr>", $titles[$xrec];
		$qr = mysql_query("select id from pciids where recid='$xrec'") or die("Query failed");
		if (!(list($xid) = mysql_fetch_array($qr))) {
			echo "<td class=red>NOT FOUND</td></tr>\n";
			continue;
		}
		mysql_query("update ids set status=1 where id='$xid'");
		mysql_query("update ids set status=0" .
			", name='" . mysql_escape_string($names[$xrec]) . "'" .
			", comment='" . mysql_escape_string($newcomments[$xrec]) . "'" .
			" where recid='$xrec'");
		$qr = mysql_query("select recid from pciids where id='$xid' and status<>0");
		while (list($zrec) = mysql_fetch_array($qr)) {
			idlog("Overriden $zrec $xid '" . mysql_escape_string($admincomments[$xrec]) . "' '" . mysql_escape_string($authors[$xrec]) . "'");
		}
		mysql_query("delete from pciids where id='$xid' and status<>0");
		echo "<td class=green>OK</td></tr>\n";
		idlog("Approve $xrec $xid '" . mysql_escape_string($admincomments[$xrec]) . "' '" . mysql_escape_string($authors[$xrec]) . "'");
	}
	/* Then removals */
	krsort($dels, SORT_STRING);
	foreach ($dels as $k => $xrec) {
		echo "<tr>", $titles[$xrec];
		$qr = mysql_query("select id from pciids where recid='$xrec'") or die("Query failed");
		if (!(list($xid) = mysql_fetch_array($qr))) {
			echo "<td class=red>ALREADY DELETED</td></tr>\n";
			continue;
		}
		$qr = mysql_query("select id from pciids where id > '$xid' and id < '{$xid}g'");
		if (!$qr || mysql_fetch_array($qr)) {
			$qr = mysql_query("select recid from pciids where id='$xid' and recid<>$xrec");
			if (!$qr || !mysql_fetch_array($qr)) {
				echo "<td class=red>NOT EMPTY</td></tr>\n";
				continue;
			}
		}
		mysql_query("delete from pciids where recid='$xrec'");
		echo "<td class=green>DELETED</td></tr>\n";
		idlog("Delete $xrec $xid '" . mysql_escape_string($admincomments[$xrec]) . "' '" . mysql_escape_string($authors[$xrec]) . "'");
	}
	echo "</table>\n";
}

function admin_auth()
{
	global $PHP_CGI, $HTTP_SERVER_VARS, $username;
/*
	if ($PHP_CGI) $aa = $HTTP_SERVER_VARS["HTTP_AUTHORIZATION"];
	else {
		$hh = getallheaders();
		$aa = $hh["Authorization"];
	}
	if ($aa) {
		list($atype, $userpass) = split(' ', $aa);
		if (strtolower($atype) == "basic") {
			list($auser, $apass) = split(':', base64_decode($userpass));
*/
/*
	if (($auser = $HTTP_SERVER_VARS["PHP_AUTH_USER"]) &&
	    ($apass = $HTTP_SERVER_VARS["PHP_AUTH_PW"])) {
		$qr = mysql_query("select password from users where name='" . mysql_escape_string($auser) . "'");
		if ($qr && (list($amd5) = mysql_fetch_array($qr)) && $amd5 == md5($apass)) {
				$username = $auser;
				return 1;
			}
	}
	*/
	if (($auser = $HTTP_SERVER_VARS["PHP_AUTH_USER"]) &&
	    ($apass = $HTTP_SERVER_VARS["PHP_AUTH_PW"])) {
		if ($auser=="tolga" && $apass = "tolga") {
				$username = $auser;
				return 1;
			}
	}
	header("Status: 401 Not authorized");
	header("WWW-Authenticate: Basic realm=\"PCI ID Administration\"");
	return 0;
}

function parse_params()
{
	global $options, $HTTP_POST_VARS, $HTTP_SERVER_VARS;
	if ($qs = $HTTP_SERVER_VARS["QUERY_STRING"])
		foreach (split('[:&]', $qs) as $q) {
			list($qv, $qx) = explode('=', $q);
			$getvars[$qv] = urldecode($qx);
		}
	foreach ($options as $name => $attrs) {
		$var = $attrs["var"];
		$def = $attrs["def"];
		$reg = '^' . $attrs["reg"] . '$';
		if ((($a = $HTTP_POST_VARS[$name]) || ($a = $getvars[$name])) && ereg($reg, $a))
			$GLOBALS[$var] = $a;
		else
			$GLOBALS[$var] = $def;
	}
}

function getvars($overrides)
{
	global $options;
	$vars = array();
	foreach ($options as $name => $attrs) {
		$var = $attrs["var"];
		$def = $attrs["def"];
		if (isset($overrides[$var]))
			$a = $overrides[$var];
		elseif (!$attrs["inonly"])
			$a = $GLOBALS[$var];
		else
			$a = $def;
		if ($a != $def)
			$vars[$name] = $a;
	}
	return $vars;
}

function selflink($overrides)
{
	$url = "";
	foreach (getvars($overrides) as $name => $value)
		$url = "$url:$name=" . urlencode($value);
	return ereg_replace('^(:|$)', '?', $url);
}

function selfform($overrides)
{
	foreach (getvars($overrides) as $name => $value)
		echo "<input type=hidden name=$name value='", htmlspecialchars($value, ENT_QUOTES), "'>\n";
}

function idlog($msg)
{
	global $logfile, $username, $HTTP_SERVER_VARS;
	$now = time();
	$ip = $HTTP_SERVER_VARS["REMOTE_ADDR"];
	$who = $username ? $username : "?";
	if (!isset($logfile)) $logfile = fopen("log", "a");
	fputs($logfile, "$now $who $ip $msg\n");
	fflush($logfile);
}

function show_id_row($s, $recid, $id, $rid, $name, $stat, $cmt, $auth)
{
	global $admin, $newids;
	echo "<tr class=s$s$stat><td>$rid</td>";
	if ($admin) {
		if ($name == "" && !$stat)
			echo "<td><input type=checkbox name=x$recid class=gb disabled><input type=checkbox name=d$recid class=rb checked></td>";
		elseif ($stat)
			echo "<td><input type=checkbox name=x$recid class=gb><input type=checkbox name=d$recid class=rb></td>";
		else
			echo "<td><a href='", selflink(array("editid" => $recid, "new" => 0)), "'>Edit</a></td>";
	}
	echo "<td>";
	if ($admin && $stat) {
		echo "<input type=text name=n$recid maxlength=128 size=64 class=s$s$stat value='", htmlspecialchars($name, ENT_QUOTES), "'>";
		echo "<br><input type=text name=c$recid maxlength=128 size=64 class=s$s$stat";
		if ($cmt) echo " value='", htmlspecialchars($cmt, ENT_QUOTES), "'";
		echo ">";
		if ($auth) echo "<br><code>", htmlspecialchars($auth), "</code>";
	} else {
		echo htmlspecialchars($name);
		if ($cmt) echo "<br><em>", htmlspecialchars($cmt), "</em>";
	}
	echo "</td></tr>\n";
	if ($stat)
		$newids="$newids,$recid";
}

function id_split($id)
{
	$l = strlen($id);
	if ($l == 4)
		ereg('^()(....)$', $id, $x);
	elseif ($l == 8)
		ereg('^(....)(....)$', $id, $x);
	elseif ($l == 16)
		ereg('^(........)(........)$', $id, $x);
	else
		$x = array('', '', '');
	array_shift($x);
	return $x;
}

?>

<hr>
<p>The Interactive Interface to PCI ID's (c) 2001-2003 <a href="http://www.ucw.cz/~mj/">Martin Mares</a>.
Browser bugs are (c) their authors.
</body></html>
