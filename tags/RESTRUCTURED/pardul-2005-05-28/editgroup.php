<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
  
  -- editgroup.php
  kök kategori düzenleme işlemini yapar. form verileri index.php üzerinden yine
  buraya yönlendirilir. $formsubmitted set edilmişse insert işlemi yapılır
  edilmemişse kök kategori düzenleme formu ekrana basılır.
  
*/

if(GetRoleName($roleid) != "admin") {
	echo "Grup düzenleme işlemi için yetkiniz yok.";
	exit;
}
if($formsubmitted) {
	if(IsGroup($grpname) && IsGroup($grpname) != $grpid)
		echo "Sistemde <b>$grpname</b> grubu zaten var.<br>";
	else
		mysql_query("update `group` set `name`='$grpname', `managed_by`='$grpmanager' where `id`='$grpid'");
	require("groups.php");
	exit();
}
$resultGrp = mysql_query("select pardul.group.name, pardul.group.managed_by from pardul.group where pardul.group.id = '$grpid'");
$rowGrp = mysql_fetch_row($resultGrp);
$editgroup = new HTML_QuickForm('editgroup', 'get', '');
$editgroup->addElement('hidden', 'action', 'editgroup');
$editgroup->addElement('hidden', 'formsubmitted', 'true');
$editgroup->addElement('hidden', 'grpid', $grpid);
$editgroup->addElement('text', 'grpname', 'Grup İsmi: ', array('value'=>$rowGrp[0]));
$s =& $editgroup->createElement('select','grpmanager','Grup Yöneticisi: ');
$resultadmins = mysql_query("select u.id, u.rname from user u, role r where u.role_id=r.id and r.rolename='sub_admin' order by u.rname");
while(($rowadmins = mysql_fetch_row($resultadmins))) {
	$opts[$rowadmins[0]] = $rowadmins[1];
	if($rowadmins[0] == $rowGrp[1])
		$selected = $rowadmins[0];
}
$s->loadArray($opts, $selected);
$editgroup->addElement($s);
$editgroup->addElement('submit', 'btnSave', 'KAYDET');
$editgroup->display();
?>
