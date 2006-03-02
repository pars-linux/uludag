<?
error_reporting(E_WARNING || E_PARSE);

if ($post_BaslikGuncelle)
{
  $DuzenlenenKategoriNo = $get_DuzenleKatNo;
  if ($YeniBaslik)
  {
    if(!KayitKontrol('KategoriOzellikBasliklar','KategoriNo',$DuzenlenenKategoriNo,'Ad',$post_YeniBaslik))
    {
      $Sql = "INSERT INTO KategoriOzellikBasliklar SET KategoriNo='$DuzenlenenKategoriNo',Ad='$post_YeniBaslik'";
      sorgula($Sql);
    } 
    else $Uyari  = 'Eklemek istediðiniz kategori özellik baþlýðý mevcut!';
   }
   else
   {
      $Sql = "SELECT No FROM KategoriOzellikBasliklar WHERE KategoriNo='$DuzenlenenKategoriNo'";
      $Sonuc = sorgula($Sql);
      while(list($No)=getir($Sonuc))
      {
        $YeniAd = ${'Baslik'.$No};
        if ($YeniAd)
         sorgula("UPDATE KategoriOzellikBasliklar SET Ad='$YeniAd' WHERE No='$No'"); 
      } 
   }
}

if ($get_DuzenleKatNo)
{
  if ($get_SilBaslikNo) //baþlýk siliniyor
  {
    $Sql = "DELETE FROM KategoriOzellikBasliklar WHERE No='$get_SilBaslikNo'";
    sorgula($Sql);
  }
  $Sql = "SELECT No,Ad FROM KategoriOzellikBasliklar WHERE KategoriNo='$get_DuzenleKatNo'";
  $Sonuc = sorgula($Sql);
  $i = 0;
  while(list($BaslikNo,$BaslikAd)=getir($Sonuc))
  {
    $KategoriOzellikBasliklar[$i]['No'] = $BaslikNo;
    $KategoriOzellikBasliklar[$i]['Ad'] = $BaslikAd;
    $i++;
  }
  $smarty->assign('KategoriOzellikBasliklar',$KategoriOzellikBasliklar);
}



if($post_Ad)
	{
	// Eðer baþýnda flt_ varsa Alan adi sadece harf,sayi ve _ icerebilir.
	if(strncmp($post_Ad,'flt_',4)<>0    /*!ereg("flt_",$post_Ad)*/){
	$post_Ad = Turkcesiz(strtolower($post_Ad));
	$post_Ad = eregi_replace("[^a-z0-9]","",$post_Ad);
	}else{ $post_Ad = Turkcesiz(strtolower($post_Ad)); }
	}
// include("$AdminAnaDizin/fonksiyonlar/kategori.php");
if ($get_KatNo)
{
  $Sql = "SELECT KatAd FROM UrunKategoriler WHERE No='$get_KatNo'";
  $Sonuc = sorgula($Sql);
  list($vt_KatAd) = getir($Sonuc);
  $smarty->assign('KategoriAd',$vt_KatAd);
}


// {{{ Alan Duzenleme Bilgileri
$DuzenleAlan = array();
if($get_DuzenleAlan)
	{
	$Sonuc = sorgula("SELECT TabloAd FROM UrunKategoriler WHERE No='$get_KatNo'");
        list($vt_TabloAd) = getir($Sonuc);
	$Sorgu1 = sorgula("SELECT * FROM $vt_TabloAd");
	$Alanlar = $Sorgu1->tableInfo();
	
	$AlanSayisi = $Sorgu1->numCols();
	for($i=0;$i<$AlanSayisi;$i++)
		{
		if($Alanlar[$i]['name']==$get_DuzenleAlan)
			{
				
			$DuzenleAlan['Ad'] = $Alanlar[$i]['name'];
			$DuzenleAlan['Boyut'] = $Alanlar[$i]['len'];
			// tableInfo() fonksiyonundan gelen blob u text e çevirir   (gokhan ekledi)
			if($Alanlar[$i]['type']==='blob'){
			$Alanlar[$i]['type']='text';	
			}//bitti
			$DuzenleAlan['Tur'] = $Alanlar[$i]['type'];
			if($DuzenleAlan['Tur']=='int' && $DuzenleAlan['Boyut']<3)
				$DuzenleAlan['Tur'] = 'TINYINT';
			else if($DuzenleAlan['Tur']=='int')
				$DuzenleAlan['Tur'] = 'INT';
			else if($DuzenleAlan['Tur'] =='real')
				$DuzenleAlan['Tur'] = 'FLOAT';
			else if($DuzenleAlan['Tur'] == 'string' && $DuzenleAlan['len']<255)
				$DuzenleAlan['Tur'] = 'VARCHAR';
			else if($DuzenleAlan['Tur'] == 'text')	{ $DuzenleAlan['Tur'] = 'TEXT'; $DuzenleAlan['Boyut'] ="";} //Sonradan Eklendi-Gokhan
		
			}
		}
	$smarty->assign('DuzenleAlan',$DuzenleAlan);
	}
