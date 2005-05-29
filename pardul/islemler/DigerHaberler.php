<?php
$Sql = "SELECT No,Baslik,Icerik,Kaynak,Durum,Tarih FROM IcerikHaber WHERE Durum='Aktif' ORDER BY Tarih DESC";
// echo $Sql;
$Sonuc = sorgula($Sql);
$numrows=$Sonuc->numRows();
$smarty->assign('TumHaberSayi',$numrows);
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

if(count($HaberListe))
{
	//$post_SayfaNo=1;
	$_GET['Grup'] = $post_SayfaNo;
	require_once "$KutuphaneDizin/Pear/Pager.php";
	$Degiskenler = array(
	'itemData' => $HaberListe,
	'perPage' => $sistem_DigerHaberSayi,
	'delta' => 8,		// for 'Jumping'-style a lower number is better
	'append' => true,
	//'separator' => ' | ',
	'clearIfVoid' => false,
	'urlVar' => 'Grup',
	'useSessions' => true,
	'closeSession' => true,
	'mode'  => 'Sliding');  // Jumping de olabilir
	$SayfaAyrim = &new Pager($Degiskenler);
	$HaberListe = $SayfaAyrim->getPageData();
	$Kopruler = $SayfaAyrim->getLinks();

	$SonSayfa = $SayfaAyrim->numPages();
	if($SonSayfa > 1)	$smarty->assign('CokSayfali',true);
	if(!$post_SayfaNo)  $post_SayfaNo = 1;
	if($post_SayfaNo && $post_SayfaNo > 1 && $post_SayfaNo <= $SonSayfa)
		$smarty->assign('OncekiSayfa',"javascript:SayfaGonder(".($post_SayfaNo-1).");");
	if($SonSayfa > $post_SayfaNo)
		$smarty->assign('SonrakiSayfa',"javascript:SayfaGonder(".($post_SayfaNo+1).");");
	$SayfaKopruler = array();
	for($i=1;$i<=$SonSayfa;$i++)
		{
		if($i!=$post_SayfaNo)
		$SayfaKopruler[$i]['Adres'] = "javascript:SayfaGonder($i);";
		$SayfaKopruler[$i]['Isim'] = $i;
		}
	$smarty->assign('Sonuclar',$Sonuclar);
	$smarty->assign('SayfaKopruler',$SayfaKopruler);
}
//}}}

$HaberSayi = count($HaberListe);
$smarty->assign('HaberListe',$HaberListe);
$smarty->assign('HaberSayi',$HaberSayi);
$Bugun = Bugun();  // date
$smarty->assign('Bugun',$Bugun);

?>
