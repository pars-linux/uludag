<?
    $KapidaOdeme = false;
	if ($sistem_KapidaOdeme=='Olsun') $KapidaOdeme = true;	
	if (!$post_BasTarih) $BasTarih = '23.04.2004';else $BasTarih = $post_BasTarih;
	if (!$post_BitTarih) $BitTarih = date('d').'.'.date('m').'.'.date('Y');
	$BaslangicTarih = TarihDonustur($BasTarih);
	$BitisTarih     = TarihDonustur($BitTarih,'Buyuk');
		
	if ($post_Raporla) {
		//{{{ Havale sipariþler
		$Sql = "SELECT No,OdenenTutar FROM Siparisler WHERE OdemeTur='Havale' AND SiparisTarih>='$BaslangicTarih' AND SiparisTarih<='$BitisTarih' AND Durum='Gonderildi'";
		$Sonuc = sorgula($Sql);
		$RaporSonuc['HavaleSiparis'] = $Sonuc->numRows();
		$HavaleTutar = 0;
		$HavaleUrunSayi = 0;
		while(list($No,$OdenenTutar) = getir($Sonuc)) {
			$Sql = "SELECT SUM(Miktar) FROM SiparisUrunler WHERE SiparisNo='$No'";
			$SonucUrun = sorgula($Sql);
			list($Miktar) = getir($SonucUrun);
			$HavaleUrunSayi += $Miktar;
			$HavaleTutar    += $OdenenTutar; 
		}
		$RaporSonuc['HavaleUrun']  = $HavaleUrunSayi;
		$RaporSonuc['ToplamSiparis'] += $RaporSonuc['HavaleSiparis'];
		$RaporSonuc['ToplamUrun']    += $RaporSonuc['HavaleUrun'];
		$RaporSonuc['ToplamTutar']   += $HavaleTutar;
		$RaporSonuc['HavaleTutar']    = ParaDuzenle($HavaleTutar,'TL');
		//}}}
		//{{{ Kredi sipariþler
		$Sql = "SELECT No,OdenenTutar FROM Siparisler WHERE (OdemeTur='KrediKartiPesin' OR OdemeTur='KrediKartiTaksit') AND SiparisTarih>='$BaslangicTarih' AND SiparisTarih<='$BitisTarih' AND Durum='Gonderildi'";
		$Sonuc = sorgula($Sql);
		$RaporSonuc['KrediSiparis'] = $Sonuc->numRows();
		$KrediTutar = 0;
		$KrediUrunSayi = 0;
		while(list($No,$OdenenTutar) = getir($Sonuc)) {
			$Sql = "SELECT SUM(Miktar) FROM SiparisUrunler WHERE SiparisNo='$No'";
			$SonucUrun = sorgula($Sql);
			list($Miktar) = getir($SonucUrun);
			$KrediUrunSayi += $Miktar;
			$KrediTutar    += $OdenenTutar; 
		}
		$RaporSonuc['KrediUrun']  = $KrediUrunSayi;
		$RaporSonuc['ToplamSiparis'] += $RaporSonuc['KrediSiparis'];
        $RaporSonuc['ToplamUrun']    += $RaporSonuc['KrediUrun'];
        $RaporSonuc['ToplamTutar']   += $KrediTutar;
		$RaporSonuc['KrediTutar'] = ParaDuzenle($KrediTutar,'TL');
		//}}}
		//{{{ Kapida sipariþler
		if ($KapidaOdeme) {
			$Sql = "SELECT No,OdenenTutar FROM Siparisler WHERE OdemeTur='KapidaOdeme' AND SiparisTarih>='$BaslangicTarih' AND SiparisTarih<='$BitisTarih' AND Durum='Gonderildi'";
			$Sonuc = sorgula($Sql);
			$RaporSonuc['KapidaSiparis'] = $Sonuc->numRows();
			$KapidaTutar = 0;
			$KapidaUrunSayi = 0;
			while(list($No,$OdenenTutar) = getir($Sonuc)) {
				$Sql = "SELECT SUM(Miktar) FROM SiparisUrunler WHERE SiparisNo='$No'";
				$SonucUrun = sorgula($Sql);
				list($Miktar) = getir($SonucUrun);
				$KapidaUrunSayi += $Miktar;
				$KapidaTutar    += $OdenenTutar; 
			}
			$RaporSonuc['KapidaUrun']  = $KapidaUrunSayi;
			$RaporSonuc['ToplamSiparis'] += $RaporSonuc['KapidaSiparis'];
	        $RaporSonuc['ToplamUrun']    += $RaporSonuc['KapidaUrun'];
    	    $RaporSonuc['ToplamTutar']   += $KapidaTutar;
			$RaporSonuc['KapidaTutar'] = ParaDuzenle($KapidaTutar,'TL');
		}
			//}}}
		$RaporSonuc['ToplamTutar'] = ParaDuzenle($RaporSonuc['ToplamTutar'],'TL');
		$smarty->assign('Listelendi',true);
	}


    $smarty->assign('Sonuc',$RaporSonuc);

	$smarty->assign('BasTarih',$BasTarih);
	$smarty->assign('BitTarih',$BitTarih);
	$smarty->assign('KapidaOdeme',$KapidaOdeme);
	
?>
