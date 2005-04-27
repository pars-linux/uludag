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

//------------------------------------------------------------
function ListAdmins($resultadmins) {
	$i = 0;
	while(($rowadmins = mysql_fetch_row($resultadmins))) {
		$i++;
		if($i%2 == 1)
			echo "<tr>\n";
		echo "<td>$rowadmins[1]";
		echo "&nbsp;&nbsp;<a href=\"?action=editadmin&adminid=$rowadmins[0]\">[Düzenle]</a>\n";
		echo "</td>\n";
		if($i%2 == 0)
			echo "</tr>\n";
	}
}
//------------------------------------------------------------
function GetRoleName($roleid) {
	$result = mysql_query("select rolename from role where id='$roleid'");
	$row = mysql_fetch_row($result);
	return $row[0];
}
//------------------------------------------------------------
function IsManaggedBy($userid, $groupid) {
	$result = mysql_query("select count(*) from pardul.group where id='$groupid' and managed_by='$userid'");
	$row = mysql_fetch_row($result);
	return $row[0];
}
//------------------------------------------------------------
function ListPVs($resultPVs) {
	$i = 0;
	while(($rowPVs = mysql_fetch_row($resultPVs))) {
		$i++;
		if($i%2 == 1)
			echo "<tr>\n";
		echo "<td>$rowPVs[1]";
		echo "&nbsp;&nbsp;<a href=\"?action=editpv&pvid=$rowPVs[0]\">[Düzenle]</a>\n";
		echo "&nbsp;<a href=\"?action=delpv&pvid=$rowPVs[0]\">[Sil]</a>";
		echo "</td>\n";
		if($i%2 == 0)
			echo "</tr>\n";
	}
}
//------------------------------------------------------------
function ListStatus($resultstatus) {
	$i = 0;
	while(($rowstatus = mysql_fetch_row($resultstatus))) {
		$i++;
		if($i%2 == 1)
			echo "<tr>\n";
		echo "<td>$rowstatus[1]";
		echo "&nbsp;&nbsp;<a href=\"?action=editstatus&statusid=$rowstatus[0]\">[Düzenle]</a>\n";
		echo "&nbsp;<a href=\"?action=delstatus&statusid=$rowstatus[0]\">[Sil]</a>";
		echo "</td>\n";
		if($i%2 == 0)
			echo "</tr>\n";
	}
}
//------------------------------------------------------------
function ListModel($resultmodel) {
	$i = 0;
	while(($rowmodel = mysql_fetch_row($resultmodel))) {
		$i++;
		if($i%2 == 1)
			echo "<tr>\n";
		echo "<td>$rowmodel[1]";
		echo "&nbsp;&nbsp;<a href=\"?action=editmodel&modelid=$rowmodel[0]\">[Düzenle]</a>\n";
		echo "&nbsp;<a href=\"?action=delmodel&modelid=$rowmodel[0]\">[Sil]</a>";
		echo "</td>\n";
		if($i%2 == 0)
			echo "</tr>\n";
	}
}
//------------------------------------------------------------
function MYSQLConnect() {
	global $MYSQLHOST, $MYSQLUSER, $MYSQLPASSWORD, $DATABASENAME;
	$link = mysql_connect($MYSQLHOST, $MYSQLUSER, $MYSQLPASSWORD);
	mysql_selectdb($DATABASENAME, $link);
	return $link;
}
//------------------------------------------------------------
function ListGroups($resultGrps, $printFor) {
	$i = 0;
	while(($rowGrps = mysql_fetch_row($resultGrps))) {
		$i++;
		if($i%2 == 1)
			echo "<tr>\n";
		echo "<td><a href=\"?action=brands&grpid=$rowGrps[0]\">$rowGrps[1]</a>";
		if($printFor == "admin") {
			echo "&nbsp;&nbsp;<a href=\"?action=editgroup&grpid=$rowGrps[0]\">[Düzenle]</a>\n";
			echo "&nbsp;<a href=\"?action=delgroup&grpid=$rowGrps[0]\">[Sil]</a>";
		}
		echo "</td>\n";
		if($i%2 == 0)
			echo "</tr>\n";
	}
}
//------------------------------------------------------------
function PrintColoumnsAsRow($result) { // kullanilmiyor
	$num_fields = mysql_num_fields($result);
	$row = $rowGrpBrnd = mysql_fetch_row($result);
	echo "<tr>\n";
	for($i=0; $i<$num_fields; $i++)
		echo "
			<td>
				$row[$i]
			</td>
		";
	echo "</tr>\n</table>\n";
}
//------------------------------------------------------------
function PrintColoumnsAsTable($col1, $result) {
	$num_fields = mysql_num_fields($result);
	$row = $rowGrpBrnd = mysql_fetch_row($result);
	echo "<table border=\"1\">\n";
	for($i=0; $i<$num_fields; $i++)
		echo "
			<tr>
				<td>
					$col1[$i]: 
				</td>
				<td>
					$row[$i]
				</td>
			</tr>
		";
	echo "</table>\n";
}
//------------------------------------------------------------
function PrintAsRowHeader($result) { // kullanilmiyor
		echo "
			<table border=\"1\">
			<tr>
			";
		for($i=0; $i<mysql_num_fields($result); $i++)
			echo "
				<td align=\"center\">
					$col1[$i]
				</td>
			";
		echo "</tr>\n";
}
//------------------------------------------------------------
function PrintGroupBrand($grpbrndid) {
	$resultGrpBrnd = mysql_query("select group_brand.id, pardul.group.name, brand.name from group_brand, pardul.group, brand where pardul.group.id = group_brand.group_id and brand.id = group_brand.brand_id and group_brand.id = '$grpbrndid'");
	$col1[0] = "Grup_Marka Sıra No";
	$col1[1] = "Grup Adı";
	$col1[2] = "Marka Adı";
	PrintColoumnsAsTable($col1, $resultGrpBrnd);
}
//------------------------------------------------------------
function PrintModel($modelid) {
	$resultmodel = mysql_query("select * from model where id = '$modelid'");
	$col1[0] = "Model Sıra No";
	$col1[1] = "Model Adı";
	$col1[2] = "Grup_Marka No";
	$col1[3] = "Gösterim Durumu";
	PrintColoumnsAsTable($col1, $resultmodel);
}
//------------------------------------------------------------
function PrintModelPVStatus($modelpvstatuseid) {
	$resultmodelpvstatus = mysql_query("select model_pv_status.id, model.name, pardus_version.pv_text, status.status_name, model_pv_status.status_text, model_pv_status.entry_date, model_pv_status.status from model_pv_status, model, pardus_version, status where model.id = model_pv_status.model_id and pardus_version.id = pv_id and status.id = status_id and model_pv_status.id = '$modelpvstatuseid'");
	$col1[0] = "Durum Sıra No";
	$col1[1] = "Model Adı";
	$col1[2] = "Pardus Versiyonu";
	$col1[3] = "Durum";
	$col1[4] = "Durum Ayrıntı";
	$col1[5] = "Giriş Tarihi";
	$col1[6] = "Gösterim Durumu";
	PrintColoumnsAsTable($col1, $resultmodelpvstatus);
}
//------------------------------------------------------------
function PrintComment($commentid) {
	$resultcomment = mysql_query("select * from comment where id='$commentid'");
	$col1[0] = "Yorum Sıra No";
	$col1[1] = "Durum Sıra No";
	$col1[2] = "Yorum";
	$col1[3] = "Gönderen E-Posta";
	$col1[4] = "Gönderen";
	$col1[5] = "Giriş Tarihi";
	$col1[6] = "Gösterim Durumu";
	PrintColoumnsAsTable($col1, $resultcomment);
}
//------------------------------------------------------------
function PrintGroup($groupid) {
	$resultgroup = mysql_query("select pardul.group.id, pardul.group.name, user.rname from pardul.group, user where pardul.group.managed_by = user.id and pardul.group.id='$groupid'");
	$col1[0] = "Grup Sıra No";
	$col1[1] = "Grup Adı";
	$col1[2] = "Sorumlu";
	PrintColoumnsAsTable($col1, $resultgroup);
}
//------------------------------------------------------------
function ListBrands($resultBrands, $printFor) {
	$i = 0;
	global $userid, $grpid;
	while(($rowBrands = mysql_fetch_row($resultBrands))) {
		$i++;
		if($i%2 == 1)
			echo "<tr>\n";
		echo "<td><a href=\"?action=statusentries&grpid=$grpid&brandid=$rowBrands[0]\">$rowBrands[1]</a>";
		if($printFor == "admin") {
			echo "&nbsp;&nbsp;<a href=\"?action=editbrand&brandid=$rowBrands[0]&grpid=$grpid\">[Düzenle]</a>\n";
			echo "&nbsp;<a href=\"?action=delbrand&brandid=$rowBrands[0]&grpid=$grpid\">[Sil]</a>";
		}
		if(IsManaggedBy($userid, $grpid))
			echo "&nbsp;<a href=\"?action=delbrand&brandid=$rowBrands[0]&grpid=$grpid\">[Sil]</a>";
		echo "</td>\n";
		if($i%2 == 0)
			echo "</tr>\n";
	}
}
//------------------------------------------------------------
function GetGroupName($grpid) {
	$resultgroup = mysql_query("select name from pardul.group where id = '$grpid'");
	$rowgroup = mysql_fetch_row($resultgroup);
	return $rowgroup[0];
}
//------------------------------------------------------------
function GetPVName($pvid) {
	$resultPV = mysql_query("select pv_text from pardus_version where id = '$pvid'");
	$rowPV = mysql_fetch_row($resultPV);
	return $rowPV[0];
}
//------------------------------------------------------------
function GetStatusName($statusid) {
	$resultstatus = mysql_query("select status_name from status where id = '$statusid'");
	$rowstatus = mysql_fetch_row($resultstatus);
	return $rowstatus[0];
}
//------------------------------------------------------------
function BrandGrpBrnd($grpbrnd) {
	$resultbrand = mysql_query("select brand_id from group_brand where id = '$grpbrnd'");
	$rowbrand = mysql_fetch_row($resultbrand);
	return $rowbrand[0];
}
//------------------------------------------------------------
function GroupGrpBrnd($grpbrnd) {
	$resultgroup = mysql_query("select group_id from group_brand where id = '$grpbrnd'");
	$rowgroup = mysql_fetch_row($resultgroup);
	return $rowgroup[0];
}
//------------------------------------------------------------
function GetGrpBrnd($modelid) {
	$resultgrpbrnd = mysql_query("select groupbrand_id from model where id = '$modelid'");
	$rowgrpbrnd = mysql_fetch_row($resultgrpbrnd);
	return $rowgrpbrnd[0];
}
//------------------------------------------------------------
function GetBrandName($brandid) {
	$resultbrand = mysql_query("select name from brand where id = '$brandid'");
	$rowbrand = mysql_fetch_row($resultbrand);
	return $rowbrand[0];
}
//------------------------------------------------------------
function GetModelName($modelid) {
	$resultmodel = mysql_query("select name from model where id = '$modelid'");
	$rowmodel = mysql_fetch_row($resultmodel);
	return $rowmodel[0];
}
//------------------------------------------------------------
function IsModelGroupBrand($modelname, $groupid, $brandid){
	$grbr = IsBrandGroup($brandid, $groupid);
	$resultmogrbr = mysql_query("select id from model where name='$modelname' and groupbrand_id='$grbr'");
	if(mysql_num_rows($resultmogrbr) == 0)
		return 0;
	$rowmogrbr = mysql_fetch_row($resultmogrbr);
	return $rowmogrbr[0];
}
//------------------------------------------------------------
function IsBrandGroup($brandid, $groupid){
	$resultgrbr = mysql_query("select id from group_brand where group_id='$groupid' and brand_id='$brandid'");
	if(mysql_num_rows($resultgrbr) == 0)
		return 0;
	$rowgrbr = mysql_fetch_row($resultgrbr);
	return $rowgrbr[0];
}
//------------------------------------------------------------
function IsModel($modelname) {
	$resultmodel = mysql_query("select id from model where name='$modelname'");
	if(mysql_num_rows($resultmodel) == 0)
		return 0;
	$rowmodel = mysql_fetch_row($resultmodel);
	return $rowmodel[0];
}
//------------------------------------------------------------
function IsPV($PVname) {
	$resultPV = mysql_query("select id from pardus_version where pv_text='$PVname'");
	if(mysql_num_rows($resultPV) == 0)
		return 0;
	$rowPV = mysql_fetch_row($resultPV);
	return $rowPV[0];
}
//------------------------------------------------------------
function IsStatus($statusname) {
	$resultstatus = mysql_query("select id from status where status_name='$statusname'");
	if(mysql_num_rows($resultstatus) == 0)
		return 0;
	$rowstatus = mysql_fetch_row($resultstatus);
	return $rowstatus[0];
}
//------------------------------------------------------------
function IsBrand($brandname) {
	$resultbrand = mysql_query("select id from brand where name='$brandname'");
	if(mysql_num_rows($resultbrand) == 0)
		return 0;
	$rowbrand = mysql_fetch_row($resultbrand);
	return $rowbrand[0];
}
//------------------------------------------------------------
function IsGroup($groupname) {
	$resultgroup = mysql_query("select id from pardul.group where name='$groupname'");
	if(mysql_num_rows($resultgroup) == 0)
		return 0;
	$rowgroup = mysql_fetch_row($resultgroup);
	return $rowgroup[0];
}
//------------------------------------------------------------
function addPageHeader($title){
	echo"<html>
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />
<link href=\"pardul.css\" rel=\"stylesheet\" type=\"text/css\">
<title>$title</title>
</head>
<body bgcolor=\"#ffffff\" topmargin=\"0\" leftmargin=\"0\" marginheight=\"0\" marginwidth=\"0\">
<center>
";
}
//------------------------------------------------------------
function addPageFooter(){
	echo"
</body>
</html>
";
}
//------------------------------------------------------------
?>
