<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
  
  -- addbrand.php
  marka ekleme işlemini yapar. form verileri index.php üzerinden yine
  buraya yönlendirilir. $formsubmitted set edilmişse insert işlemi yapılır
  edilmemişse kök kategori ekleme formu ekrana basılır.
  
*/



if(GetRoleName($roleid) != "admin" && !IsManaggedBy($userid, $grpid)) {
	$grpName = GetGroupName($grpid);
	echo "<b>$grpName</b> grubuna marka ekleme işlemi için yetkiniz yok.";
	exit;
}
$grpName = GetGroupName($grpid);
if($formsubmitted) {
	if($newbrand == "true") {
		$brandname = strtoupper($brandname);
		if(($brandid=IsBrand($brandname)))
			echo "Sistemde <b>$brandname</b> markası zaten var.<br>";
		else {
			mysql_query("insert into brand values('', '$brandname')");
			echo "Sisteme <b>$brandname</b> markası eklendi.<br>";
			$brandid = mysql_insert_id();
		}
		if(IsBrandGroup($brandid, $grpid))
			echo "<b>$grpName</b> grubu ile <b>$brandname</b> markası zaten ilişkili.<br>";
		else {
			mysql_query("INSERT INTO `group_brand` VALUES ('', '$grpid', '$brandid')");
			echo "<b>$grpName</b> grubu ile <b>$brandname</b> markası ilişkilendirildi.<br>";
		}
	}
	else {
		for($i=0; $i<count($brandid); $i++) {
			$brandname = GetBrandName($brandid[$i]);
			if(IsBrandGroup($brandid[$i], $grpid))
				echo "<b>$grpName</b> grubu ile <b>$brandname</b> markası zaten ilişkili.<br>";
			else {
				mysql_query("INSERT INTO `group_brand` VALUES ('', '$grpid', '$brandid[$i]')");
				echo "<b>$grpName</b> grubu ile <b>$brandname</b> markası ilişkilendirildi.<br>";
			}
		}
	}
	require("brands.php");
	exit();
}
$addbrand = new HTML_QuickForm('addbrand', 'get', '');
$addbrand->addElement('hidden', 'action', 'addbrand');
$addbrand->addElement('hidden', 'formsubmitted', 'true');
$addbrand->addElement('hidden', 'newbrand', 'false');
$addbrand->addElement('hidden', 'grpid', $grpid);
$s =& $addbrand->createElement('select','brandid','Eklemek istediğiniz markaları seçiniz: ');
$s->setMultiple(true);
$resultbrands = mysql_query("select id, name from brand order by name");
while(($rowbrands=mysql_fetch_row($resultbrands))) {
	if(!IsBrandGroup($rowbrands[0], $grpid))
		$opts[$rowbrands[0]] = $rowbrands[1];
}
$s->loadArray($opts, $selected);
$addbrand->addElement($s);
$addbrand->addElement('submit', 'btnSave', 'KAYDET');
$addbrand->display();
$addbrand2 = new HTML_QuickForm('addbrand2', 'get', '');
$addbrand2->addElement('hidden', 'action', 'addbrand');
$addbrand2->addElement('hidden', 'formsubmitted', 'true');
$addbrand2->addElement('hidden', 'newbrand', 'true');
$addbrand2->addElement('hidden', 'grpid', $grpid);
$addbrand2->addElement('text', 'brandname', 'Eklemek istediğiniz marka listede yok ise marka<br>ismini yazıp "Yeni Marka" butonunu tıklayınız.');
$addbrand2->addElement('submit', 'btnSave', 'YENİ MARKA');
$addbrand2->display();
?>
