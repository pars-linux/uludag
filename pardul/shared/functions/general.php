<?
  /**
   *   functions/general.php
   *   This is a good place for shared functions which will be used in both user and admin interfeces.
   *   @package shared_functions
   *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
   *   @todo internal variable names should be renamed in order to u18a purposes.
   */

   /**
    *   Looks for the given URL, is it valid?
    *   @package shared_functions
    *   @param string $url
    *   @return bool
    */
    
    function urlExists($url)
    {
        $url = ereg_replace("http://", "", $url);
        list($domain, $file) = explode("/", $url, 2);
        $fid=fsockopen($domain,80);
        $Cumle = "GET /$file HTTP/1.0\r\nHost: $domain\r\n\r\n";
        fputs($fid,$Cumle);
        $gets = fgets($fid, 1024);
        fclose($fid);
        if (ereg("HTTP/1.1 200 OK", $gets))
        {
            return TRUE;
        }
        else
        {
            return FALSE;
        }
    }

   /**
    *   Uses PEAR and to query an SQL, this is a practical and shorthand method
    *   which is used for all queries. It includes its formatted error returns as well.
    *   @package shared_functions
    *   @global $vt Database used.
    *   @param string $Sorgu
    *   @see getir()
    *   @return array
    */

    function sorgula($Sorgu)
    {
        global $vt;
        $Sonuc = $vt->query($Sorgu);
        if(DB::isError($Sonuc))
        {
                echo $Sorgu;
                echo mysql_error();
                die($Sonuc->getMessage()."<br><font color=red>$Sorgu</font><br>");
        }
    return $Sonuc;
    }

   /**
    *   Uses PEAR to fetch result set from an already queried SQL, this is a practical and shorthand method
    *   which is used for all queries with function sorgula($Sonuc).
    *   Security Note: stripslashes is applied to all data fetched! No need to redo!
    *   @package shared_functions
    *   @param string $Sorgu
    *   @see sorgula()
    *   @return array
    */
    
    function getir($Sorgu,$FetchMode = '')
    {
	$Sonuc = $Sorgu->fetchRow($FetchMode);
	if(is_array($Sonuc) && count($Sonuc))
	foreach($Sonuc as $a => $b)
		$Sonuc[$a] = stripslashes($b);
	return $Sonuc;
    }

   /**
    *   Time as YmdHis.
    *   @package shared_functions
    *   @link http://php.net/date PHP date functions
    *   @return string
    */
    function Simdi()
    {
        $simdi=date("YmdHis");
        return $simdi;
    }
         
   /**
    *   Loks for a specific row, if exests, before DB INSERT
    *   @package shared_functions
    *   @param string $TabloAd
    *   @param string $AlanAd1
    *   @param string $AlanDeger1
    *   @param string $AlanAd2
    *   @param string $AlanDeger2
    *   @return bool
    */

    function KayitKontrol($TabloAd,$AlanAd1,$AlanDeger1,$AlanAd2="",$AlanDeger2="")
    {
        if (($AlanAd2=="")&&($AlanDeger2==""))
            $SqlKontrol = "SELECT * FROM $TabloAd WHERE $AlanAd1='$AlanDeger1'";
        else
            $SqlKontrol = "SELECT * FROM $TabloAd WHERE $AlanAd1='$AlanDeger1' AND $AlanAd2='$AlanDeger2'";
            $Sonuc = sorgula($SqlKontrol);
        if ($Sonuc->numRows()!=0)
            return 'Eklemek istediðiniz kayýt sistemde mevcut!';
        else
            return false;
    }

    /**
    *   Do not use MySQL date fields. Use Bigint for dates, for compatiliblity reasons.
    *   Here is a function to help you format bigint dates.
    *   We use javascript calendar with "." seperated dates.
    *   @package shared_functions
    *   @param string $Tarih
    *   @param string $Nasil
    *   @return integer
    */

    function TarihDonustur($Tarih,$Nasil="")
    {
        list($Gun,$Ay,$Yil) = explode(".",$Tarih);
        if ($Nasil) {
            $Donus = $Yil.$Ay.$Gun."245959";
        } else {
            $Donus = $Yil.$Ay.$Gun."000000";
        }
        return $Donus;
    }

    /**
    *   Uses Simdi() and reformats it.
    *   @package shared_functions
    *   @see Simdi()
    *   @param string $Tarih
    *   @param string $Format Can be one of (sade:default, gunay, acik, gun, tam, tamgun, dizi
    *   @param string $Ayrac
    *   @return mixed if $Format=dizi, returns array, else returns string
    */
    
    function TarihGetir($Tarih,$Format="sade",$Ayrac=".")
    {
        $Yil = substr($Tarih,0,4);
        $Ay = substr($Tarih,4,2);
        $Gun = substr($Tarih,6,2);
        $Saat = substr($Tarih,8,2);
        $Dakika = substr($Tarih,10,2);
        $Saniye = substr($Tarih,12,2);
        $MkTarih = mktime($Saat,$Dakika,$Saniye,$Ay,$Gun,$Yil);
        $AyAdi = strftime("%B",$MkTarih);
        $GunAdi = strftime("%A",$MkTarih);
        switch($Format)
        {
            case "sade": // 10.10.2003
                return $Gun.$Ayrac.$Ay.$Ayrac.$Yil;
                break;
            case "gunay":
                return $Gun." ".$AyAdi;
                break;
            case "acik": // 10 Ekim 2003
                return $Gun." ".$AyAdi." ".$Yil;
                break;
            case "gun": // 10 Ekim 2003 Cuma
                return $Gun." ".$AyAdi." ".$Yil." ".$GunAdi;
                break;
            case "tam": // 10.10.2003|14:06:32
                return $Gun.$Ayrac.$Ay.$Ayrac.$Yil."|".$Saat.":".$Dakika.":".$Saniye;
                break;
            case "tamgun":
                return intval($Gun)." ".$AyAdi." ".$Yil." ".$GunAdi." ".$Saat.":".$Dakika.":".$Saniye;
                break;
            case "dizi": //returns as array.
                $Dizi[]=$Yil;$Dizi[]=$Ay;
                $Dizi[]=$Gun;$Dizi[]=$Saat;
                $Dizi[]=$Dakika;$Dizi[]=$Saniye;
            return $Dizi;
            break;
        }
    
    }

    /**
    *   Todays date.
    *   @package shared_functions
    *   @return string
    */
    
    function Bugun()
    {
        $Bugun = date("d").'.'.date("m").'.'.date("Y");
        return $Bugun;
    }

    /**
    *   Uses Simdi() and reformats it.
    *   @package shared_functions
    *   @see Simdi()
    *   @param string $Tarih
    *   @param string $Format Can be one of (sade:default, gunay, acik, gun, tam, tamgun, dizi
    *   @param string $Ayrac
    *   @return mixed if $Format=dizi, returns array, else returns string
    */
    
    function UyariEkle($Mesaj)
    {
        $Simdi = Simdi();
        $Sql = "SELECT * FROM Uyarilar WHERE Mesaj='$Mesaj'";
        $Sonuc = sorgula($Sql);
        if ($Sonuc->numRows()>0) // ayný hatadan daha önce kaydedilmiþ sadece sayýyý artýralým
            $Sql = "UPDATE Uyarilar SET GerceklesmeSayi=GerceklesmeSayi+1,TarihSaat='$Simdi' WHERE Mesaj='$Mesaj'";
        else //an insert will occure
            $Sql = "INSERT INTO Uyarilar SET GerceklesmeSayi=1,Mesaj='$Mesaj',TarihSaat='$Simdi'";
        sorgula($Sql);
    }
    
    /**
    *   Calculates month=x days
    *   @package shared_functions
    *   @param integer $gelenay     which month
    *   @param integer $gelenyil which year
    *   @return integer
    */

    function kacgun($gelenay,$gelenyil)
    {
        if($gelenay==2) //Feb.
                if(($gelenyil%4) == 0)  $gun_sayisi = 29;
                else                    $gun_sayisi = 28;
        else if(($gelenay == 1) || ($gelenay == 3) || ($gelenay == 5) ||
        ($gelenay == 7) ||  ($gelenay == 8) ||  ($gelenay == 10) ||  ($gelenay == 12))
                $gun_sayisi = 31;
        else
                $gun_sayisi = 30;
        return $gun_sayisi;
    }

    /**
    *   Used to remove an obj. from an array
    *   @package shared_functions
    *   @param array $Dizi
    *   @param mixed $Deger
    *   @return array
    */
    
    function DizidenCikar(&$Dizi,$Deger)
    {
     for($i=0;$i<count($Dizi);$i++)
     {
       if ($Dizi[$i]==$Deger) {$SiraNo=$i;break;}
     }
     $Dizi = array_merge(array_splice($Dizi,0,$SiraNo),array_splice($Dizi,1));
    }

    /**
    *   Changes a string to not to include Turkish accents which are not included in latin1 charset.
    *   Use in password etc fields.
    *   @package shared_functions
    *   @param string $Gelen
    *   @return string
    */
    
    function Turkcesiz($Gelen)
    {
        $Donus = strtr($Gelen,"ÜÞÇÝÐüöþçýð","USCIGuoscig");
        return $Donus;
    }
    
    /**
    *   Random string generator.
    *   @package shared_functions
    *   @return mixed if $Format=dizi, returns array, else returns string
    */

    function Rastgele($HarfSayisi,$Ozel = "TamKarisik")
    {
	$TamKarisik = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvyxyz0123456789";
	$HarfKarisik = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvyxyz";
	$SayiKarisik = "0123456789";
	$BuyukKarisik = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	$KucukKarisik = "abcdefghijklmnopqrstuvyxyz";
	if($Ozel!= 'HarfKarisik' && $Ozel!='SayiKarisik' && $Ozel!='BuyukKarisik' && $Ozel!='KucukKarisik')
		$Ozel = 'TamKarisik';
	$Sonuc = "";
	$DiziIsim = ${$Ozel};
	for($i=0;$i<$HarfSayisi;$i++)
		$Sonuc.=$DiziIsim[rand(0,strlen($DiziIsim)-1)];
	return $Sonuc;
    }

    /**
    *   Check to see if the value is numeric.
    *   @package shared_functions

    *   @param string $Deger
    *   @return bool
    */
    
    function SadeceRakam($Deger)
    {
        if(!eregi("[^0-9]",$Deger)) return true; else  return false;
    }
    
    /**
    *   extracts file extension from file
    *   @package shared_functions
    *   @param string $Dosya
    *   @return string
    */
    
    function DosyaUzantiCikar($DosyaAd)
    {
        $Donen = substr($DosyaAd,0,strpos($DosyaAd,'.'));
        return $Donen;
    }

    /**
    *   Calculates time between two dates. dates must be given as in Simdi() function
    *   @package shared_functions
    *   @see Simdi()
    *   @link http://php.net/date
    *   @param string $Tarih1
    *   @param string $Tarih2
    *   @param string $Donus    Can be one of Saniye(sec)(Default), Dakika(min), Saat(hr), Gun(day), Yil(Year).
    *   @return integer 
    */
    
    function IkiTarihArasiFark($Tarih1,$Tarih2,$Donus='Saniye')
    {
        $TarihDizi1 = tarihgetir($Tarih1,'dizi');
        $MkTarih1 = mktime($TarihDizi1[3],$TarihDizi1[4],$TarihDizi1[5],$TarihDizi1[1],$TarihDizi1[2],$TarihDizi1[0]);   
        
        $TarihDizi2 = tarihgetir($Tarih2,'dizi');
        $MkTarih2 = mktime($TarihDizi2[3],$TarihDizi2[4],$TarihDizi2[5],$TarihDizi2[1],$TarihDizi2[2],$TarihDizi2[0]);  
        
        $Fark = $MkTarih2-$MkTarih1;
        $Dakika = $Fark/60;
        $Saat   = round($Dakika/60,2);
        $Gun    = round($Saat/24);
        $Yil    = round($Gun/365);
        
        switch($Donus) {
            case 'Saniye':
                return $Fark;
                break; 
            case 'Dakika':
                return $Dakika;
                break;
            case 'Saat':
                return $Saat;
                break;
            case 'Gun':
                return $Gun;
                break;
            case 'Yil':
                return $Yil;
                break; 
        }
    }

    /**
    *   Checks an post string an evaluate if it is a valied e-mail
    *   @package shared_functions
    *   @param string $email
    *   @return bool
    */
    
    function CheckEmail($email = "")
    {
        if (ereg("[[:alnum:]]+@[[:alnum:]]+\.[[:alnum:]]+", $email)) {
        return true;
        } else {
            return false;
        }
    }

    
    /**
    *   Jabber Mesaj Fonksiyonu, sistemde tanimli bir jabber kullanicisi araci
    *   ligi ile diger jabber kullanicilarina otomatik mesaj gonderir.
    *   @package shared_functions
    *   @param string $toWhom
    *   @param string $Message
    *   @return string
    *   @link   jabber.class.php    http://jabber.class.php (link???)
    */
    
    function JabberMesaj($toWhom,$Message)
    {
    $Error  = "";  // Bos bir hata degiskeni acalim
    $Jabber = new Jabber();
    if($Jabber->Connect())
      $Error    = "Jabber Sunucusuna Baglanamadim!";
    if($Jabber->SendAuth())
      $Error    = "Kimlik Dogrulamasi Basarisiz Oldu!"; // Kimlik Dogrulama
    $Jabber->SendPresence(NULL, NULL, "online");
    $Jabber->SendMessage("$toWhom",
                     "normal",
                     NULL,
                     array(
                           "body" => "$Message"
                          ),
                     $payload
                    );
    $Jabber->Disconnect();
    return $Error;
  }

    /**
    *   Lists all the hardware categories...
    *   @package shared_functions
    *   @return array
    */
  
  function KategoriListele()
  {
    $KayitliKategoriler = array();
    $sorgu1 = sorgula("SELECT No,KatAd FROM UrunKategoriler ORDER BY KatAd");
    $i = 0;
    while(list($vt_No,$vt_KatAd) = getir($sorgu1))
    {
        $KayitliKategoriler[$i]['No'] = $vt_No;
        $KayitliKategoriler[$i]['KatAd'] = $vt_KatAd;
        $i++;
    }
    return $KayitliKategoriler;
  }
  
  function KategoriSelect($SifirOlsun='')
{
  $Kategoriler = array();
  if ($SifirOlsun=='Sifir') $Kategoriler[0] = 'Tüm Kategoriler';
  $Sql = "SELECT No,KatAd FROM UrunKategoriler ORDER BY KatAd";
  $Sonuc = sorgula($Sql);
  while(list($vt_No,$vt_KatAd)=getir($Sonuc))
  {
   $SqlAd = "SELECT Isim FROM UrunKategorilerMenu WHERE AnaNo='0' AND KategoriNo='$vt_No'";
   list($Isim) = getir(sorgula($SqlAd));
   if(!$Isim) $Isim = $vt_KatAd;
   $Kategoriler[$vt_No] = $Isim;
  }
  return $Kategoriler;
}

  function MarkaSelect($KategoriNo=0)
{
 $Markalar = array();
 if ($KategoriNo)
  $Sql = "SELECT DISTINCT(Marka) FROM Urunler WHERE KatNo='$KategoriNo' ORDER BY Marka";
 else
  $Sql = "SELECT DISTINCT(Marka) FROM Urunler ORDER BY Marka";
 $Sonuc = sorgula($Sql);
 $j = 0;
 while(list($Marka)=getir($Sonuc))
  if ($Marka)
    $Markalar[$Marka] = $Marka;
 return $Markalar;
}
//}}}
//{{{ BirimSelect()
function BirimSelect()
{
 $Birimler = array();
 $Sql = "SELECT DISTINCT(Birim) FROM Urunler ORDER BY Birim";
 $Sonuc = sorgula($Sql);
 $j = 0;
 while(list($Birim)=getir($Sonuc))
  if ($Birim)
    $Birimler[$Birim] = $Birim;
 return $Birimler;
}

