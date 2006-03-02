<?
if ($post_HaberNo) {
	$HaberNo = $post_HaberNo;
} else { 
	$HaberNo = $get_HaberNo;
} // else
if ($post_HaberNo&&YetkiKontrol('HaberDuzenle'))
{

  if ($post_Durum == true) 
  {
  	  $post_Durum = "Aktif";
  } else {
  	  $post_Durum = "Pasif";
  }
  list($g,$a,$y)=explode(".",$post_Tarih);
  $Tarih=$y."-".$a."-".$g;
  $Sql = "UPDATE IcerikHaber SET Baslik='$post_Baslik',Icerik='$post_Icerik',HaberSlogan='$post_HaberSlogan',Kaynak='$post_Kaynak', Durum='$post_Durum',Tarih='$Tarih' WHERE No='$HaberNo'";
  sorgula($Sql);
  $Uyari="Kayýt Ýþlemi Baþarý ile Tamamlanmýþtýr!!! ";
       $smarty->assign('Uyari',$Uyari);
}

if($HaberNo)
{
  $Sql = "SELECT No,Baslik,Icerik,HaberSlogan,Kaynak,Durum,Manset,Tarih FROM IcerikHaber WHERE No='$HaberNo'";
  $Sonuc = sorgula($Sql);
  
  list($vt_HaberNo,$vt_HaberBaslik,$vt_HaberIcerik,$vt_HaberSlogan,$vt_Kaynak,$vt_HaberDurum,$vt_Manset,$vt_HaberTarih)=getir($Sonuc);
		$smarty->assign('HaberNo',$$vt_HaberNo);
		$smarty->assign('Baslik',$vt_HaberBaslik);
		$smarty->assign('Icerik',$vt_HaberIcerik);
		$smarty->assign('HaberSlogan',$vt_HaberSlogan);
		$smarty->assign('Durum',$vt_HaberDurum);
		$smarty->assign('Manset',$vt_Manset);
		$smarty->assign('Kaynak',$vt_Kaynak);
		list($y,$a,$g)=explode("-",$vt_HaberTarih);
	    $Tarih=$g.".".$a.".".$y;
		$smarty->assign('Tarih',$Tarih);
		
  		$smarty->assign('HaberNo',$HaberNo);
//  $smarty->assign('HaberIcerik',$HaberIcerik);
}
?>