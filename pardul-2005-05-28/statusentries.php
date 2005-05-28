<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
  
  
  -- statusentries.php
  elimizde bir kök kategori(group_id) ve bir marka (brand_id) var. bu marka altındaki
  modellere ait durum bilgisi girişlerini ve girişlerle ilgili yorumları listelemek
  istiyoruz.
  
  
  önce "aktif" modeller çekilecek (bkz: alg_1)
  modeller için bir döngü açılacak { (bkz: alg_2)
  	model ekrana basılacak (bkz: alg_3)
  	modelle ilgili durum bilgisi girişleri çekilecek (bkz: alg_4)
	durum bilgisi girişleri için bir döngü açılacak { (bkz: alg_5)
		durum bilgisi girişinin statüsü aktifse { (bkz: alg_6)
			giriş ekrana basılacak (bkz: alg_7)
			durum bilgisi girişiyle ilgili yorumlar çekilecek (bkz: alg_8)
			yorumlar için bir döngü açılacak { (bkz: alg_9)
				yorumun statüsü aktifse (bkz: alg_10)
					yorum ekrana basılacak (bkz: alg_11)
				değilse { (bkz: alg_12)
					yönetici için listeliyorsak (bkz: alg_13)
						statüs aktife çekilsin mi diye sorulacak (bkz: alg_14)
				}
			}
		}
		değilse { (bkz: alg_15)
			yönetici için listeliyorsak { (bkz: alg_16)
				statüs aktife çekilsin mi diye sorulacak (bkz: alg_17)
			}
		}
	}
  }
  yönetici için listeliyorsak { (bkz: alg_18)
  	"pasif" modeller çekilecek (bkz: alg_19)
	modeller için bir döngü açılacak (bkz: alg_20)
		statüs aktife çekilsin mi diye sorulacak (bkz: alg_21)
  }
  
*/

if(GetRoleName($roleid) == "admin" || IsManaggedBy($userid, $grpid))
	$hasfullaccess = true;
else
	$hasfullaccess = false;
