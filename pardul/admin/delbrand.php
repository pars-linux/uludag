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
	echo "<b>$grpName</b> grubundan marka silme işlemi için yetkiniz yok.";
	exit;
}
mysql_query("delete from group_brand where group_id='$grpid' and brand_id='$brandid'");
mysql_query("optimize table brand");
$grpName = GetGroupName($grpid);
$brandName = GetBrandName($brandid);
echo "<b>$grpName</b> grubu ile <b>$brandName</b> markası arasındaki ilişki silindi.";
require("brands.php");
?>
