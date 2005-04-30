<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
  
  -- addgroup.php
  kök kategori ekleme işlemini yapar. form verileri index.php üzerinden yine
  buraya yönlendirilir. $formsubmitted set edilmişse insert işlemi yapılır
  edilmemişse kök kategori ekleme formu ekrana basılır.
  
*/



if(GetRoleName($roleid) != "admin") {
	echo "Grup ekleme işlemi için yetkiniz yok.";
	exit;
}
if($formsubmitted) {
	if(IsGroup($grpname))
		echo "Sistemde <b>$grpname</b> grubu zaten var.<br>";
	else
		mysql_query("INSERT INTO `group` ( `id` , `name` , `managed_by` ) VALUES ('', '$grpname', '$grpmanager')");
	require("groups.php");
	exit();
}
$addgroup = new HTML_QuickForm('addgroup', 'get', '');
$addgroup->addElement('hidden', 'action', 'addgroup');
$addgroup->addElement('hidden', 'formsubmitted', 'true');
$addgroup->addElement('text', 'grpname', 'Grup İsmi: ');
$s =& $addgroup->createElement('select','grpmanager','Grup Yöneticisi: ');
$resultadmins = mysql_query("select u.id, u.rname from user u, role r where u.role_id=r.id and r.rolename='sub_admin'");
while(($rowadmins = mysql_fetch_row($resultadmins)))
	$opts[$rowadmins[0]] = $rowadmins[1];
$s->loadArray($opts);
$addgroup->addElement($s);
$addgroup->addElement('submit', 'btnSave', 'KAYDET');
$addgroup->display();
?>
