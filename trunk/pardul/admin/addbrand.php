<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
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
?>
<form action="?" name="addbrand">
<input type="hidden" name="action" value="addbrand">
<input type="hidden" name="formsubmitted" value="true">
<input type="hidden" name="newbrand" value="false">
<input type="hidden" name="grpid" value="<?echo $grpid;?>">
<table>
	<tr>
		<td>
			Eklemek istediğiniz markaları seçiniz:
		</td>
		<td>
			<select name="brandid[]" multiple>
			<?
			$resultbrands = mysql_query("select id, name from brand order by name");
			while(($rowbrands=mysql_fetch_row($resultbrands))) {
				if(!IsBrandGroup($rowbrands[0], $grpid))
					echo "<option value='$rowbrands[0]'>$rowbrands[1]</option>\n";
			}
			?>
			</select>
		</td>
		<td>
			<input type="submit" value="EKLE">
		</td>
	<tr>
	</tr>
	<tr>
		<td>
		Eklemek istediğiniz marka listede yok ise<br>marka ismini yazıp "Yeni Marka" butonunu tıklayınız.
		</td>
		<td>
			<input type="text" name="brandname">
		</td>
		<td>
			<input type="button" value="Yeni Marka" onClick="if(!document.addbrand.brandname.value.length){alert('Marka adı boş olamaz.');return false;}document.addbrand.newbrand.value=true;document.addbrand.submit();">
		</td>
	</tr>
</table>
</form>
