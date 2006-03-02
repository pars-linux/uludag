<?php
$Sql = "SELECT No,Baslik,Icerik,Kaynak,Durum,Tarih FROM IcerikHaber WHERE Durum='Aktif' ORDER BY Tarih DESC LIMIT 0,$sistem_HaberSayi";
// echo $Sql;
$Sonuc = sorgula($Sql);
	$i = 0;
	while(list($vt_No,$vt_Baslik,$vt_Icerik,$vt_Kaynak,$vt_Durum,$vt_Tarih) = getir($Sonuc))
		{
		$HaberListe[$i]['No']			= $vt_No;
		$HaberListe[$i]['Baslik']		= $vt_Baslik;
		$HaberListe[$i]['Icerik']		= $vt_Icerik;
		$HaberListe[$i]['Kaynak']		= $vt_Kaynak;
		$HaberListe[$i]['Durum']		= $vt_Durum;
		list($y,$a,$g)				    = explode("-",$vt_Tarih);
		$HaberListe[$i]['Tarih']		= $g.".".$a.".".$y;
		$i++;
		}

$smarty->assign('HaberListe',$HaberListe);
?>