<?
  $Sql = "SELECT No,Icerik,Tarih FROM SiteHakkinda";
  $Sonuc = sorgula($Sql);
  
  list($vt_No,$vt_Icerik,$vt_Tarih)=getir($Sonuc);
		$smarty->assign('No',$vt_No);
		list($y,$a,$g)=explode("-",$vt_Tarih);
	    $Tarih=$g.".".$a.".".$y;
	    $smarty->assign('Icerik',$vt_Icerik);
		$smarty->assign('Tarih',$Tarih);
		//  $smarty->assign('HaberIcerik',$HaberIcerik);

?>