<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/


include("globals.inc.php");
include("globals_admin.inc.php");
//------------------------------------------------------------
function GetRoleName($roleid) {
	$result = mysql_query("select rolename from role where id='$roleid'");
	$row = mysql_fetch_row($result);
	return $row[0];
}
//------------------------------------------------------------
function IsManaggedBy($userid, $groupid) {
	$result = mysql_query("select count(*) from pardul.groups where id='$groupid' and managged_by='$userid'");
	$row = mysql_fetch_row($result);
	return $row[0];
}
//------------------------------------------------------------
?>
