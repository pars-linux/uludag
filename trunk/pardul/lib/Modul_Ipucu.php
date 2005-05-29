<?
	$Sql = "SELECT Mesaj FROM Notlar ORDER BY Rand() LIMIT 1";
	$Sonuc = sorgula($Sql);
	list($Mesaj) = getir($Sonuc);
	$smarty->assign('Ipucu',$Mesaj);
?>