// }}}
// {{{ Alan Turleri
$AlanTurler['VARCHAR'] = 'VARCHAR';
$AlanTurler['TINYINT'] = 'TINYINT';
$AlanTurler['INT'] = 'INT';
$AlanTurler['FLOAT'] = 'FLOAT';
$AlanTurler['TEXT'] = 'TEXT';
$smarty->assign('AlanTurler',$AlanTurler);
// }}}

// {{{ Kategori Sil
if($get_SilKatNo&&YetkiKontrol('UrunKategoriSilme'))
	{
	if(KategoriSil($get_SilKatNo)<>"KategoriSilBasarili")
		$Uyari = "Geçersiz bir kategori silinemez!";
	}
// }}}
// {{{Kategori Ekle
if($post_KatAd&&YetkiKontrol('UrunKategoriEkleme'))
	{
	$IslemUyari = KategoriOlustur($post_KatAd);
	if($IslemUyari<>'KategoriEkleBasarili')
	   $Uyari = $IslemUyari;
	}
else if($post_KategoriEkle)
	$IslemUyari = $ceviri['GecersizTabloKategori'];
// }}}

// {{{ Kategori Bilgileri Guncelleniyor
if($post_DuzenleKatNo)
{
	$IslemUyari = KategoriDuzenle($post_DuzenleKatAd,$post_DuzenleKatNo);
	if($IslemUyari<> 'KategoriDuzenleBasarili')
	   $Uyari = $IslemUyari;
	$get_DuzenleKatNo = $post_DuzenleKatNo;
}
// }}}

// {{{ Kategori Guncelle
if($post_KatNo)
	{
	$Sonuc = sorgula("SELECT TabloAd,AlanSirasi FROM UrunKategoriler WHERE No='$post_KatNo'");
        list($vt_TabloAd,$vt_AlanSirasi) = getir($Sonuc); 
	$sorgu1 = sorgula("SELECT $vt_AlanSirasi FROM $vt_TabloAd");
	$AlanSayisi = $sorgu1->numCols();
	$Alanlar = $sorgu1->tableInfo();
	$GorunenIsim = array();
	$SonEk = array();
	$GirisNot = array();
	$FiltreAlan = array();
	$ListeAlan = array();
	for($i=0;$i<$AlanSayisi;$i++)
		{
		$AlanAdi = $Alanlar[$i]['name'];
		$GorunenIsim[] = ${"post_GorunenIsim$AlanAdi"};
		$SonEk[] = ${"post_SonEk$AlanAdi"};
		$GirisNot[] = ${"post_GirisNot$AlanAdi"};
		if(${"post_FiltreAlan$AlanAdi"})	$FiltreAlan[] = $AlanAdi;
		if(${"post_ListeAlan$AlanAdi"})	$ListeAlan[] = $AlanAdi;
		}
	$GorunenIsim = implode("##",$GorunenIsim);
	$SonEk = implode("##",$SonEk);
	$GirisNot = implode("##",$GirisNot);
	$FiltreAlanlar = implode("##",$FiltreAlan);
	$ListeAlanlar = implode("##",$ListeAlan);
	$IslemUyari = KategoriGuncelle($post_KatNo,$GorunenIsim,$SonEk,$GirisNot,$FiltreAlanlar,$ListeAlanlar);
	if($IslemUyari<>'BilgiGuncelBasarili')
	   $Uyari = 'Bilgiler güncellenemedi!';
	}
// }}}
// {{{  Alan Ekle
if($post_AlanTipi && !$post_DuzenleAlan && YetkiKontrol('UrunKategoriAlanEkleme'))
	{
	$IslemUyari = AlanEkle($get_KatNo,$post_Ad,$post_AlanBoyut,$post_AlanTipi,$post_Varsayilan);
	if($IslemUyari<>'AlanEkleBasarili')
           $Uyari = $IslemUyari;
	}
