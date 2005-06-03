<?
// {{{ Sayfa Siliniyor
if($get_SSayfa&&YetkiKontrol('SayfaSilme'))
	{
	sorgula("DELETE FROM KullaniciSayfalar WHERE SayfaIsim='$get_SSayfa'");
	}
// }}}
// {{{ Yeni Sayfa Ekleniyor
if($post_YeniSayfa&&YetkiKontrol('YeniSayfaEkleme'))
	{
	$Sorgu1 = sorgula("SELECT SayfaIsim FROM KullaniciSayfalar WHERE SayfaIsim='$post_YeniSayfa'");
	if($Sorgu1->numRows() != 0)
		$smarty->assign('Uyari','Belirttiðiniz isimde bir sayfa zaten mevcut');
	else	{
		$Sorgu1 = sorgula("SELECT BolumIsim,Satir,Sutun FROM KullaniciSayfalar WHERE SayfaIsim='Anasayfa'");
		while(list($BolumIsim,$Satir,$Sutun) = getir($Sorgu1))
			{
			if($BolumIsim=='Anasayfa')
			 	sorgula("INSERT INTO KullaniciSayfalar SET SayfaIsim='$post_YeniSayfa',Satir='$Satir',Sutun='$Sutun',BolumIsim='$post_YeniSayfa'");
			else 	sorgula("INSERT INTO KullaniciSayfalar SET SayfaIsim='$post_YeniSayfa',Satir='$Satir',Sutun='$Sutun',BolumIsim='$BolumIsim'");
			}
		$get_Sayfa = $post_YeniSayfa;
		}
	}
// }}}
// {{{ Sayfadan bolum cikariliyor
if($get_SBolum&&YetkiKontrol('BolumSilme'))
	{
          SayfadanBolumSil($get_SBolum);
	}
// }}}
// {{{ Bolum yer degistiriyor
if($get_YBolum&&YetkiKontrol('BolumYerDegistirme'))
	{
	$Sorgu1 = sorgula("SELECT SayfaIsim,Sutun,Satir FROM KullaniciSayfalar WHERE No='$get_YBolum'");
	list($SayfaIsim,$Sutun,$Satir) = getir($Sorgu1);
	if($Satir > 1)
		{
		$UstSatir = $Satir-1;
		sorgula("UPDATE KullaniciSayfalar SET Satir='$Satir' WHERE Sutun='$Sutun' AND SayfaIsim='$SayfaIsim' AND Satir='$UstSatir'");
		sorgula("UPDATE KullaniciSayfalar SET Satir='$UstSatir' WHERE No='$get_YBolum'");
		}
	}
if($get_ABolum&&YetkiKontrol('BolumYerDegistirme'))
	{
	$Sorgu1 = sorgula("SELECT SayfaIsim,Sutun,Satir FROM KullaniciSayfalar WHERE No='$get_ABolum'");
	list($SayfaIsim,$Sutun,$Satir) = getir($Sorgu1);
	$Sorgu1 = sorgula("SELECT MAX(Satir) FROM KullaniciSayfalar WHERE SayfaIsim='$SayfaIsim' AND Sutun='$Sutun'");
	list($SonSatir) = getir($Sorgu1);
	if($Satir < $SonSatir)
		{
		$AltSatir = $Satir+1;
		sorgula("UPDATE KullaniciSayfalar SET Satir='$Satir' WHERE Sutun='$Sutun' AND SayfaIsim='$SayfaIsim' AND Satir='$AltSatir'");
		sorgula("UPDATE KullaniciSayfalar SET Satir='$AltSatir' WHERE No='$get_ABolum'");
		}
	}
// }}}
// {{{ Sayfaya Bolum Ekleniyor
if($post_YeniBolum&&YetkiKontrol('YeniBolumEkleme'))
	{
	$SonSutun = 1;
	$SonSatir = 1;
	if($post_YeniSutun < 1)
		$post_YeniSutun = 1;
	if($post_YeniSatir < 1)
		$post_YeniSatir = 1;
	$Sorgu1 = sorgula("SELECT Sutun FROM KullaniciSayfalar WHERE SayfaIsim='$get_Sayfa'");
	while(list($Sutun) = getir($Sorgu1))
		if($Sutun > $SonSutun)
			$SonSutun = $Sutun;
	if($post_YeniSutun > $SonSutun)
		{
		$Sutun = $SonSutun+1;
		$Satir = 1;
		}
	else	{
		$SonSatir = 1;
		$Sutun = $post_YeniSutun;
		$Sorgu1 = sorgula("SELECT Satir FROM KullaniciSayfalar WHERE SayfaIsim='$get_Sayfa' AND Sutun='$Sutun'");
		while(list($Satir) = getir($Sorgu1))
			if($Satir > $SonSatir)
				$SonSatir = $Satir;
		if($post_YeniSatir > $SonSatir)
			$Satir = $SonSatir+1;
		else	$Satir = $post_YeniSatir;
		}
	sorgula("UPDATE KullaniciSayfalar SET Satir=Satir+1 WHERE SayfaIsim='$get_Sayfa' AND Sutun='$Sutun' AND Satir >= '$Satir'");
	sorgula("INSERT INTO KullaniciSayfalar SET SayfaIsim='$get_Sayfa',BolumIsim='$post_YeniBolum',Sutun='$Sutun',Satir='$Satir'");

        if ($post_TumSayfalardaOlsun=='Evet')
        {
          ///{{{Modül tüm sayfalara ekleniyor
          $Sql = "SELECT DISTINCT(SayfaIsim) FROM KullaniciSayfalar WHERE SayfaIsim<>'$get_Sayfa'";     
          $Sonuc = sorgula($Sql);
          while(list($SayfaIsim)=getir($Sonuc))
          {
              $SonSutun = 1;
              $SonSatir = 1;
              if($post_YeniSutun < 1)
                 $post_YeniSutun = 1;
              if($post_YeniSatir < 1)
                 $post_YeniSatir = 1;
              $Sorgu1 = sorgula("SELECT Sutun FROM KullaniciSayfalar WHERE SayfaIsim='$SayfaIsim'");
              while(list($Sutun) = getir($Sorgu1))
                 if($Sutun > $SonSutun)
                        $SonSutun = $Sutun;
                 if($post_YeniSutun > $SonSutun)
                 {
                    $Sutun = $SonSutun+1;
                    $Satir = 1;
                 }
                 else    
                 {
                   $SonSatir = 1;
                   $Sutun = $post_YeniSutun;
                   $Sorgu1 = sorgula("SELECT Satir FROM KullaniciSayfalar WHERE SayfaIsim='$SayfaIsim' AND Sutun='$Sutun'");
                   while(list($Satir) = getir($Sorgu1))
                        if($Satir > $SonSatir)
                                $SonSatir = $Satir;
                   if($post_YeniSatir > $SonSatir)
                           $Satir = $SonSatir+1;
                   else    $Satir = $post_YeniSatir;
                }
               sorgula("UPDATE KullaniciSayfalar SET Satir=Satir+1 WHERE SayfaIsim='$SayfaIsim' AND Sutun='$Sutun' AND Satir >= '$Satir'");
               sorgula("INSERT INTO KullaniciSayfalar SET SayfaIsim='$SayfaIsim',BolumIsim='$post_YeniBolum',Sutun='$Sutun',Satir='$Satir'");
          }//while
          //}}}
        }//if
   }
