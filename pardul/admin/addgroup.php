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
	echo "Grup ekleme işlemi için yetkiniz yok.";
	exit;
}
if($formsubmitted) {
	mysql_query("INSERT INTO `group` ( `id` , `name` , `managed_by` ) VALUES ('', '$grpname', '$grpmanager')");
	require("groups.php");
	exit();
}
?>
<form action="?" name="addgroup">
<input type="hidden" name="action" value="addgroup">
<input type="hidden" name="formsubmitted" value="true">
<table>
	<tr>
		<td>
			Grup İsmi:
		</td>
		<td>
			<input type="text" name="grpname">
		</td>
		<tr>
	</tr>
	<tr>
		<td>
			Grup Yetkilisi:
		</td>
		<td>
			<select name="grpmanager">
			<?
			$resultadmins = mysql_query("select u.id, u.rname from user u, role r where u.role_id=r.id and r.rolename='sub_admin'");
			while(($rowadmins = mysql_fetch_row($resultadmins)))
				echo "<option value='$rowadmins[0]'>$rowadmins[1]</option>\n";
			?>
			</select>
		</td>
	</tr>
	<tr>
		<td colspan="2" align="center">
			<input type="submit" value="EKLE" onClick="if(!document.addgroup.grpname.value.length){alert('Grup adı boş olamaz.');return false;}">
		</td>
	</tr>
</table>
</form>
