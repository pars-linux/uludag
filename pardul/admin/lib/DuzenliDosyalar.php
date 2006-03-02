<?
// {{{ Kayitli Dosyalar
$Sorgu1 = sorgula("SELECT No,Isim FROM crontab ORDER BY Isim");
for($i=0;list($No,$Isim) = getir($Sorgu1);$i++)
	{
	$DuzenliDosyalar[$i]['No'] = $No;
	$DuzenliDosyalar[$i]['Isim'] = $Isim;
	}
$smarty->assign('DuzenliDosyalar',$DuzenliDosyalar);
// }}}
// {{{ Zaman Araliklar
for($i=1;$i<=60;$i+=1)
	$DakikaZamanAraliklar[$i] = $i;
for($i=1;$i<=24;$i++)
	$SaatZamanAraliklar[$i] = $i;
$smarty->assign('DakikaZamanAraliklar',$DakikaZamanAraliklar);
$smarty->assign('SaatZamanAraliklar',$SaatZamanAraliklar);

for($i=0;$i<24;$i++)
	{
	if($i<10)	$HerGunSaatler[$i] = "0".$i;
	else		$HerGunSaatler[$i] = $i;
	}
$smarty->assign('HerGunSaatler',$HerGunSaatler);
for($i=0;$i<60;$i++)
	{
	if($i<10)	$HerGunDakikalar[$i] = "0".$i;
	else		$HerGunDakikalar[$i] = $i;
	}
$smarty->assign('HerGunDakikalar',$HerGunDakikalar);
// }}}

// {{{ Bilgiler Guncelleniyor
if($post_Guncelle&&YetkiKontrol('DuzenliDosyaGuncelleme'))
	{
	$Sorgu1 = sorgula("SELECT SonCalisma FROM crontab WHERE No='$get_Dosya'");
	if(list($SonCalisma) = $Sorgu1->fetchRow())
		{
		if($post_AktifPasif == "1")	$AktifPasif = 'Aktif';
		else				$AktifPasif = 'Pasif';
		if($post_CalismaZaman == 'HerGun')
			{
			$BugunDakika = floatval(date("H"))*60+floatval(date("i"));
			$IstenilenDakika = floatval($post_HerGunSaat)*60+($post_HerGunDakika);
			$ZamanAralik = 24*60*60;
			$CalismaSaniye = mktime($post_HerGunSaat,$post_HerGunDakika,"00",date("m"),date("d"),date("Y"));
			if($IstenilenDakika >= $BugunDakika)
				$CalismaSaniye-= (24*60*60);		// Dun belirtilen saat
			$SonCalisma = date("YmdHis",$CalismaSaniye);
			}
		else if($post_CalismaZaman == 'SaatteBir')
			{
			$ZamanAralik = $post_SaatteBir*60*60;
			}
		else if($post_CalismaZaman == 'DakikadaBir')
			{
			$ZamanAralik = $post_DakikadaBir*60;
			}
		sorgula("UPDATE crontab SET AktifPasif='$AktifPasif',SonCalisma='$SonCalisma',ZamanAralik='$ZamanAralik' WHERE No='$get_Dosya'");
		}
	}
// }}}
// {{{ Bilgiler Cekiliyor
if($get_Dosya)
	{
	$Sorgu1 = sorgula("SELECT AktifPasif,Isim,Dosya,Aciklama,SonCalisma,ZamanAralik FROM crontab WHERE No='$get_Dosya'");
	if(list($AktifPasif,$Isim,$Dosya,$Aciklama,$SonCalisma,$ZamanAralik) = $Sorgu1->fetchRow())
		{
		$Bilgiler['No'] = $get_Dosya;
		$Bilgiler['AktifPasif'] = $AktifPasif;
		$Bilgiler['Isim'] = $Isim;
		$Bilgiler['Dosya'] = $Dosya;
		$Bilgiler['Aciklama'] = $Aciklama;

		if($Bilgiler['AktifPasif']=='Aktif')
			$Bilgiler['Aktif'] = true;
		else	$Bilgiler['Aktif'] = false;

		if($ZamanAralik < (60*60))		// Bir Saatten Az
			{
			$ZamanAralik/=60;
			$Bilgiler['DakikadaBirAralik'] = $ZamanAralik;
			$Bilgiler['DakikadaBir'] = true;
			}
		else if($ZamanAralik < (60*60*24))	// Bir Gunden Az
			{
			$ZamanAralik/=(60*60);
			$Bilgiler['SaatteBirAralik'] = $ZamanAralik;
			$Bilgiler['SaatteBir'] = true;
			}
		else					// Hergun
			{
			$SonSaat = substr($SonCalisma,8,2);
			$SonDakika = substr($SonCalisma,10,2);
			$Bilgiler['HerGunSaat'] = $SonSaat;
			$Bilgiler['HerGunDakika'] = $SonDakika;
			$Bilgiler['HerGun'] = true;
			}
		

		// Calisma Zamanlari Listeleniyor
		if(!$post_ListeTur)
			{
			$post_ListeTur = 'Defa';
			$post_DefaSayi = 10;
			}
		if($post_ListeTur == 'Gun')
			{
			$Bilgiler['ListeTur'] = 'Gun';
			$Bilgiler['GunSayi'] = $post_GunSayi;
			$GunSayi = intval($post_GunSayi);
			$Saniye  = mktime(date("H"),date("i"),date("s"),date("m"),date("d"),date("Y"))-$GunSayi*24*60*60;
			$IlkZaman = date("YmdHis",$Saniye);
			$SorguEk = " AND Zaman > '$IlkZaman' ORDER BY Zaman DESC";
			}
		else if($post_ListeTur == 'Defa')
			{
			$Bilgiler['ListeTur'] = 'Defa';
			$Bilgiler['DefaSayi'] = $post_DefaSayi;
			$DefaSayi = intval($post_DefaSayi);
			$SorguEk = " ORDER BY Zaman DESC LIMIT 10";
			}
		$Sorgu1 = sorgula("SELECT Zaman FROM cronlog WHERE Dosya='$Dosya' $SorguEk");
		for($i=0;list($Zaman) = $Sorgu1->fetchRow();$i++)
			{
			$Bilgiler['Calismalar'][$i] = tarihgetir($Zaman,"tamgun");
			}
		$smarty->assign('Bilgiler',$Bilgiler);
		}
	}
// }}}
?>
