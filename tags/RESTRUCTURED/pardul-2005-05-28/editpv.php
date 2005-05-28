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
	echo "Pardus versiyonu düzenlme işlemi için yetkiniz yok.";
	exit;
}
if($formsubmitted) {
	if(IsPV($pvname) && IsPV($pvname) != $pvid)
		echo "Sistemde <b>$pvname</b> Pardus versiyonu zaten var.<br>";
	else
		mysql_query("update pardus_version set pv_text='$pvname' where `id`='$pvid'");
	require("pv_param.php");
	exit();
}
$resultPV = mysql_query("select pv_text from pardus_version where id = '$pvid'");
$rowPV = mysql_fetch_row($resultPV);
$editPV = new HTML_QuickForm('editPV', 'get', '');
$editPV->addElement('hidden', 'action', 'editpv');
$editPV->addElement('hidden', 'formsubmitted', 'true');
$editPV->addElement('hidden', 'pvid', $pvid);
$editPV->addElement('text', 'pvname', 'Pardus Versiyonu: ', array('value'=>$rowPV[0]));
$editPV->addElement('submit', 'btnSave', 'KAYDET');
$editPV->display();
?>
