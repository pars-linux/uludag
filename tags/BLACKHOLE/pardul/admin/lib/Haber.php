<?
//error_reporting(E_ALL & ~E_NOTICE);
//{{{ Haber Silme
if ($get_Sil&&YetkiKontrol('HaberSilme'))
{
  $Sql = "DELETE FROM IcerikHaber WHERE No='$get_Sil'"; 
  sorgula($Sql);
}
//}}}
$smarty->assign('IslemUyari',$Mesaj);
//}}}
if ($get_Aktif&&$get_HaberNo) {
	$Sql = "UPDATE IcerikHaber SET Durum='$get_Aktif' WHERE No=$get_HaberNo";
	$Sonuc = sorgula($Sql);
}
if ($get_Manset&&$get_HaberNo) {
	$Sql = "UPDATE IcerikHaber SET Manset='$get_Manset' WHERE No=$get_HaberNo";
	$Sonuc = sorgula($Sql);
}
//{{{ Haber Ekle
if($post_Ekle){
	list($g,$a,$y)=explode(".",$post_YeniHaberTarih);
	$HaberTarih=$y."-".$a."-".$g;
	$Sql = "INSERT INTO IcerikHaber SET
       Baslik		='$post_YeniHaberBaslik',
       Tarih	    ='$HaberTarih'";
       sorgula($Sql);
       // Debug icin aciniz.
       //echo $Sql;
       $Uyari="Kayýt Ýþlemi Baþarý ile Tamamlanmýþtýr!!! ";
       $smarty->assign('Uyari',$Uyari);
}
//}}}
//{{{ Haberler Listeleme
if($post_HaberAra){
 $Sql = "SELECT No,Baslik,Icerik,Kaynak,Durum,Manset,Tarih FROM IcerikHaber  WHERE 1=1 ";
 if($post_Baslik)       $SqlEk.= " AND Baslik LIKE '%$post_Baslik%'"; 
 if($post_Tarih){        
 list($g,$a,$y)=explode(".",$post_Tarih);
 $Tarih=$y."-".$a."-".$g;
 $SqlEk.= " AND Tarih='$Tarih'";
 } 
 if($post_Durum)       $SqlEk.= " AND Durum='$post_Durum'"; 
 if($post_MansetDurum)       $SqlEk.= " AND Manset='$post_MansetDurum'"; 
 $Sql.=$SqlEk;
 $Sql.=" ORDER BY No DESC";
}else{
$Sql = "SELECT No,Baslik,Icerik,Kaynak,Durum,Manset,Tarih FROM IcerikHaber ORDER BY No DESC LIMIT 0,10";
}
$Sonuc = sorgula($Sql);
$numrows=$Sonuc->numRows();
$smarty->assign('TumHaberSayi',$numrows);
	$i = 0;
	while(list($vt_No,$vt_Baslik,$vt_Icerik,$vt_Kaynak,$vt_Durum,$vt_Manset,$vt_Tarih) = getir($Sonuc))
		{
		$Haberler[$i]['No']			= $vt_No;
		$Haberler[$i]['Baslik']		= $vt_Baslik;
		$Haberler[$i]['Icerik']		= $vt_Icerik;
		$Haberler[$i]['Kaynak']		= $vt_Kaynak;
		$Haberler[$i]['Durum']		= $vt_Durum;
		$Haberler[$i]['Manset']		= $vt_Manset;
		list($y,$a,$g)				= explode("-",$vt_Tarih);
		$Haberler[$i]['Tarih']		= $g.".".$a.".".$y;
		$i++;
		}
$smarty->assign('Haberler',$Haberler);

//}}}


if($HaberNo)
{
  $Sql = "SELECT No,Baslik,Icerik,Kaynak,Durum,Manset,Tarih FROM IcerikHaber WHERE No='$HaberNo'";
  $Sonuc = sorgula($Sql);
  $HaberBilgiler = getir($Sonuc,DB_FETCHMODE_ASSOC); 
  $smarty->assign('HaberBilgiler',$HaberBilgiler); 
  $smarty->assign('HaberNo',$HaberNo);
}

?>
