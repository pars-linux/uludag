<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
  
  
  -- groups.php
  kök kategorileri listeler.
  
*/

?>

<table border="1">
<?
$roleName = GetRoleName($roleid);
$resultGrps = mysql_query("select id, name from pardul.group order by name");
ListGroups($resultGrps, $roleName);
?>
<?if($roleName == "admin") {?>
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
