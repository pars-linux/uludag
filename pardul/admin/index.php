<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/




include("../inc/functions.inc.php");

$link = MYSQLConnect();

$action = $HTTP_GET_VARS[action];
if($action == "")
	$action = $HTTP_POST_VARS[action];
$subaction = $HTTP_GET_VARS[subaction];
$grpname = $HTTP_GET_VARS[grpname];
$grpmanager = $HTTP_GET_VARS[grpmanager];
$grpid = $HTTP_GET_VARS[grpid];
$formsubmitted = $HTTP_GET_VARS[formsubmitted];
$approved = $HTTP_GET_VARS[approved];

if($action == "login")
	require("login.php");
else {
	session_start();
	if($action == "logoff") {
		session_destroy();
		header("Location: $APPL_URL");
		exit;
	}
}

$loggedin = $HTTP_SESSION_VARS[loggedin];
$userid = $HTTP_SESSION_VARS[userid];
$roleid = $HTTP_SESSION_VARS[roleid];
?>
<html>
<head>
<title>ParDul-Yönetim</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link href="../pardul.css" rel="stylesheet" type="text/css">
</head>
<?if(!$loggedin) {?>
<body>
<center>
<?if($invaliduserpass) {?>
Girdiğiniz kullanıcı adı ve/veya parola yanlış.
<?}?>
<form action="" method="post">
	<input type="hidden" name="action" value="login">
	<table class="arkayan">
		<tr>
			<td colspan="2" align="center">
				Kullanıcı Girişi
			</td>
		</tr>
		<tr>
			<td>
				Kullanıcı Adı:
			</td>
			<td>
				<input type="text" name="username">
			</td>
		</tr>
		<tr>
			<td>
				Parola:
			</td>
			<td>
				<input type="password" name="password">
			</td>
		</tr>
		<tr>
			<td colspan="2" align="center">
				<input type="submit" value="GİRİŞ">
			</td>
		</tr>
	</table>
</form>
<?
} else {
?>
<body bgcolor="#ffffff" topmargin="0" leftmargin="0" marginheight="0" marginwidth="0">
<center>
<table border="1" width="80%">
	<tr>
		<td colspan="2" align="center">
			Kullanıcı tipi: <?echo GetRoleName($roleid);?>
		</td>
	</tr>
	<tr>
		<td align="left" valign="top" width="10%">
			<table>
				<tr>
					<td>
						<a href="?action=groups">Gruplar</a>
					</td>
				</tr>
				<?if($roleid==1) {?>
				<tr>
					<td>
						<a href="?action=admins">Yöneticiler</a>
					</td>
				</tr>
				<?}?>
				<tr>
					<td>
						<a href="?action=requests">İstekler</a>
					</td>
				</tr>
				<tr>
					<td>
						<a href="?action=logoff">ÇIKIŞ</a>
					</td>
				</tr>
			</table>
		</td>
		<td align="center" valign="top" width="80%">
			<table>
				<tr>
					<td align="center">
					<?require("$action.php");?>
					</td>
				</tr>
			</table>
		</td>
	</tr>
</table>
</body>
<?
}
?>
</body>
</html>
<?mysql_close();?>