// }}}
// {{{ Kayitli Sayfalar
$Sayfalar = array();
$Sorgu1 = sorgula("SELECT DISTINCT SayfaIsim FROM KullaniciSayfalar ORDER BY SayfaIsim");
while(list($vt_SayfaIsim) = getir($Sorgu1))
	$Sayfalar[] = $vt_SayfaIsim;
$smarty->assign('Sayfalar',$Sayfalar);
// }}}
// {{{ Sayfa Bolumleri
if($get_Sayfa)
	{
	$Bolumler = array();
	$SonSutun = 1;
	$SonSatir = 1;
	$Sorgu1 = sorgula("SELECT No,BolumIsim,Sutun,Satir FROM KullaniciSayfalar WHERE SayfaIsim='$get_Sayfa' ORDER BY Sutun,Satir");
	while(list($vt_No,$vt_BolumIsim,$vt_Sutun,$vt_Satir) = getir($Sorgu1))
		{
		$Bolumler[$vt_Sutun][$vt_Satir]['Satir'] = $vt_Satir;
		$Bolumler[$vt_Sutun][$vt_Satir]['No'] = $vt_No;
		$Bolumler[$vt_Sutun][$vt_Satir]['Isim'] = $vt_BolumIsim;
		if($vt_Sutun > $SonSutun)
			$SonSutun = $vt_Sutun;
		if($vt_Satir > $SonSatir)
			$SonSatir = $vt_Satir;
		}
	$smarty->assign('Bolumler',$Bolumler);
	$smarty->assign('SecilenSayfa',$get_Sayfa);
	$smarty->assign('SutunGenislik',100/$SonSutun);
	// {{{ Kayitli Bolumler
	$Bolumler = array();
	$Dizin = opendir($INI_TemplateDizin);
	while($Dosya = readdir($Dizin))
		{
		if($Dosya == '.' || $Dosya == '..')
			continue;
		$Uzanti = substr(strrchr($Dosya,'.'),1);
		if(is_dir($INI_TemplateDizin.'/'.$Dosya))
			{
			$Dizin2 = opendir($INI_TemplateDizin.'/'.$Dosya);
			while($Dosya2 = readdir($Dizin2))
				{
				$Uzanti = substr(strrchr($Dosya2,'.'),1);
				if($Uzanti!='tpl')
					continue;
				$Bolumler[$Dosya.'/'.substr($Dosya2,0,strlen($Dosya2)-4)] = $Dosya.' / '.substr($Dosya2,0,strlen($Dosya2)-4);
				}
			continue;
			}
		if($Uzanti!='tpl')
			continue;
		$Bolumler[substr($Dosya,0,strlen($Dosya)-4)] = substr($Dosya,0,strlen($Dosya)-4);
		}
	asort($Bolumler);
		
	$smarty->assign('YeniBolumler',$Bolumler);
	
	// }}}
	// {{{ Sutunlar - Satirlar
	$SonSutun++;
	$SonSatir++;
	for($i=1;$i<=$SonSutun && $i<=3;$i++)
		$YeniSutunlar[$i] = $i;
	$smarty->assign('YeniSutunlar',$YeniSutunlar);
	for($i=1;$i<=$SonSatir;$i++)
		$YeniSatirlar[$i] = $i;
	$smarty->assign('YeniSatirlar',$YeniSatirlar);
	// }}}
	}
// }}}
// {{{ Sayfanýn Üyelik Durumunu Belirle
if($post_UyelikDurum&&YetkiKontrol('SayfaUyelikZorunlu')){
	sorgula("UPDATE KullaniciSayfalar SET UyelikDurum='$post_UyelikDurum' WHERE SayfaIsim='$get_Sayfa'");
}
$sayfasorgu = "SELECT No,UyelikDurum FROM KullaniciSayfalar WHERE SayfaIsim='$get_Sayfa'";
$sonucsayfa=sorgula($sayfasorgu);
list($vt_No,$vt_UyelikDurum)=getir($sonucsayfa);
$smarty->assign('UyelikDurum',$vt_UyelikDurum);
// }}}	
?>
