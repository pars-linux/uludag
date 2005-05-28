<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

if(GetRoleName($roleid) != "admin" && !IsManaggedBy($userid, $grpid))
	$comment_status = 'PASSIVE';
else
	$comment_status = 'ACTIVE';
if($formsubmitted) {
	mysql_query("INSERT INTO `comment` ( `id` , `mpvs_id` , `comment` , `emailaddr` , `rname` , `entry_date` , `status` ) VALUES ('', '$statusentryid', '$comment', '$email', '$rname', CURDATE( ) , '$comment_status')");
	require("statusentries.php");
	exit();
}
$groupname = GetGroupName($grpid);
$brandname = GetBrandName($brandid);
$modelname = GetModelName($modelid);
$resultstatus = mysql_query("select * from model_pv_status where id='$statusentryid'");
$rowstatus = mysql_fetch_row($resultstatus);
echo "
	<table border=\"1\">
		<tr>
			<td colspan=\"3\" align=\"center\"><b>$groupname > $brandname > $modelname</b></td>
		</tr>
		<tr>
			<td align=\"center\"><b>Pardus Versiyonu</b></td>
			<td align=\"center\"><b>Durum</b></td>
			<td align=\"center\"><b>Giriş Tarihi</b></td>
		</tr>
	";
$status = GetStatusName($rowstatus[3]);
$pv = GetPVName($rowstatus[2]);
$desc = nl2br($rowstatus[4]);
echo "
	<tr>
	<td>$pv</td>
	<td>$status</td>
	<td>$rowstatus[5]</td>
	</tr>
	<tr>
	<td colspan=\"3\">$desc</td>
	</tr>
	<tr>
	<td colspan=\"3\" align=\"center\">
	";
$addcomment = new HTML_QuickForm('addcomment', 'get', '');
$addcomment->addElement('hidden', 'action', 'addcomment-');
$addcomment->addElement('hidden', 'formsubmitted', 'true');
$addcomment->addElement('hidden', 'grpid', $grpid);
$addcomment->addElement('hidden', 'brandid', $brandid);
$addcomment->addElement('hidden', 'modelid', $modelid);
$addcomment->addElement('hidden', 'statusentryid', $statusentryid);
$addcomment->addElement('text', 'rname', 'İsim Soyisim:');
$addcomment->addElement('text', 'email', 'E-Posta:');
$addcomment->addElement('textarea', 'comment', 'Yorumunuz: ');
$addcomment->addElement('submit', 'btnSave', 'KAYDET');
$addcomment->display();
echo "
	</td>
	</tr>
	</table>
	";
?>
