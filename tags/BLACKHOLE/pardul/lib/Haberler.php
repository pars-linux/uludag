<?
//error_reporting(E_ALL & ~E_NOTICE);
//{{{ Haber Silme
 
if($post_HaberAra) {
 $Sql = "SELECT No,Baslik,Icerik,HaberSlogan,Kaynak,Durum,Tarih FROM IcerikHaber WHERE 1=1 AND Durum='Aktif'";
	if ($post_Anahtar <> '') {
		$Sql.= " AND (Baslik LIKE '%$post_Anahtar%' OR Icerik LIKE '%$post_Anahtar%')";
	}
	if ($post_Tarih) {
		list($g,$a,$y)=explode(".",$post_Tarih);
		$Tarih=$y."-".$a."-".$g;
		$SqlEk.= " AND Tarih='$Tarih'";
	} // if post_Tarih 
		$Sql.=" AND Durum='Aktif' ORDER BY Tarih DESC LIMIT 0,20";
}elseif($get_HaberNo){
	$Sql = "SELECT No,Baslik,Icerik,HaberSlogan,Kaynak,Durum,Tarih FROM IcerikHaber WHERE Durum='Aktif' AND No='$get_HaberNo'";
	$Detay="1";
	$smarty->assign('Detay',$Detay);
} else {
		$Sql = "SELECT No,Baslik,Icerik,HaberSlogan,Kaynak,Durum,Tarih FROM IcerikHaber WHERE Durum='Aktif' AND Manset='Aktif' ORDER BY Tarih DESC LIMIT 0,$sistem_MansetSayi";
}
// echo $Sql;
$Sonuc = sorgula($Sql);
	if($post_HaberAra) {
	$numrows=$Sonuc->numRows();
	AramaHit('Haberler',$post_Anahtar,$numrows);
	}
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

$Sql = "SELECT No,Yorum,GondermeTarih,HaberNo,Durum,KullaniciNo FROM Yorum WHERE HaberNo='$get_HaberNo' AND Durum='Onaylandi' ORDER BY GondermeTarih DESC LIMIT 0,$sistem_YorumSayi";
	$Sonuc = sorgula($Sql);	
	$numrows=$Sonuc->numRows();
	$smarty->assign('YorumSayi',$numrows);
		$i = 0;
		while(list($No,$Yorum,$Tarih,$Haber,$Durum,$KullaniciNo) = getir($Sonuc)) {
			$Yorumlar[$i]['Yorum'] = stripslashes($Yorum);
			$Yorumlar[$i]['Tarih'] = TarihGetir($Tarih,'gun');
			//yazani bulmak için
			$sql = "SELECT No,AdSoyad FROM Kullanicilar WHERE No='$KullaniciNo'";
			$sonuc = sorgula($sql);	
			list($UyeNo,$AdSoyad) = getir($sonuc);
		    $Yorumlar[$i]['Yazan']=$AdSoyad;
			$Yorumlar[$i]['Durum'] = $Durum;
			$Yorumlar[$i]['No'] = $No;
			$i++;
		}
	$smarty->assign('Yorumlar',$Yorumlar);	
//}}}
//Haberler Sayfasýnýn hitleri

$FullPage=$REQUEST_URI;
$DegerVar=strstr($FullPage,'&');
if($DegerVar<>''){
	list($sol,$HaberSayi)=explode('=',$DegerVar);
	$sqlkontrol = "SELECT No,Baslik,Icerik,HaberSlogan,Kaynak,Durum,Tarih FROM IcerikHaber WHERE Durum='Aktif' AND Manset='Aktif' AND No='$HaberSayi'";
	$sonuckontrol = sorgula($sqlkontrol);	
	$nrows=$sonuckontrol->numRows();
	if($nrows<>0){
		SayfaHitler($FullPage);
	}
}elseif($Page=="Haberler"){
		SayfaHitler($FullPage);
}


?>
