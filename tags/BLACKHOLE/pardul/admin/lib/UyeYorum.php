<?
if ($get_Onay&&$get_YorumNo) {
	$Sql = "UPDATE Yorum SET Durum='$get_Onay' WHERE No=$get_YorumNo";
	$Sonuc = sorgula($Sql);
}
	//{{{ UyeGorusler($KullaniciNo)
	function UyeGorusler($KullaniciNo,$EPosta) 
	{
		$Sql = "SELECT Mesaj,TarihSaat FROM GorusOneri WHERE KullaniciNo='$KullaniciNo' OR EPosta='$EPosta'";	
		$Sonuc = sorgula($Sql);	
		$i = 0;
		while(list($Mesaj,$TarihSaat) = getir($Sonuc)) {
			$Gorusler[$i]['Gorus'] = stripslashes($Mesaj);
			$Gorusler[$i]['Tarih'] = TarihGetir($TarihSaat,'gun');
			$i++;
		}
		return $Gorusler;
	}
	//}}}

	$KullaniciNo = $get_UyeNo;
	$KullaniciBilgi = KullaniciBilgi($KullaniciNo);
	$Gorusler = UyeGorusler($KullaniciNo,$KullaniciBilgi['EPosta']);

	$smarty->assign('AdSoyad',$KullaniciBilgi['AdSoyad']);
	$smarty->assign('Gorusler',$Gorusler);
	$smarty->assign('GorusSayi',count($Gorusler));
	$smarty->assign('UyeNo',$KullaniciNo);
/*	//$UrunYorumlar = UrunYorumlar('Tumu');
	$i = 0;
	foreach($UrunYorumlar as $Yorum) {
		if ($Yorum['KullaniciNo'] == $KullaniciNo) {
			$Yorumlar[$i]['Yorum']  = $Yorum['Yorum'];
			$Yorumlar[$i]['Gorus']  = $Yorum['Gorus'];
			$Yorumlar[$i]['Tarih']  = $Yorum['Tarih'];
			$Yorumlar[$i]['UrunAd'] = $Yorum['UrunAd'];
			$Yorumlar[$i]['Yorum']  = $Yorum['Yorum'];
			$i++;
		}
	}*/
	$Sql = "SELECT No,Yorum,GondermeTarih,HaberNo,Durum FROM Yorum WHERE KullaniciNo='$KullaniciNo'";
	$Sonuc = sorgula($Sql);	
	$numrows=$Sonuc->numRows();
	$smarty->assign('YorumSayi',$numrows);
		$i = 0;
		while(list($No,$Yorum,$Tarih,$Haber,$Durum) = getir($Sonuc)) {
			$Yorumlar[$i]['Yorum'] = stripslashes($Yorum);
			$Yorumlar[$i]['Tarih'] = TarihGetir($Tarih,'gun');
			$Yorumlar[$i]['Durum'] = $Durum;
			$Yorumlar[$i]['No'] = $No;
			$i++;
		}
	$smarty->assign('Yorumlar',$Yorumlar);	
	
		
?>
