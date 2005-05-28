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
	echo "Pardus versiyonu ekleme işlemi için yetkiniz yok.";
	exit;
}
if($formsubmitted) {
	if(IsPV($pvname))
		echo "Sistemde <b>$pvname</b> Pardus versiyonu zaten var.<br>";
	else
		mysql_query("INSERT INTO pardus_version ( id , pv_text ) VALUES ('', '$pvname')");
	require("pv_param.php");
	exit();
}
$addPV = new HTML_QuickForm('addPV', 'get', '');
$addPV->addElement('hidden', 'action', 'addpv');
$addPV->addElement('hidden', 'formsubmitted', 'true');
$addPV->addElement('text', 'pvname', 'Pardus Versiyonu: ');
$addPV->addElement('submit', 'btnSave', 'KAYDET');
$addPV->display();
?>
