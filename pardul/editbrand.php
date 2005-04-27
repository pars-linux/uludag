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
	echo "Marka düzenlme işlemi için yetkiniz yok.";
	exit;
}
if($formsubmitted) {
	if(IsBrand($brandname) && IsBrand($brandname) != $brandid)
		echo "Sistemde <b>$brandname</b> markası zaten var.<br>";
	else
		mysql_query("update brand set name='$brandname' where `id`='$brandid'");
	require("brands.php");
	exit();
}
$resultBrand = mysql_query("select name from brand where id = '$brandid'");
$rowBrand = mysql_fetch_row($resultBrand);
$editbrand = new HTML_QuickForm('editbrand', 'get', '');
$editbrand->addElement('hidden', 'action', 'editbrand');
$editbrand->addElement('hidden', 'formsubmitted', 'true');
$editbrand->addElement('hidden', 'brandid', $brandid);
$editbrand->addElement('hidden', 'grpid', $grpid);
$editbrand->addElement('text', 'brandname', 'Marka: ', array('value'=>$rowBrand[0]));
$editbrand->addElement('submit', 'btnSave', 'KAYDET');
$editbrand->display();
?>
