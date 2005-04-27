<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

$grpbrnd = GetGrpBrnd($modelid);
$grpid = GroupGrpBrnd($grpbrnd);
$brandid = BrandGrpBrnd($grpbrnd);
if(GetRoleName($roleid) != "admin" && !IsManaggedBy($userid, $grpid)) {
	echo "olmaz.<br>";
	exit;
}
mysql_query("update comment set status='ACTIVE' where id='$commentid'");
require("statusentries.php");
exit();
?>
