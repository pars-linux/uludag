<?
	$Sql = "SELECT Mesaj FROM notes ORDER BY Rand() LIMIT 1";
	$Sonuc = sorgula($Sql);
	list($Mesaj) = getir($Sonuc);
	$smarty->assign('Ipucu',$Mesaj);
?>
