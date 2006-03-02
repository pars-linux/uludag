<?
if($post_Guncelle){
$post_Tarih=date('Y-m-d');
$Sql = "UPDATE SiteHakkinda SET Icerik='$post_Icerik',Tarih='$post_Tarih' WHERE No='$post_No'";
  sorgula($Sql);
  
  $Uyari="Kayýt Ýþlemi Baþarý ile Tamamlanmýþtýr!!! ";
       $smarty->assign('Uyari',$Uyari);
   
}
  $Sql = "SELECT No,Icerik,Tarih FROM SiteHakkinda WHERE No=2";
  $Sonuc = sorgula($Sql);
  
  list($vt_No,$vt_Icerik,$vt_Tarih)=getir($Sonuc);
		$smarty->assign('No',$vt_No);
		$smarty->assign('Icerik',$vt_Icerik);
		list($y,$a,$g)=explode("-",$vt_Tarih);
	    $Tarih=$g.".".$a.".".$y;
	    $smarty->assign('Tarih',$Tarih);
		//  $smarty->assign('HaberIcerik',$HaberIcerik);

?>