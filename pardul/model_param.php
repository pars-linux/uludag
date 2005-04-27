<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/
?>
<table border="1">
<?
if(GetRoleName($roleid) != "admin") {
	echo "Parametre tanımlamaları için yetkiniz yok.";
	exit;
}
if($formsubmitted) {
	$brandname = GetBrandName($brandid);
	$groupname = GetGroupName($grpid);
	$grpbrnd = IsBrandGroup($brandid, $grpid);
	if(!$grpbrnd) {
		echo "<b>$groupname</b> grubu ve <b>$brandname</b> markası ilişkilendirilmemiş.";
	}
	else {
		$resultmodel = mysql_query("select * from model where groupbrand_id='$grpbrnd' and status='ACTIVE'");
		ListModel($resultmodel);
		echo "
		<table>
		<tr>
		<td colspan=\"2\">
		<br>
		</td>
		</tr>
		<tr>
		<td colspan=\"2\">
		<br>
		</td>
		</tr>
		<tr>
		<td colspan=\"2\">
		$groupname grubundaki $brandname markasına yeni model eklemek için <a href=\"?action=addmodel&grpid=$grpid&brandid=$brandid\">tıklayınız</a>.
		</td>
		</tr>
		</table>
		";
	}
}
else {
	$resultgroup = mysql_query("select * from pardul.group order by name");
	$resultbrand = mysql_query("select * from brand order by name");
	$modelForm = new HTML_QuickForm('model_form', 'get', '');
	$modelForm->addElement('header', 'header', 'Model listesi için grup ve marka seçiniz');
	$modelForm->addElement('hidden', 'action', 'parameters');
	$modelForm->addElement('hidden', 'subaction', 'model_param');
	$modelForm->addElement('hidden', 'formsubmitted', 'true');
	$gid =& $modelForm->createElement('select','grpid','Grup: ');
	while(($rowgroup = mysql_fetch_row($resultgroup)))
		$opts[$rowgroup[0]] = $rowgroup[1];
	$gid->loadArray($opts);
	$modelForm->addElement($gid);
	$bid =& $modelForm->createElement('select','brandid','Marka: ');
	while(($rowbrand = mysql_fetch_row($resultbrand)))
		$opts2[$rowbrand[0]] = $rowbrand[1];
	$bid->loadArray($opts2);
	$modelForm->addElement($bid);
	$modelForm->addElement('submit', 'btnShow', 'GÖSTER');
	$modelForm->display();
}
?>
