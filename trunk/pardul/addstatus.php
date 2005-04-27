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
	echo "Durum ekleme işlemi için yetkiniz yok.";
	exit;
}
if($formsubmitted) {
	if(IsPV($pvname))
		echo "Sistemde <b>$pvname</b> Pardus versiyonu zaten var.<br>";
	else
		mysql_query("INSERT INTO status ( id , status_name, description ) VALUES ('', '$statusname', '$statusdesc')");
	require("status_param.php");
	exit();
}
$addstatus = new HTML_QuickForm('addstatus', 'get', '');
$addstatus->addElement('hidden', 'action', 'addstatus');
$addstatus->addElement('hidden', 'formsubmitted', 'true');
$addstatus->addElement('text', 'statusname', 'Durum: ');
$addstatus->addElement('textarea', 'statusdesc', 'Açıklama: ');
$addstatus->addElement('submit', 'btnSave', 'KAYDET');
$addstatus->display();
?>
