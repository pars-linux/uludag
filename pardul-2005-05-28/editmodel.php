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
	echo "Model düzenleme işlemi için yetkiniz yok.";
	exit;
}
$grpbrnd = GetGrpBrnd($modelid);
$grpid = GroupGrpBrnd($grpbrnd);
$brandid = BrandGrpBrnd($grpbrnd);
$groupname = GetGroupName($newgrpid);
$brandname = GetBrandName($newbrandid);
$newgrpbrnd = IsBrandGroup($newbrandid, $newgrpid);
if($formsubmitted) {
	if(!$newgrpbrnd) {
		echo "<b>$groupname</b> grubu ve <b>$brandname</b> markası ilişkilendirilmemiş.";
	}
	else {
		if(IsModelGroupBrand($modelname, $newgrpid, $newbrandid) && IsModelGroupBrand($modelname, $newgrpid, $newbrandid) != $modelid)
			echo "<b>$groupname</b> grubundaki <b>$brandname</b> markasında <b>$modelname</b> modeli zaten var.<br>";
		else
			mysql_query("update model set name='$modelname', groupbrand_id='$newgrpbrnd', status='$status' where `id`='$modelid'");
		$subaction = 'model_param';	
		require("model_param.php");
		exit();
	}
}
$resultModel = mysql_query("select name, status from model where id = '$modelid'");
$rowModel = mysql_fetch_row($resultModel);
$editmodel = new HTML_QuickForm('editmodel', 'get', '');
$editmodel->addElement('hidden', 'action', 'editmodel');
$editmodel->addElement('hidden', 'formsubmitted', 'true');
$editmodel->addElement('hidden', 'modelid', $modelid);
$editmodel->addElement('text', 'modelname', 'Model: ', array('value'=>$rowModel[0]));
$s =& $editmodel->createElement('select','newgrpid','Grup: ');
$resultgrp = mysql_query("select * from pardul.group");
while(($rowgrp = mysql_fetch_row($resultgrp))) {
	$opts[$rowgrp[0]] = $rowgrp[1];
	if($rowgrp[0] == $grpid)
		$selected = $rowgrp[0];
}
$s->loadArray($opts, $selected);
$editmodel->addElement($s);
$s2 =& $editmodel->createElement('select','newbrandid','Marka: ');
$resultbrand = mysql_query("select * from brand");
while(($rowbrand = mysql_fetch_row($resultbrand))) {
	$opts2[$rowbrand[0]] = $rowbrand[1];
	if($rowbrand[0] == $brandid)
		$selected = $rowbrand[0];
}
$s2->loadArray($opts2, $selected);
$editmodel->addElement($s2);

$s4 =& $editmodel->createElement('select','status','Gösterim: ');
$opts4['ACTIVE'] = 'AKTİF';
$opts4['PASSIVE'] = 'PASİF';
if($rowModel[1] == 'ACTIVE')
	$selected = 'ACTIVE';
else
	$selected = 'PASSIVE';
$s4->loadArray($opts4, $selected);
$editmodel->addElement($s4);


$editmodel->addElement('submit', 'btnSave', 'KAYDET');
$editmodel->display();
?>
