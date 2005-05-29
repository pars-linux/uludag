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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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
    *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
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

?>
