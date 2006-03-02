<?
$Sql = "SELECT No,Baslik,Icerik,HaberSlogan,Kaynak,Durum,Tarih FROM IcerikHaber WHERE Durum='Aktif' AND No='$get_HaberNo'";
$Sonuc = sorgula($Sql);
list($vt_No,$vt_Baslik,$vt_Icerik,$vt_HaberSlogan,$vt_Kaynak,$vt_Durum,$vt_Tarih) = getir($Sonuc);
$smarty->assign('HaberSlogan',$vt_HaberSlogan);	
$smarty->assign('Baslik',$vt_Baslik);	
$smarty->assign('No',$vt_No);	
	
    if ($OturumBilgiler['OturumKullaniciNo']) {
    	$KullaniciNo = $OturumBilgiler['OturumKullaniciNo'];
    } else {
    	$KullaniciNo = 0;
    }
    
	$Yorum = $post_Yorum;
	$Gorus = $post_Gorus;
	if ($post_Gonder) {
		$Simdi = Simdi();
		$Sql = "INSERT INTO Yorum SET HaberNo='$post_No',KullaniciNo='$KullaniciNo',Yorum='$Yorum',GondermeTarih='$Simdi'";
		sorgula($Sql);
		$smarty->assign('Gonderildi',true);
		
	}
	

?>
