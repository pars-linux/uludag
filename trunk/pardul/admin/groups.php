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
$roleName = GetRoleName($roleid);
if($roleName == "admin")
	$resultGrps = mysql_query("select id, name from pardul.group");
else if($roleName == "sub_admin")
	$resultGrps = mysql_query("select id, name from pardul.group where managed_by='$userid'");
ListGroups($resultGrps, $roleName);
?>
<?if($roleid == "1") {?>
	<tr>
	<td colspan="2">
	<br>
	</td>
	</tr>
	<tr>
	<td colspan="2">
	<br>
	</td>
	</tr>
	<tr>
	<td colspan="2">
	Sisteme yeni grup eklemek için <a href="?action=addgroup">tıklayınız</a>.
	</td>
	</tr>
<?}?>
</table>
