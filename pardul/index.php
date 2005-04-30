<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.


 -- index.php
 
 uygulamadaki (login formundan gelen istekler dışındaki) bütün istekler buraya
 yönlendirilir. isteğin neyle ilgili olduğu bilgisi $action değişkeninde tutulur
 ve "$action.php" dosyası require edilir.

*/




include("inc/functions.inc.php");
require_once 'HTML/QuickForm.php';
require_once "HTML/Table.php";
require_once 'HTML/Menu.php';

$link = MYSQLConnect();

/*
 set edilsin ya da edilmesin bütün post/get_vars verileri burada alınır. set edilen
 gerekli veriler "$action.php" tarafından kullanılır.
*/

$action = $HTTP_GET_VARS[action];
if(!isset($action))
	$action = $HTTP_POST_VARS[action];
$subaction = $HTTP_GET_VARS[subaction];
$grpname = $HTTP_GET_VARS[grpname];
$grpmanager = $HTTP_GET_VARS[grpmanager];
$grpid = $HTTP_GET_VARS[grpid];
$formsubmitted = $HTTP_GET_VARS[formsubmitted];
$approved = $HTTP_GET_VARS[approved];
$newbrand = $HTTP_GET_VARS[newbrand];
$brandname = $HTTP_GET_VARS[brandname];
$brandid = $HTTP_GET_VARS[brandid];
$pvid = $HTTP_GET_VARS[pvid];
$pvname = $HTTP_GET_VARS[pvname];
$statusid = $HTTP_GET_VARS[statusid];
$statusname = $HTTP_GET_VARS[statusname];
$statusdesc = $HTTP_GET_VARS[statusdesc];
$modelname = $HTTP_GET_VARS[modelname];
$modelid = $HTTP_GET_VARS[modelid];
$newgrpid = $HTTP_GET_VARS[newgrpid];
$newbrandid = $HTTP_GET_VARS[newbrandid];
$grpbrnd = $HTTP_GET_VARS[grpbrnd];
$newmodel = $HTTP_GET_VARS[newmodel];
$statusentryid = $HTTP_GET_VARS[statusentryid];
$status = $HTTP_GET_VARS[status];
$email = $HTTP_GET_VARS[email];
$rname = $HTTP_GET_VARS[rname];
$comment = $HTTP_GET_VARS[comment];
$commentid = $HTTP_GET_VARS[commentid];



if(!isset($action))     // $action set edilmemişse
	$action = 'groups'; // yapılacak en mantıklı şey kök kategoriyi göstermek
session_start();
if($action == "logoff") {
	session_destroy();
	header("Location: $APPL_URL");
}

$userid = $HTTP_SESSION_VARS[userid];
$roleid = $HTTP_SESSION_VARS[roleid];
$loggedin = $HTTP_SESSION_VARS[loggedin];

if($loggedin) { // login olunmuşsa göstermemiz gereken bir menü ve rolName var.
	$roleName = GetRoleName($roleid);
	$menuItems = array(0 => array('title' => 'Gruplar', 'url' => '?action=groups'));
	if(GetRoleName($roleid)=='admin') { // 
		$to_push = array('title' => 'Yöneticiler', 'url' => '?action=admins');
		array_push($menuItems, $to_push);
		$to_push = array('title' => 'Parametreler', 'url' => '?action=parameters');
		array_push($menuItems, $to_push);
	}
	$to_push = array('title' => 'ÇIKIŞ', 'url' => '?action=logoff');
	array_push($menuItems, $to_push);	
	$menu =& new HTML_Menu($menuItems, 'tree');
	$title = "ParDul Yönetim";
}
else
	$title = "ParDul";
addPageHeader($title);
echo "
<table widt=\"80%\" border=\"1\">
	<tr>
		<td colspan=\"2\" align=\"center\">
";
if($loggedin)
	echo "
	Kullanıcı tipi: $roleName
 	";
else
	echo "
	<a href=\"?action=login\">Yönetici</a>
 	";
echo "
		</td>
	</tr>
	<tr>
		<td align=\"left\" valign=\"top\" width=\"10%\">
";
if($loggedin) // login olunmuşsa menüyü bas
	$menu->show();
else
	echo "
	PARDUL
	";
echo "
	</td>
	<td align=\"center\" valign=\"top\" width=\"90%\">
		<table>
			<tr>
				<td align=\"center\">
";
if(!file_exists("$action.php"))
	echo "pardul bunun nasıl yapılacağını bilmiyor: $action";
else
	require("$action.php"); // ilgili .php dosyasını require et
echo "
	</tr>
	</table>
";
addPageFooter();
mysql_close();
?>
