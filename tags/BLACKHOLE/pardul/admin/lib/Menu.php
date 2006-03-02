<?
$Menuler = array();
$Sira = 1;
$Sorgu1 = sorgula("SELECT No,Isim,Adres FROM YonetimMenu WHERE AnaNo='0' AND YeniPencere='Hayir' ORDER BY No");
while(list($vt_No,$vt_Isim,$vt_Adres) = $Sorgu1->fetchRow())
	{
	$Menuler[$Sira-1]['Isim'] = $vt_Isim;
	$Menuler[$Sira-1]['Sira'] = $Sira;
	$Sorgu2 = sorgula("SELECT No,Isim,Adres FROM YonetimMenu WHERE AnaNo='$vt_No' ORDER BY No");
	while(list($AltNo,$Isim,$Adres)=$Sorgu2->fetchRow())
		{
		$Menuler[$Sira-1]['AltMenuler'][$AltNo]['Isim'] = $Isim;
		$Menuler[$Sira-1]['AltMenuler'][$AltNo]['Adres'] = $Adres;
		}
	$Sira++;
	}
$smarty->assign('Menuler',$Menuler);
// $smarty->display("lib/Menu.tpl");
?>
