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
$resultstatus = mysql_query("select * from status");
Liststatus($resultstatus);
?>
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
	Yeni durum eklemek için <a href="?action=addstatus">tıklayınız</a>.
	</td>
	</tr>
</table>
