<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/
if(GetRoleName($roleid) != "admin") {
	echo "Durum düzenlme işlemi için yetkiniz yok.";
	exit;
}
if($formsubmitted) {
	if(IsStatus($statusname) && IsStatus($statusname) != $statusid)
		echo "Sistemde <b>$statusname</b> durumu zaten var.<br>";
	else
		mysql_query("update status set status_name='$statusname', description='$statusdesc' where `id`='$statusid'");
	require("status_param.php");
	exit();
}
$resultstatus = mysql_query("select status_name, description from status where id = '$statusid'");
$rowstatus = mysql_fetch_row($resultstatus);
$editstatus = new HTML_QuickForm('edittatus', 'get', '');
$editstatus->addElement('hidden', 'action', 'editstatus');
$editstatus->addElement('hidden', 'formsubmitted', 'true');
$editstatus->addElement('hidden', 'statusid', $statusid);
$editstatus->addElement('text', 'statusname', 'Durum: ', array('value'=>$rowstatus[0]));
$ta = & $editstatus->createElement('textarea'); // textarea`ya value`yu başka türlü ekleyemedim
$ta->setName('statusdesc');
$ta->setLabel('Açıklama: ');
$ta->setValue($rowstatus[1]);
$editstatus->addElement($ta);
$editstatus->addElement('submit', 'btnSave', 'KAYDET');
$editstatus->display();
?>
