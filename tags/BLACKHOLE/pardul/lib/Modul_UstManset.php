<?

//error_reporting(E_ALL & ~E_NOTICE);
//{{{ Haber Silme
if($post_HaberAra) {
 $Sql = "SELECT No,Baslik,Icerik,Resim,Durum,HaberSlogan,Tarih FROM IcerikHaber  WHERE 1=1 AND Durum='Aktif'";
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
	$Sql = "SELECT No,Baslik,Icerik,Resim,Durum,HaberSlogan,Tarih FROM IcerikHaber WHERE Durum='Aktif' AND No='$get_HaberNo'";
	$Detay="1";
	$smarty->assign('Detay',$Detay);
} else {
		$Sql = "SELECT No,Baslik,Icerik,HaberSlogan,Resim,Durum,Tarih FROM IcerikHaber WHERE Durum='Aktif' AND Manset='Aktif' ORDER BY No DESC LIMIT 0,$sistem_MansetSayi";
}
// echo $Sql;
$Sonuc = sorgula($Sql);
	$i = 0;
	while(list($vt_No,$vt_Baslik,$vt_Icerik,$vt_HaberSlogan,$vt_Resim,$vt_Durum,$vt_Tarih) = getir($Sonuc))
		{
		$Haberler[$i]['No']			= $vt_No;
		$Haberler[$i]['Baslik']		= $vt_Baslik;
		$Haberler[$i]['Icerik']		= $vt_Icerik;
		$Haberler[$i]['HaberSlogan']= $vt_HaberSlogan;
		$Haberler[$i]['Resim']		= $vt_Resim;
		$Haberler[$i]['Durum']		= $vt_Durum;
		list($y,$a,$g)				= explode("-",$vt_Tarih);
		$Haberler[$i]['Tarih']		= $g.".".$a.".".$y;
		$i++;
		}

$smarty->assign('Haberler',$Haberler);

//}}}


/*if($get_HaberNo)
{
  $Sql = "SELECT No,Baslik,Icerik,Resim,Durum,Tarih FROM IcerikHaber WHERE No='$get_HaberNo'";
  $Sonuc = sorgula($Sql);
  $HaberBilgiler = getir($Sonuc,DB_FETCHMODE_ASSOC); 
  $smarty->assign('HaberBilgiler',$HaberBilgiler); 
  $smarty->assign('HaberNo',$HaberNo);
}
if($get_HaberNo&&$get_Detay=='true')
{
  $Sql = "SELECT No,Baslik,Icerik,Resim,Durum,Tarih FROM IcerikHaber WHERE No='$get_HaberNo'";
  $Sonuc = sorgula($Sql);
  $HaberBilgiler = getir($Sonuc,DB_FETCHMODE_ASSOC); 
  $smarty->assign('HaberBilgiler',$HaberBilgiler); 
  $smarty->assign('HaberNo',$HaberNo);
}*/



/*//{{{ Mansetler Cekiliyor: Aktif Olanlar...
	$Sql = "SELECT No,Baslik,Icerik,Resim FROM IcerikManset WHERE Durum='Aktif' ORDER BY No DESC LIMIT 3";

$Sonuc = sorgula($Sql);
	$i = 0;
	while(list($vt_No,$vt_Baslik,$vt_Icerik,$vt_Resim) = getir($Sonuc))
		{
		$Mansetler[$i]['No']		= $vt_No;
		$Mansetler[$i]['Baslik']	= $vt_Baslik;
		$Mansetler[$i]['Icerik']	= $vt_Icerik;
		$Mansetler[$i]['Resim']		= $vt_Resim;
		$i++;
		}
$smarty->assign('Mansetler',$Mansetler);
//}}}*/
?>