<?
if($get_Yer=="Haberler"){
$Sql = "SELECT No,Baslik,Icerik,HaberSlogan,Kaynak,Durum,Tarih FROM IcerikHaber WHERE Durum='Aktif' AND No='$get_HaberNo'";
// echo $Sql;
$Sonuc = sorgula($Sql);
	$i = 0;
	while(list($vt_No,$vt_Baslik,$vt_Icerik,$vt_HaberSlogan,$vt_Kaynak,$vt_Durum,$vt_Tarih) = getir($Sonuc))
		{
		$Haberler[$i]['No']			= $vt_No;
		$Haberler[$i]['Baslik']		= $vt_Baslik;
		$Haberler[$i]['Icerik']		= $vt_Icerik;
		$Haberler[$i]['HaberSlogan']= $vt_HaberSlogan;
		$Haberler[$i]['Kaynak']		= $vt_Kaynak;
		$Haberler[$i]['Durum']		= $vt_Durum;
		list($y,$a,$g)				= explode("-",$vt_Tarih);
		$Haberler[$i]['Tarih']		= $g.".".$a.".".$y;
		$i++;
		}

$smarty->assign('Haberler',$Haberler);
}
if($get_Yer=="EnglishNews"){
$Sql = "SELECT No,Baslik,Icerik,HaberSlogan,Kaynak,Durum,Tarih FROM EnglishNews WHERE Durum='Aktif' AND No='$get_HaberNo'";
// echo $Sql;
$Sonuc = sorgula($Sql);
	$i = 0;
	while(list($vt_No,$vt_Baslik,$vt_Icerik,$vt_HaberSlogan,$vt_Kaynak,$vt_Durum,$vt_Tarih) = getir($Sonuc))
		{
		$Haberler[$i]['No']			= $vt_No;
		$Haberler[$i]['Baslik']		= $vt_Baslik;
		$Haberler[$i]['Icerik']		= $vt_Icerik;
		$Haberler[$i]['HaberSlogan']= $vt_HaberSlogan;
		$Haberler[$i]['Kaynak']		= $vt_Kaynak;
		$Haberler[$i]['Durum']		= $vt_Durum;
		list($y,$a,$g)				= explode("-",$vt_Tarih);
		$Haberler[$i]['Tarih']		= $g.".".$a.".".$y;
		$i++;
		}

$smarty->assign('Haberler',$Haberler);	
}
if($get_Yer=="Soylesi"){
	$Sql = "SELECT * FROM IcerikSoylesi ORDER BY No ASC LIMIT 1";
	$Sonuc = sorgula($Sql);
	while(list($vt_SoylesiNo,$vt_SoylesiKonu,$vt_SoylesiTarih,$vt_SoylesiKimle,$vt_SoylesiIcerik,$vt_SoylesiAktif)=getir($Sonuc)){
		$Soylesiler[$i]['SoylesiIcerik']=$vt_SoylesiIcerik;
	}
	$smarty->assign('Soylesiler',$Soylesiler);	
}
if($get_Yer=="KoseYazisi"){
$Sql = "SELECT No,Konu,Icerik,Yazar,Tarih,Durum FROM IcerikKoseYazilari WHERE No='$get_No'";
$Sonuc = sorgula($Sql);
	$i = 0;
	while(list($vt_No,$vt_Konu,$vt_Icerik,$vt_Yazar,$vt_Tarih,$vt_Durum) = getir($Sonuc))
		{
		$KoseYazilari[$i]['No']			= $vt_No;
		$KoseYazilari[$i]['Konu']		= $vt_Konu;
		$KoseYazilari[$i]['Icerik']		= $vt_Icerik;
		$strsql = "SELECT No,Ad,Soyad,Unvan,Resim FROM KoseYazarlari WHERE No='$vt_Yazar'";
		$sonuc = sorgula($strsql);
		list($vt_No,$vt_Ad,$vt_Soyad,$vt_Unvan,$vt_Resim) = getir($sonuc);
		$Yazar=$vt_Unvan." ".$vt_Ad." ".$vt_Soyad;
		$KoseYazilari[$i]['Yazar']		= $Yazar;
		$KoseYazilari[$i]['YazarNo']	= $vt_No;
		$KoseYazilari[$i]['Durum']		= $vt_Durum;
		list($y,$a,$g)				    = explode("-",$vt_Tarih);
		$KoseYazilari[$i]['Tarih']		= $g.".".$a.".".$y;
		$i++;
		}

$smarty->assign('KoseYazilari',$KoseYazilari);

}
?>