// alg_1
$resultmodel = mysql_query("select model.id from model, group_brand where model.groupbrand_id = group_brand.id and group_brand.group_id='$grpid' and group_brand.brand_id='$brandid' and status='ACTIVE'");
echo "<table border=\"1\">";
$brandname = GetBrandName($brandid);
$groupname = GetGroupName($grpid);
// alg_2
while(($rowmodel = mysql_fetch_row($resultmodel))) {
	$modelname = GetModelName($rowmodel[0]);
	// alg_3
	echo "<tr>
		<td colspan=\"4\" align=\"center\"><b>$groupname > $brandname > $modelname</b></td>
		</tr>
		<tr>
		<td align=\"center\"><b>Pardus Versiyonu</b></td>
		<td align=\"center\"><b>Durum</b></td>
		<td align=\"center\"><b>Giriş Tarihi</b></td>
		<td align=\"center\"><b>...</b></td>
		</tr>
		";
	// alg_4
	$resultstatus = mysql_query("select * from model_pv_status where model_id='$rowmodel[0]'");
	// alg_5
	while(($rowstatus = mysql_fetch_row($resultstatus))) {
		$status = GetStatusName($rowstatus[3]);
		$pv = GetPVName($rowstatus[2]);
		$desc = nl2br($rowstatus[4]);
		// alg_6
		if($rowstatus[6] == 'ACTIVE') {
			// alg_7
			echo "
			<tr>
			<td>$pv</td>
			<td>$status</td>
			<td>$rowstatus[5]</td>
			";
			if($hasfullaccess)
				echo "
					<td align=\"center\"><a href=\"?action=editstatusentry&grpid=$grpid&brandid=$brandid&statusentryid=$rowstatus[0]\">[DÜZENLE]</a>&nbsp;<a href=\"?action=delstatusentry&grpid=$grpid&brandid=$brandid&statusentryid=$rowstatus[0]\">[SİL]</a></td>
				";
			else
				echo "
					<td align=\"center\">[N/A]</td>
				";
			echo "
			</tr>
			<tr>
			<td colspan=\"4\">$desc</td>
			</tr>
			";
			// alg_8
			$resultcomments = mysql_query("select * from comment where mpvs_id='$rowstatus[0]'");
			echo "
			<tr>
			<td colspan=\"4\" align=\"center\">
			<table border=\"1\">
			<tr>
			<td colspan=\"4\" align=\"center\"><b>YORUMLAR</b></td>
			</tr>
			<td align=\"center\"><b>Gönderen</b></td>
			<td align=\"center\"><b>Yorum</b></td>
			<td align=\"center\"><b>Tarih</b></td>
			<td align=\"center\"><b>...</b></td>
			</tr>
			";
			// alg_9
			while(($rowcomments = mysql_fetch_row($resultcomments))) {
				$comment = nl2br($rowcomments[2]);
				// alg_10
				if($rowcomments[6] == 'ACTIVE') {
					// alg_11
					echo "
					<tr>
					<td><a href=\"mailto:$rowcomments[3]\">$rowcomments[4]</a></td>
					<td>$comment</td>
					<td>$rowcomments[5]</td>
					";
					if($hasfullaccess)
						echo "
						<td align=\"center\"><a href=\"?action=delcomment&grpid=$grpid&brandid=$brandid&statusentryid=$rowstatus[0]&commentid=$rowcomments[0]\">[SİL]</a></td>
						";
					else
						echo "
						<td align=\"center\">[N/A]</td>
						";
				}
				// alg_12
				else {
					// alg_13
					if($hasfullaccess) {
						// alg_14
						echo "
						<tr>
						<td><a href=\"mailto:$rowcomments[3]\">$rowcomments[4]</a></td>
						<td>$comment</td>
						<td>$rowcomments[5]</td>
						<td align=\"center\"><a href=\"?action=app_comment&modelid=$rowmodel[0]&commentid=$rowcomments[0]\">[ONAYLA]</a></td>
						";
					}
				}
			}
			echo "
				<tr>
				<td align=\"center\" colspan=\"4\">Yeni yorum eklemek için <a href=\"?action=addcomment&grpid=$grpid&brandid=$brandid&modelid=$rowmodel[0]&statusentryid=$rowstatus[0]\">tıklayınız</a>.</td>
				</tr>
			</table>
			</td>
			</tr>
			";

		}
		// alg_15
		else {
			// alg_16
			if($hasfullaccess) {
				// alg_17
				echo "
				<tr>
				<td>$pv</td>
				<td>$status</td>
				<td>$rowstatus[5]</td>
				<td align=\"center\"><a href=\"?action=app_statusentry&modelid=$rowmodel[0]&statusentryid=$rowstatus[0]\">[ONAYLA]</a></td>
				</tr>
				<tr>
				<td colspan=\"4\">$desc</td>
				</tr>
				";
			}
		}
	}
}
// alg_18
if($hasfullaccess) {
	echo"
		<tr>
		<td colspan=\"4\">
		<br>
		</td>
		</tr>
		<tr>
		<td colspan=\"4\" align=\"center\">
		<table border=\"1\">
		<tr>
		<td colspan=\"2\" align=\"center\">
		<b>Onay Bekleyen Model Girişleri</b>
		</td>
		</tr>
		<tr>
		<td align=\"center\">
		<b>Model</b>
		</td>
		<td align=\"center\">
		<b>...</b>
		</td>
		</tr>
		";
	// alg_19
	$resultpassivemodel = mysql_query("select model.id from model, group_brand where model.groupbrand_id = group_brand.id and group_brand.group_id='$grpid' and group_brand.brand_id='$brandid' and status='PASSIVE'");
	// alg_20
	while(($rowpassivemodel=mysql_fetch_row($resultpassivemodel))) {
		$modelname = GetModelName($rowpassivemodel[0]);
		// alg_21
		echo "
			<tr>
			<td>$groupname > $brandname > $modelname</td>
			<td align=\"center\"><a href=\"?action=app_model&modelid=$rowpassivemodel[0]\">[ONAYLA]</a></td>
			</tr>
			";
	}
}
echo "
		</table>
		</td>
		</tr>
		<tr>
		<td colspan=\"4\">
		<br>
		</td>
		</tr>
		<tr>
		<td colspan=\"4\">
		<br>
		</td>
		</tr>
		<tr>
		<td colspan=\"4\">
		$groupname grubundaki $brandname markasına yeni durum bilgisi eklemek için <a href=\"?action=addstatusentry&grpid=$grpid&brandid=$brandid\">tıklayınız</a>.
		</td>
		</tr>";
?>
</table>
