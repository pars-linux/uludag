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
	echo "Grup düzenleme işlemi için yetkiniz yok.";
	exit;
}
if($formsubmitted)
	mysql_query("update `group` set `name`='$grpname', `managed_by`='$grpmanager' where `id`='$grpid'");
$resultGrp = mysql_query("select pardul.group.name, pardul.group.managed_by from pardul.group where pardul.group.id = '$grpid'");
$rowGrp = mysql_fetch_row($resultGrp);
?>
<form action="?" name="editgroup">
<input type="hidden" name="action" value="editgroup">
<input type="hidden" name="formsubmitted" value="true">
<input type="hidden" name="grpid" value="<?echo $grpid;?>">
<table>
	<tr>
		<td>
			Grup İsmi:
		</td>
		<td>
			<input type="text" name="grpname" value="<?echo $rowGrp[0];?>">
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
			while(($rowadmins = mysql_fetch_row($resultadmins))) {
				if($rowadmins[0] == $rowGrp[1])
					echo "<option value='$rowadmins[0]' selected>$rowadmins[1]</option>\n";
				else
					echo "<option value='$rowadmins[0]'>$rowadmins[1]</option>\n";
			}
			?>
			</select>
		</td>
	</tr>
	<tr>
		<td colspan="2" align="center">
			<input type="submit" value="KAYDET" onClick="if(!document.editgroup.grpname.value.length){alert('Grup adı boş olamaz.');return false;}">
		</td>
	</tr>
</table>
</form>
