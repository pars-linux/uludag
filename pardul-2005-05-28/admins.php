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
	echo "Yönetici tanımlamaları için yetkiniz yok.";
	exit;
}
$resultAdmins = mysql_query("select * from user order by rname");
ListAdmins($resultAdmins);
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
Sisteme yeni yönetici eklemek için <a href="?action=addadmin">tıklayınız</a>.
</td>
</tr>
</table>
