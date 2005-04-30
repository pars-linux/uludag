<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.


  -- brands.php
  $grpid kök kategorisindeki markaları listeler.
  
*/

?>

<table border="1">
<?
$resultBrands = mysql_query("select brand.id, brand.name from brand, group_brand where brand.id = group_brand.brand_id and group_brand.group_id='$grpid' order by brand.name");
ListBrands($resultBrands, GetRoleName($roleid));
if(GetRoleName($roleid) == "admin" || IsManaggedBy($userid, $grpid)) {?>
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
	<b><?echo GetGroupName($grpid);?></b> grubuna yeni marka eklemek için <a href="?action=addbrand&grpid=<?echo $grpid;?>">tıklayınız</a>.
	</td>
	</tr>
<?}?>
</table>
