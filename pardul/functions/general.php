<?
  /**
   *  functions.php
   *  This is a good place for end-user GUI specific functions.
   *   @package user_functions
   *   @author R. Tolga KORKUNCKAYA <tolga@forsnet.com.tr>
   *   @todo internal variable names should be renamed in order to u18a purposes.
   */

     
   /**
    *   Looks for if there is any FAQ in DB
    *   @param integer $KategoriNo
    *   @return bool
    */
    
    function SssSoruVarmi($KategoriNo)
    {
    $Sql = "SELECT No FROM SssSorular WHERE KatNo='$KategoriNo'";
    $Sonuc = sorgula($Sql);
    if ($Sonuc->numRows()>0)
        return true;
    else
        return false;
    } // end SssSoruVarmi

    /**
    *   Updates site search hits...
    *   @package shared_functions
    *   @param string $ArananSayfaTur
    *   @param string $Kelime
    *   @param integer $SonucSayi 
    */
    
    function AramaHit($ArananSayfaTur,$Kelime,$SonucSayi)
    {
	$Sql= "SELECT No,Kelime,ArananSayfaTur,AramaSayisi,SonBulunanKayitSayisi FROM searchterms WHERE Kelime='$Kelime' AND ArananSayfaTur='$ArananSayfaTur'";
	$Sonuc=sorgula($Sql);
	$numrows=$Sonuc->numRows();
	if($numrows>0){
	 list($vt_No,$vt_Kelime,$vt_ArananSayfaTur,$vt_AramaSayisi,$vt_SonBulunanKayitSayisi)= getir($Sonuc);	
	 $ASayi=0;
	 $ASayi=$vt_AramaSayisi+1;
	 $sql = "UPDATE ArananKelimeler SET AramaSayisi='$ASayi',SonBulunanKayitSayisi='$SonucSayi' WHERE No='$vt_No'";
  	 sorgula($sql);	
	} else {
		$Arama=1;
	   $sql = "INSERT INTO ArananKelimeler SET
           Kelime	  ='$Kelime',
           ArananSayfaTur ='$ArananSayfaTur',
	   AramaSayisi    ='$Arama',SonBulunanKayitSayisi='$SonucSayi'";
         sorgula($sql);
	}
    }

    /**
    *   Updates page hits
    *   @package shared_functions
    *   @param string $FullPage
    *   @return mixed 
    */
    
    function SayfaHitler($FullPage)
    {
	$Sql= "SELECT No,Sayfa,Hit,Ek FROM SayfalarHit WHERE Sayfa='$FullPage'";
	$Sonuc=sorgula($Sql);
	$numrows=$Sonuc->numRows();
	if($numrows>0){
	 list($vt_No,$vt_Sayfa,$vt_Hit,$vt_Ek)= getir($Sonuc);	
	 $ASayi=0;
	 $ASayi=$vt_Hit+1;
	 $sql = "UPDATE SayfalarHit SET Hit='$ASayi' WHERE No='$vt_No'";
	 sorgula($sql);	
	 } else {
	   $Hit=1;
	   $sql = "INSERT INTO SayfalarHit SET
            Hit	    ='$Hit',
            Sayfa   ='$FullPage',
	    Ek	    ='0'";
	   sorgula($sql);
	 }
    }
    
    /**
    *   Check if a specific page needs Login
    *   @package shared_functions
    *   @param string $Pagename
    *   @return string Yes or No
    */
    
    function UyelikKontrol($PageName)
    {
        $sayfasorgu = "SELECT No,UyelikDurum FROM KullaniciSayfalar WHERE SayfaIsim='$PageName'";
        $sonucsayfa=sorgula($sayfasorgu);
        list($vt_No,$vt_UyelikDurum)=getir($sonucsayfa);
        return $vt_UyelikDurum;
    }
?>
