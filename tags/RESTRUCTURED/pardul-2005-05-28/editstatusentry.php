<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/
$grpbrnd = IsBrandGroup($brandid, $grpid);
if(GetRoleName($roleid) != "admin" && !IsManaggedBy($userid, $grpid)) {
	echo "Durum bilgisi düzenlme işlemi için yetkiniz yok.";
	exit;
}
if($formsubmitted) {
	if(strlen($newmodel)) {
		if(IsModelGroupBrand($newmodel, $grpid, $brandid)) {
			echo "<b>$groupname</b> grubundaki <b>$brandname</b> markasında <b>$newmodel</b> modeli zaten var.<br>";
			$modelid = IsModel($newmodel);
		}
		else {
			mysql_query("INSERT INTO model ( id , name , groupbrand_id, status ) VALUES ('', '$newmodel', '$grpbrnd', 'ACTIVE')");
			$modelid = mysql_insert_id();
		}
	}
	mysql_query("update model_pv_status set model_id='$modelid', pv_id='$pvid', status_id='$statusid', status_text='$statusdesc', status='$status' where id='$statusentryid'");
	require("statusentries.php");
	exit();
}
$resultstatusentry = mysql_query("select * from model_pv_status where id = '$statusentryid'");
$rowstatusentry = mysql_fetch_row($resultstatusentry);
$editstatusentry = new HTML_QuickForm('editstatusentry', 'get', '');
$editstatusentry->addElement('hidden', 'action', 'editstatusentry');
$editstatusentry->addElement('hidden', 'formsubmitted', 'true');
$editstatusentry->addElement('hidden', 'brandid', $brandid);
$editstatusentry->addElement('hidden', 'grpid', $grpid);
$editstatusentry->addElement('hidden', 'statusentryid', $statusentryid);
$s =& $editstatusentry->createElement('select','modelid','Model seçiniz: ');
$resultmodels = mysql_query("select id, name from model where groupbrand_id='$grpbrnd' and status='ACTIVE' order by name");
while(($rowmodels=mysql_fetch_row($resultmodels))) {
	$opts[$rowmodels[0]] = $rowmodels[1];
	if($rowmodels[0] == $rowstatusentry[1])
		$selected = $rowmodels[0];
}
$s->loadArray($opts, $selected);
$editstatusentry->addElement($s);
$editstatusentry->addElement('text', 'newmodel', 'Model Listede Yok:');
$s2 =& $editstatusentry->createElement('select','pvid','Pardus Versiyonunu Seçiniz: ');
$resultPVs = mysql_query("select * from pardus_version order by pv_text");
while(($rowPVs=mysql_fetch_row($resultPVs))) {
	$opts2[$rowPVs[0]] = $rowPVs[1];
	if($rowPVs[0] == $rowstatusentry[2])
		$selected = $rowPVs[0];
}
$s2->loadArray($opts2, $selected);
$editstatusentry->addElement($s2);
$s3 =& $editstatusentry->createElement('select','statusid','Durum: ');
$resultstatus = mysql_query("select id, status_name from status order by status_name");
while(($rowstatus=mysql_fetch_row($resultstatus))) {
	$opts3[$rowstatus[0]] = $rowstatus[1];
	if($rowstatus[0] == $rowstatusentry[3])
		$selected = $rowstatus[0];
}
$s3->loadArray($opts3, $selected);
$editstatusentry->addElement($s3);
$ta = & $editstatusentry->createElement('textarea'); // textarea`ya value`yu başka türlü ekleyemedim
$ta->setName('statusdesc');
$ta->setLabel('Açıklama: ');
$ta->setValue($rowstatusentry[4]);
$editstatusentry->addElement($ta);
$s4 =& $editstatusentry->createElement('select','status','Gösterim: ');
$opts4['ACTIVE'] = 'AKTİF';
$opts4['PASSIVE'] = 'PASİF';
if($rowstatusentry[6] == 'ACTIVE')
	$selected = 'ACTIVE';
else
	$selected = 'PASSIVE';
$s4->loadArray($opts4, $selected);
$editstatusentry->addElement($s4);
$editstatusentry->addElement('submit', 'btnSave', 'KAYDET');
$editstatusentry->display();
?>