else if($post_AlanTipi && !$post_DuzenleAlan)	$Uyari = '';
// }}}
// {{{ AlanDuzenle
if($post_DuzenleAlan && YetkiKontrol('UrunKategoriAlanDuzenleme'))
	{
	$IslemUyari = AlanDuzenle($post_DuzenleAlan,$get_KatNo,$post_Ad,$post_AlanBoyut,$post_AlanTipi,$post_Varsayilan);
	if($IslemUyari<>'AlanDuzenleBasarili')
	    $Uyari = $IslemUyari;
	}
else if($post_AlanTipi && $post_DuzenleAlan)	$Uyari = '';
// }}}
// {{{ Alan Sil
if($get_SilAlan && YetkiKontrol('UrunKategoriAlanSilme'))
	{
	$IslemUyari = AlanSil($get_KatNo,$get_SilAlan);
	if($IslemUyari<>'AlanSilBasarili')
	   $Uyari = $IslemUyari;
	}
// }}}
// {{{ Alan Yukari - Asagi
if(($get_YukariAlan || $get_AsagiAlan)&& YetkiKontrol('UrunKategoriAlanSiralama'))
{
		$Dizi_AlanIsimler = array();

		$Sorgu1 = sorgula("SELECT TabloAd,AlanSirasi,GorunenIsim,SonEk,GirisNot,FiltreAlanlar,ListeAlanlar FROM UrunKategoriler WHERE No='$get_KatNo'");
		list($TabloAd,$AlanSirasi,$GorunenIsim,$SonEk,$GirisNot,$FiltreAlanlar,$ListeAlanlar) = getir($Sorgu1);
		$Dizi_AlanSirasi = explode(",",$AlanSirasi);
		$Dizi_GorunenIsim = explode("##",$GorunenIsim);
		$Dizi_SonEk = explode("##",$SonEk);
		$Dizi_GirisNot = explode("##",$GirisNot);
		$Sorgu1 = sorgula("SELECT $AlanSirasi FROM $TabloAd");
		$AlanSayisi = $Sorgu1->numCols();
		$Alanlar = $Sorgu1->tableInfo();
		foreach($Alanlar as $Alan)
			$Dizi_AlanIsimler[] = $Alan['name'];
		if($get_YukariAlan)
			{
			for($i=1;$i<$AlanSayisi;$i++)	// Ilk alan yukari tasinamayacagindan 1 den basliyoruz
				{
				if($get_YukariAlan == $Dizi_AlanIsimler[$i]) // Bu alan yukari tasinacak ...
					{
					$Gecici = $Dizi_AlanSirasi[$i-1];
					$Dizi_AlanSirasi[$i-1] = $Dizi_AlanSirasi[$i];
					$Dizi_AlanSirasi[$i] = $Gecici;
	
					$Gecici = $Dizi_GorunenIsim[$i];
					$Dizi_GorunenIsim[$i] = $Dizi_GorunenIsim[$i-1];
					
					$Dizi_GorunenIsim[$i-1] = $Gecici;
	
					$Gecici = $Dizi_SonEk[$i];
					$Dizi_SonEk[$i] = $Dizi_SonEk[$i-1];
					$Dizi_SonEk[$i-1] = $Gecici;
	
					$Gecici = $Dizi_GirisNot[$i];
					$Dizi_GirisNot[$i] = $Dizi_GirisNot[$i-1];
					$Dizi_GirisNot[$i-1] = $Gecici;
					}
				}
			}
		else
			{
			for($i=0;$i<$AlanSayisi-1;$i++)	// Son alan asagi tasinamayacagindan 1 eksige kadar gidiyoruz
				{
				if($get_AsagiAlan == $Dizi_AlanIsimler[$i]) // Bu alan asagi tasinacak ...
					{
					$Gecici = $Dizi_AlanSirasi[$i+1];
					$Dizi_AlanSirasi[$i+1] = $Dizi_AlanSirasi[$i];
					$Dizi_AlanSirasi[$i] = $Gecici;
	
					$Gecici = $Dizi_GorunenIsim[$i];
					$Dizi_GorunenIsim[$i] = $Dizi_GorunenIsim[$i+1];
					$Dizi_GorunenIsim[$i+1] = $Gecici;
	
					$Gecici = $Dizi_SonEk[$i];
					$Dizi_SonEk[$i] = $Dizi_SonEk[$i+1];
					$Dizi_SonEk[$i+1] = $Gecici;
	
					$Gecici = $Dizi_GirisNot[$i];
					$Dizi_GirisNot[$i] = $Dizi_GirisNot[$i+1];
					$Dizi_GirisNot[$i+1] = $Gecici;
					}
				}
			}
		$GirisNot = implode("##",$Dizi_GirisNot);
		$SonEk = implode("##",$Dizi_SonEk);
		$GorunenIsim = implode("##",$Dizi_GorunenIsim);
		$AlanSirasi = implode(",",$Dizi_AlanSirasi);
		sorgula("UPDATE UrunKategoriler SET AlanSirasi='$AlanSirasi',GorunenIsim='$GorunenIsim',SonEk='$SonEk',GirisNot='$GirisNot' WHERE No='$get_KatNo'");

		// Alan sirasi degisince UrunKategorilerMenu tablosu
		$Sorgu1 = sorgula("SELECT $AlanSirasi FROM $TabloAd");
		$Alanlar = $Sorgu1->tableInfo();
		$AlanSira = 1;
		foreach($Dizi_AlanSirasi as $i => $Alan)
			{
			$AlanIsim = $Alanlar[$i]['name'];
			$AlanSiraIsim = 'Alan'.$AlanSira;
			sorgula("UPDATE UrunKategorilerMenu SET AlanSira='$AlanSiraIsim' WHERE KategoriNo='$get_KatNo' AND AlanAd='$AlanIsim'");
			$AlanSira ++;
			}
	}