function KategoriAd($KategoriNo)
{
  $Sql = "SELECT KatAd FROM UrunKategoriler WHERE No='$KategoriNo'";
  $Sonuc = sorgula($Sql);
  list($vt_KatAd) = getir($Sonuc);
  $Isim = $vt_KatAd;
  if ($Sonuc->numRows()>0)
    return $Isim;
  else
    return '';
}

function KategoriMenuAd($KategoriNo)
{
  $Sql = "SELECT KatAd FROM UrunKategoriler WHERE No='$KategoriNo'";
  $Sonuc = sorgula($Sql);
  list($vt_KatAd) = getir($Sonuc);
  $SqlAd = "SELECT Isim FROM UrunKategorilerMenu WHERE AnaNo='0' AND KategoriNo='$KategoriNo'";
  list($Isim) = getir(sorgula($SqlAd));
  if (!$Isim) $Isim = $vt_KatAd;
  if ($Sonuc->numRows()>0)
    return $Isim;
  else
    return '';
}

function OrtakAlanlarBul($UrunKategoriNo,$UrunNo=0)
{
  $Sql = "SELECT TabloAd,AlanSirasi,GorunenIsim,SonEk,GirisNot,FiltreAlanlar,ListeAlanlar FROM UrunKategoriler WHERE No='$UrunKategoriNo'";
  $Sonuc = sorgula($Sql);
  list($vt_TabloAd,$vt_AlanSirasi,$vt_GorunenIsim,$vt_SonEk,$vt_GirisNot,$vt_FiltreAlanlar,$vt_ListeAlanlar)=getir($Sonuc);
  $GorunenIsimler = explode('##',$vt_GorunenIsim);
  $SonEkler       = explode('##',$vt_SonEk);
  $GirisNotlar    = explode('##',$vt_GirisNot);
  $FiltreAlanlar  = explode('##',$vt_FiltreAlanlar);
  $ListeAlanlar   = explode('##',$vt_ListeAlanlar);

  $UrunKategoriAd = KategoriAd($UrunKategoriNo);


  $EkOzellikler = array();

  $KategoriAd = KategoriAd($UrunKategoriNo);
  $TabloAd = 'Urunler_'.$KategoriAd;
  $Sql = "SELECT * FROM $TabloAd LIMIT 1";
  $Sonuc = sorgula($Sql);
  $EkOzellikSayisi = $Sonuc->numCols(); //UrunNo alanýný çýkaralým
  $Alanlar = $Sonuc->TableInfo();
  for($i=1;$i<$EkOzellikSayisi;$i++)
  {
     $EkOzellikler[$i]['GorunenIsim'] = $GorunenIsimler[$i-1];
     $EkOzellikler[$i]['SonEk']       = $SonEkler[$i-1];
     $EkOzellikler[$i]['GirisNot']    = $GirisNotlar[$i-1];
     $EkOzellikler[$i]['MevcutDegerler'] = array();
     $AlanAdi = $Alanlar[$i]['name'];
     $EkOzellikler[$i]['AlanAd']    = $AlanAdi;
     if (in_array($AlanAdi,$FiltreAlanlar)) $EkOzellikler[$i]['FiltreAlan'] = true; else $EkOzellikler[$i]['FiltreAlan'] = false;
     if (in_array($AlanAdi,$ListeAlanlar))  $EkOzellikler[$i]['ListeAlan'] = true;  else $EkOzellikler[$i]['ListeAlan'] = false;


     if (ereg('flt_',$AlanAdi))
       $EkOzellikler[$i]['Tip'] = 'Secmeli';
     else
       $EkOzellikler[$i]['Tip'] = 'Text';
     if ($UrunNo)
     {
       $SqlDeger = "SELECT $AlanAdi FROM $TabloAd WHERE UrunNo='$UrunNo'";
       $SonucDeger = sorgula($SqlDeger);
       list($vt_Deger) = getir($SonucDeger);
       $EkOzellikler[$i]['Deger'] = $vt_Deger;
     }
     if ($UrunKategoriAd=='aksesuarlar'&&$AlanAdi=='kategoriad') //aksesuarlar için ayrý biþey yapmaya mecbur kaldýk
     {
        $SqlKategoriler = "SELECT No,KatAd FROM UrunKategorilerORDER BY KatAd";
        $SonucKategoriler = sorgula($SqlKategoriler);
        while(list($vt_No,$vt_KatAd) = getir($SonucKategoriler))
         if ($vt_KatAd<>'aksesuarlar')
           $EkOzellikler[$i]['MevcutDegerler'][$vt_KatAd] = $vt_KatAd;
     }
     else
     {
       $SqlDegerler = "SELECT DISTINCT($AlanAdi) FROM $TabloAd WHERE $AlanAdi<>''";
       $SonucDegerler = sorgula($SqlDegerler);
       if($AlanAdi=='altkategori') {
     $SqlNoBul = "SELECT No FROM UrunKategoriler WHERE TabloAd='$TabloAd'";
     $SonucSqlNoBul = sorgula($SqlNoBul);
     list($KategoriNumara) = getir($SonucSqlNoBul);
     $Sql1 = "SELECT Isim FROM UrunKategorilerMenu WHERE KategoriNo='$KategoriNumara' AND AnaNo<>'0'";
     $SonucBul = sorgula($Sql1);
     while(list($Isim) = getir($SonucBul))
          $EkOzellikler[$i]['MevcutDegerler'][$Isim] = $Isim;
       } else {
      while(list($vt_MevcutDeger) = getir($SonucDegerler))
          $EkOzellikler[$i]['MevcutDegerler'][$vt_MevcutDeger] = $vt_MevcutDeger;
     }
     }
  }
  return $EkOzellikler;
}
//}}}
//{{{YeniUrunGetir($Sayi='Tumu',$KategoriNo=0)
function YeniUrunGetir($Sayi='Tumu',$KategoriNo=0)
{
 global $sistem_UrunYeniKalmaSure;
 $Simdi = Simdi();
 $SimdiYil    = substr($Simdi,0,4);
 $SimdiAy     = substr($Simdi,4,2);
 $SimdiGun    = substr($Simdi,6,2);
 $SimdiSaat   = substr($Simdi,8,2);
 $SimdiDakika = substr($Simdi,10,2);
 $SimdiSaniye = substr($Simdi,12,2);
 $KriterSure = 60*60*24*$sistem_UrunYeniKalmaSure;
 $KriterZaman = date("YmdHis",mktime($SimdiSaat,$SimdiDakika,$SimdiSaniye,$SimdiAy,$SimdiGun,$SimdiYil)-$KriterSure);
 if ($KategoriNo)
  $Sql = "SELECT No,GirisTarih FROM Urunler WHERE AktifPasif='Aktif' AND KatNo='$KategoriNo' ORDER BY GirisTarih DESC";
 else
  $Sql = "SELECT No,GirisTarih FROM Urunler WHERE AktifPasif='Aktif' ORDER BY GirisTarih DESC";
 $i = 0;
 $Sonuc = sorgula($Sql);
 while(list($No,$GirisTarih)=getir($Sonuc))
 {
   if($GirisTarih<$KriterZaman) continue;
   if(!UrunGecerli($No)) continue;
   $Urunler[$i]['Bilgi'] = UrunBilgi($No);
   $i++;
   if($Sayi<>'Tumu' && $Sayi<=$i) break;
 }
 if (($Sayi<>'Tumu') && $Urunler)
    $Urunler = array_splice($Urunler,0,$Sayi);
 return $Urunler;
}














