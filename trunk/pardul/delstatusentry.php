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
	echo "olmaz..";
	exit;
}
$result_comments = mysql_query("select id from comment where mpvs_id='$statusentryid'");
$j = 0;
while(($row_comments = mysql_fetch_row($result_comments)))
	$comments[$j++] = $row_comments[0];
$num_comments = $j;
if($approved != true) {
	echo "Silinecek durum bilgisi:<br>\n";
	PrintModelPVStatus($statusentryid);
	echo "<br><br> Bu durum bilgisiyle ilgli yorumlar:<br>\n";
	for($i=0; $i<$num_comments; $i++)
		PrintComment($comments[$i]);
	echo "
	 	<br>
     	<br>
	     <a href=\"?action=statusentries&grpid=$grpid&brandid=$brandid\">[GERİ]</a>&nbsp;&nbsp;&nbsp;<a href=\"?action=delstatusentry&grpid=$grpid&brandid=$brandid&statusentryid=$statusentryid&approved=true\">[SİL]</a>
	 	";
}
else {
	mysql_query("delete from model_pv_status where id='$statusentryid'");
	for($i=0; $i<$num_comments; $i++)
		mysql_query("delete from comment where id='$comments[$i]'");
	mysql_query("optimize table model_pv_status");
	mysql_query("optimize table comment");
	require("statusentries.php");
	exit();
}
?>