// }}}




// {{{ Kayitli Kategoriler
$Kategoriler = KategoriListele();
$smarty->assign('Kategoriler',$Kategoriler);
// }}}
// {{{ Kategori Detaylar
if($get_KatNo)
	{
	$Sonuc = sorgula("SELECT TabloAd,AlanSirasi,GorunenIsim,SonEk,GirisNot,FiltreAlanlar,ListeAlanlar FROM UrunKategoriler WHERE No='$get_KatNo'");
        list($vt_TabloAd,$vt_AlanSirasi,$vt_GorunenIsim,$vt_SonEk,$vt_GirisNot,$vt_FiltreAlanlar,$vt_ListeAlanlar) = getir($Sonuc);
	if($vt_AlanSirasi)
		$vt_AlanSirasi = ",".$vt_AlanSirasi;
	$Sorgu = "SELECT UrunNo$vt_AlanSirasi FROM $vt_TabloAd";
	$sorgu1 = sorgula($Sorgu);
	$AlanSayisi = $sorgu1->numCols();
	$Alanlar = $sorgu1->tableInfo();
	
	$SonEkler = explode("##",$vt_SonEk);
	$GorunenIsimler = explode("##",$vt_GorunenIsim);
	$GirisNotlari = explode("##",$vt_GirisNot);
	$FiltreAlanlar = explode("##",$vt_FiltreAlanlar);
	$ListeAlanlar = explode("##",$vt_ListeAlanlar);
	for($i=1;$i<$AlanSayisi;$i++)	// ilk alan varsayilan ortak birincil anahtar = no , atlaniyor
		{
			
		$Alanlar[$i]['gorunen_isim'] = $GorunenIsimler[$i-1];
		$Alanlar[$i]['son_ek'] = $SonEkler[$i-1];
		$Alanlar[$i]['giris_notu'] = $GirisNotlari[$i-1];
		if(is_array($FiltreAlanlar) && count($FiltreAlanlar) && in_array($Alanlar[$i]['name'],$FiltreAlanlar))
			$Alanlar[$i]['Filtre'] = true;
		else	$Alanlar[$i]['Filtre'] = false;
		if(is_array($ListeAlanlar) && count($ListeAlanlar) && in_array($Alanlar[$i]['name'],$ListeAlanlar))
			$Alanlar[$i]['Liste'] = true;
		else	$Alanlar[$i]['Liste'] = false;
		}

	$smarty->assign("KatNo",$get_KatNo);
	}
// }}}
// {{{ Kategori Duzenleme Bilgileri
if($get_DuzenleKatNo)
	{
	$Sonuc = sorgula("SELECT KatAd FROM UrunKategoriler WHERE No='$get_DuzenleKatNo'");
        list($vt_KatAd) = getir($Sonuc);
	$Duzenle['KatAd'] = $vt_KatAd;
	$smarty->assign('Duzenle',$Duzenle);
	$smarty->assign('DuzenleKatNo',$get_DuzenleKatNo);
	}
// }}}
///////////////////////
 
$smarty->assign('Alanlar',$Alanlar);
$smarty->assign('AlanSayisi',$AlanSayisi);
$smarty->assign('Uyari',$Uyari);


?>
