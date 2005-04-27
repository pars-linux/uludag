<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

$brandname = GetBrandName($brandid);
$grpName = GetGroupName($grpid);
$grpbrnd = IsBrandGroup($brandid, $grpid);
if(GetRoleName($roleid) != "admin" && !IsManaggedBy($userid, $grpid))
	$entry_status = 'PASSIVE';
else
	$entry_status = 'ACTIVE';
if($formsubmitted) {
	if(strlen($newmodel)) {
		if(IsModelGroupBrand($newmodel, $grpid, $brandid)) {
			echo "<b>$groupname</b> grubundaki <b>$brandname</b> markasında <b>$newmodel</b> modeli zaten var.<br>";
			$modelid = IsModel($newmodel);
		}
		else {
			mysql_query("INSERT INTO model ( id , name , groupbrand_id, status ) VALUES ('', '$newmodel', '$grpbrnd', '$entry_status')");
			$modelid = mysql_insert_id();
		}
	}
	mysql_query("INSERT INTO `model_pv_status` ( `id` , `model_id` , `pv_id` , `status_id` , `status_text` , `entry_date` , `status` ) VALUES ('', '$modelid', '$pvid', '$statusid', '$statusdesc', CURDATE(), '$entry_status')");
	require("statusentries.php");
	exit();
}
$addstatusentry = new HTML_QuickForm('addstatusentry', 'get', '');
$addstatusentry->addElement('header', 'header', "$grpName > $brandname");
$addstatusentry->addElement('hidden', 'action', 'addstatusentry');
$addstatusentry->addElement('hidden', 'formsubmitted', 'true');
$addstatusentry->addElement('hidden', 'grpid', $grpid);
$addstatusentry->addElement('hidden', 'brandid', $brandid);
$s =& $addstatusentry->createElement('select','modelid','Model seçiniz: ');
$resultmodels = mysql_query("select id, name from model where groupbrand_id='$grpbrnd' and status='ACTIVE' order by name");
while(($rowmodels=mysql_fetch_row($resultmodels)))
	$opts[$rowmodels[0]] = $rowmodels[1];
$s->loadArray($opts, $selected);
$addstatusentry->addElement($s);
$addstatusentry->addElement('text', 'newmodel', 'Model Listede Yok:');
$s2 =& $addstatusentry->createElement('select','pvid','Pardus Versiyonunu Seçiniz: ');
$resultPVs = mysql_query("select * from pardus_version order by pv_text");
while(($rowPVs=mysql_fetch_row($resultPVs)))
	$opts2[$rowPVs[0]] = $rowPVs[1];
$s2->loadArray($opts2, $selected);
$addstatusentry->addElement($s2);
$s3 =& $addstatusentry->createElement('select','statusid','Durum: ');
$resultstatus = mysql_query("select id, status_name from status order by status_name");
while(($rowstatus=mysql_fetch_row($resultstatus)))
	$opts3[$rowstatus[0]] = $rowstatus[1];
$s3->loadArray($opts3, $selected);
$addstatusentry->addElement($s3);
$addstatusentry->addElement('textarea', 'statusdesc', 'Açıklama: ');
$addstatusentry->addElement('submit', 'btnSave', 'KAYDET');
$addstatusentry->display();
?>
