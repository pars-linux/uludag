<?
 if ($post_Guncelle&&YetkiKontrol('YonetimMenuGuncelleme'))
 {
   $Sql = "SELECT Isim FROM Degiskenler WHERE Kategori='YonetimMenu'";  
   $Sonuc = sorgula($Sql);
   $i = 0;
   while(list($Isim)=getir($Sonuc))
   {
     $DegiskenAd = 'post_'.$Isim;
     $DegiskenDeger = $$DegiskenAd;
     $SqlCumle = "UPDATE Degiskenler SET Deger='$DegiskenDeger' WHERE Isim='$Isim'";
     sorgula($SqlCumle);
   } 
  
 }

 $Degiskenler = array(); 
 $Sql = "SELECT Isim,Deger,Aciklama FROM Degiskenler WHERE Kategori='YonetimMenu'";  
 $Sonuc = sorgula($Sql);
 $i = 0;
 while(list($Isim,$Deger,$Aciklama)=getir($Sonuc))
 {
   $Degiskenler[$i]['Isim'] = $Isim;
   $Degiskenler[$i]['Deger'] = $Deger;
   $Degiskenler[$i]['Aciklama'] = $Aciklama;
   $i++;
 }
 $smarty->assign('Degiskenler',$Degiskenler);

?>
