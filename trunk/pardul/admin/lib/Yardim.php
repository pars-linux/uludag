<?
	$Sql = "SELECT No,Isim FROM YonetimMenu WHERE AnaNo=0 AND No<>1";
	$Sonuc = sorgula($Sql);
	$i = 0;
	while(list($No,$Isim) = getir($Sonuc)) {
		$AnaSayfalar[$i]['No']   = $No;
		$AnaSayfalar[$i]['Isim'] = $Isim;
		$SqlAlt = "SELECT No,Isim,Adres FROM YonetimMenu WHERE AnaNo=$No AND IslemKod=''";
		$SonucAlt = sorgula($SqlAlt);
        $j = 0;
		while(list($AltNo,$AltIsim,$AltAdres) = getir($SonucAlt)) {
			$AltSayfalar[$j]['No']    = $AltNo;
			$AltSayfalar[$j]['Isim' ] = $AltIsim;
			$AltSayfalar[$j]['Adres'] = $AltAdres;
            $SqlYardim = "SELECT Metin FROM Yardim WHERE Sayfa='$AltAdres'";
			$SonucYardim = sorgula($SqlYardim);
			list($Metin) = getir($SonucYardim);
			$AltSayfalar[$j]['Metin'] = nl2br($Metin);
			$j++;
		}
		$AnaSayfalar[$i]['AltSayfalar'] = $AltSayfalar;
		$i++;
	}
	$smarty->assign('AnaSayfalar',$AnaSayfalar);
?>
