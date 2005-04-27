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
	echo "Grup silme işlemi için yetkiniz yok.";
	exit;
}
$i = 0;
$result_grp_brnd = mysql_query("select id from group_brand where group_id='$grpid'");
while(($row_grp_brnd = mysql_fetch_row($result_grp_brnd)))
	$grp_brnds[$i++] = $row_grp_brnd[0];
$num_grp_brnds = $i;
$j = 0;
for($i=0; $i<$num_grp_brnds; $i++) {
	$result_models = mysql_query("select id from model where groupbrand_id='$grp_brnds[$i]'");
	while(($row_models = mysql_fetch_row($result_models)))
		$models[$j++] = $row_models[0];
}
$num_models = $j;
$j = 0;
for($i=0; $i<$num_models; $i++) {
	$result_model_pv_statuses = mysql_query("select id from model_pv_status where model_id='$models[$i]'");
	while(($row_model_pv_statuses = mysql_fetch_row($result_model_pv_statuses)))
		$model_pv_statuses[$j++] = $row_model_pv_statuses[0];
}
$num_model_pv_statuses = $j;
$j = 0;
for($i=0; $i<$num_model_pv_statuses; $i++) {
	$result_comments = mysql_query("select id from comment where mpvs_id='$model_pv_statuses[$i]'");
	while(($row_comments = mysql_fetch_row($result_comments)))
		$comments[$j++] = $row_comments[0];
}
$num_comments = $j;
if($approved != true) {
	echo "Silinecek gruba ait bilgi:<br>\n";
	PrintGroup($grpid);
	echo "<br><br> Bu grupla ilgli grup-marka ilişkileri:<br>\n";
	for($i=0; $i<$num_grp_brnds; $i++)
		PrintGroupBrand($grp_brnds[$i]);
	echo "<br><br> Bu grup-marka ilişkileriyle ilgli modeller:<br>\n";
	for($i=0; $i<$num_models; $i++)
		PrintModel($models[$i]);
	echo "<br><br> Bu modellerle ilgli durum bilgileri:<br>\n";
	for($i=0; $i<$num_model_pv_statuses; $i++)
		PrintModelPVStatus($model_pv_statuses[$i]);
	echo "<br><br> Bu durum bilgileriyle ilgli yorumlar:<br>\n";
	for($i=0; $i<$num_comments; $i++)
		PrintComment($comments[$i]);
	echo "
	 	<br>
     	<br>
	     <a href=\"?action=groups\">[GERİ]</a>&nbsp;&nbsp;&nbsp;<a href=\"?action=delgroup&grpid=$grpid&approved=true\">[SİL]</a>
	 	";
}
else {
	mysql_query("delete from pardul.group where id='$grpid'");
	for($i=0; $i<$num_grp_brnds; $i++)
		mysql_query("delete from group_brand where id='$grp_brnds[$i]'");
	for($i=0; $i<$num_models; $i++)
		mysql_query("delete from model where id='$models[$i]'");
	for($i=0; $i<$num_model_pv_statuses; $i++)
		mysql_query("delete from model_pv_status where id='$model_pv_statuses[$i]'");
	for($i=0; $i<$num_comments; $i++)
		mysql_query("delete from comment where id='$comments[$i]'");
	mysql_query("optimize table pardul.group");
	mysql_query("optimize table group_brand");
	mysql_query("optimize table model");
	mysql_query("optimize table model_pv_status");
	mysql_query("optimize table comment");
	require("groups.php");
}
?>
