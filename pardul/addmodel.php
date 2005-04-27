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
	echo "Model ekleme işlemi için yetkiniz yok.";
	exit;
}
$groupname = GetGroupName($grpid);
$brandname = GetBrandName($brandid);
$grpbrnd = IsBrandGroup($brandid, $grpid);
if($formsubmitted) {
	if(IsModelGroupBrand($modelname, $grpid, $brandid))
		echo "<b>$groupname</b> grubundaki <b>$brandname</b> markasında <b>$modelname</b> modeli zaten var.<br>";
	else
		mysql_query("INSERT INTO model ( id , name , groupbrand_id, status ) VALUES ('', '$modelname', '$grpbrnd', 'ACTIVE')");
	$subaction = 'model_param';	
	require("model_param.php");
	exit();
}
$addmodel = new HTML_QuickForm('addmodel', 'get', '');
$addmodel->addElement('hidden', 'action', 'addmodel');
$addmodel->addElement('hidden', 'grpid', $grpid);
$addmodel->addElement('hidden', 'brandid', $brandid);
$addmodel->addElement('hidden', 'formsubmitted', 'true');
$addmodel->addElement('text', 'modelname', 'Model: ');
$addmodel->addElement('submit', 'btnSave', 'KAYDET');
$addmodel->display();
?>
