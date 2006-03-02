<?
	if($post_Dakika) {
		$Dakika = $post_Dakika;
	} else {
		$Dakika = 30;
    }
    $Simdi = Simdi();
	$Sql = "SELECT No,SonGiris FROM Kullanicilar WHERE SonGiris<>0 AND SonGiris<>'' ORDER BY SonGiris DESC";
	$Sonuc = sorgula($Sql);
	$i = 0;
 	while(list($No,$SonGiris) = getir($Sonuc)) {
		$KullaniciBilgi = KullaniciBilgi($No);
		$Fark = IkiTarihArasiFark($SonGiris,$Simdi,'Dakika');
		if($Fark>$Dakika) continue;
		$SonGiris		= TarihGetir($SonGiris,'tamgun');
		$SonGirisler[$i]['AdSoyad'] = $KullaniciBilgi['AdSoyad'];
		$SonGirisler[$i]['EPosta']	= $KullaniciBilgi['EPosta'];
		$SonGirisler[$i]['SonGiris']= $SonGiris;
  		$i++;
    }
	$UyeSayi = count($SonGirisler);
	$smarty->assign('SonGirisler',$SonGirisler);
	$smarty->assign('UyeSayi',$UyeSayi);
	$smarty->assign('Dakika',$Dakika);
	
	$Sql = "SELECT SonGiris FROM Anonim ORDER BY SonGiris DESC";
	$Sonuc = sorgula($Sql);
	$AnonimGirisler = 0;
	while(list($SonGiris) = getir($Sonuc)) {
		$Fark = IkiTarihArasiFark($SonGiris,$Simdi,'Dakika');
		if ($Fark > $Dakika) continue;
		$AnonimGirisler++;
	}
	$smarty->assign('AnonimSayi',$AnonimGirisler);
	$smarty->assign('Toplam',$AnonimGirisler + $UyeSayi);
?>
