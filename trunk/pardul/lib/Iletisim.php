<?
if($post_Gonder) {

	$OturumVar = $OturumBilgiler['OturumVar'];
	$Simdi = Simdi();
	$AktifPasif = 'Aktif';
	if ($OturumVar) {
		$KullaniciNo = $OturumBilgiler['OturumKullaniciNo'];
		$KullaniciBilgi = KullaniciBilgi($KullaniciNo);
		$AdSoyad = $KullaniciBilgi['AdSoyad'];
		$EPosta  = $KullaniciBilgi['EPosta'];
	} else {
		$KullaniciNo = 0;
		$AdSoyad = $post_AdSoyad;
		$EPosta  = $post_EPosta1;
	}
	$Mesaj = $post_Mesaj;

	$SqlKontrol = "SELECT No FROM GorusOneri WHERE EPosta='$EPosta' AND Mesaj='$Mesaj'";
	$SonucKontrol = sorgula($SqlKontrol);
	if(!$SonucKontrol->numRows()) {
		$Sql = "INSERT INTO GorusOneri SET AdSoyad='$AdSoyad',EPosta='$EPosta',KullaniciNo='$KullaniciNo',Mesaj='$Mesaj',TarihSaat='$Simdi',AktifPasif='$AktifPasif'";
		sorgula($Sql);	
		$smarty->assign('Kaydedildi',true);
	}
}

?>
