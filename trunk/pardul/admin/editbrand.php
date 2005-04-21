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
	$brandName = GetBrandName($brandid);
	echo "<b>$brandName</b> markasını düzenlme işlemi için yetkiniz yok.";
	exit;
}
if($formsubmitted) {
	if(IsBrand($brandname))
		echo "Sistemde <b>$brandname</b> markası zaten var.<br>";
	else
		mysql_query("update brand set name='$brandname' where `id`='$brandid'");
	require("brands.php");
	exit();
}
$resultBrand = mysql_query("select name from brand where id = '$brandid'");
$rowBrand = mysql_fetch_row($resultBrand);
?>
<form action="?" name="editbrand">
<input type="hidden" name="action" value="editbrand">
<input type="hidden" name="formsubmitted" value="true">
<input type="hidden" name="brandid" value="<?echo $brandid;?>">
<input type="hidden" name="grpid" value="<?echo $grpid;?>">
<table>
	<tr>
		<td>
			Marka:
		</td>
		<td>
			<input type="text" name="brandname" value="<?echo $rowBrand[0];?>">
		</td>
		<tr>
	</tr>
	<tr>
		<td colspan="2" align="center">
			<input type="submit" value="KAYDET" onClick="if(!document.editbrand.brandname.value.length){alert('Marka boş olamaz.');return false;}">
		</td>
	</tr>
</table>
</form>
