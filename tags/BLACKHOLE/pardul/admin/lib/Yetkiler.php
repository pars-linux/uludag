<?
if ($get_KullaniciAd) $KullaniciAd = $get_KullaniciAd; else $KullaniciAd = $post_KullaniciAd;
$smarty->assign('KullaniciAd',$KullaniciAd);

//{{{if($post_Guncelle)
if($post_BilgiGuncelle&&YetkiKontrol('YoneticiBilgiDuzenleme'))
{
  $SifreDegisti = false;
  $AdSoyad = addslashes($post_AdSoyad);
  $SqlKontrol = "SELECT * FROM Yoneticiler WHERE KullaniciAd='$KullaniciAd' AND Sifre='$post_Sifre'";
  $SonucKontrol = sorgula($SqlKontrol);
  if($post_TamYetki=='on') $TamYetki = 'Evet'; else $TamYetki = 'Hayir'; 
  if ($SonucKontrol->numRows()>0)
  {
    $SifreDegisti = true;
  }
  if (!$SifreDegisti)
  {
    $YeniSifre = md5($post_Sifre);
    $Sql = "UPDATE Yoneticiler SET Adsoyad='$AdSoyad',Sifre='$YeniSifre',TamYetki='$TamYetki' WHERE KullaniciAd='$KullaniciAd'";
  }
  else
    $Sql = "UPDATE Yoneticiler SET Adsoyad='$AdSoyad',TamYetki='$TamYetki' WHERE KullaniciAd='$KullaniciAd'";
  sorgula($Sql);
}
//}}}
//{{{ if($KullaniciAd)
if ($KullaniciAd)
{
 $Sql = "SELECT KullaniciAd,Sifre,AdSoyad,Durum,TamYetki FROM Yoneticiler WHERE KullaniciAd='$KullaniciAd'";
 $Sonuc = sorgula($Sql);
 list($KullaniciAd,$Sifre,$AdSoyad,$Durum,$TamYetki) = getir($Sonuc);
 $smarty->assign('AdSoyad',$AdSoyad);
 $smarty->assign('Sifre',$Sifre);
 $smarty->assign('KullaniciAd',$KullaniciAd);
 if ($TamYetki=='Evet') 
  $smarty->assign('TamYetki',true);
 else
  $smarty->assign('TamYetki',false);
}
//}}}

//{{{Yetkiler güncelleniyor
if ($post_Guncelle&&YetkiKontrol('YoneticiYetkiDuzenleme'))
{
  $Eklenecek   = array();
  $Cikarilacak = array();
  $Sql = "SELECT No,AnaNo FROM YonetimMenu WHERE AnaNo<>0 AND IslemKod=''";
  $Sonuc = sorgula($Sql);
  $i = 0;
  while(list($vt_No,$vt_AnaNo)=getir($Sonuc))
  {
    $YetkiAd = 'Yetki'.$vt_No;
    $YetkiDeger = $$YetkiAd;
    if ($YetkiDeger=='on') $Eklenecek[] = $vt_No; else $Cikarilacak[] = $vt_No;
    $i++;
  }
  YetkiDuzenle($KullaniciAd,$Eklenecek,$Cikarilacak);
}
//}}}


//{{{ function AltYetkiSayi($AnaNo)
 function AltYetkiSayi($AnaNo)
 {
   $Sql = "SELECT count(*) FROM YonetimMenu WHERE AnaNo='$AnaNo' AND IslemKod<>''";
   $Sonuc = sorgula($Sql);
   list($YetkiSayi) = getir($Sonuc);
   return $YetkiSayi;
 }
 //}}}
//{{{ function YeniPencereGetir($AnaNo)
 function YeniPencereGetir($AnaNo)
 {
   global $KullaniciAd;
   $Sql = "SELECT No,Isim,Aciklama FROM YonetimMenu WHERE AnaNo='$AnaNo' AND YeniPencere='Evet'";  
   $Sonuc = sorgula($Sql);
   $i = 0;
   while(list($vt_No,$vt_Isim,$vt_Aciklama)=getir($Sonuc))
   {
     $YeniPencere[$i]['No'] = $vt_No;
     $YeniPencere[$i]['Isim'] = $vt_Isim;
     $YeniPencere[$i]['Aciklama'] = $vt_Aciklama;
     $YeniPencere[$i]['YetkiVar'] = YetkiVarmi($KullaniciAd,$vt_No); 
     $YeniPencere[$i]['YetkiSayi'] = AltYetkiSayi($vt_No); 
 
     $i++;
   }
   return $YeniPencere; 
 } 
 //}}}
//{{{ function AltSayfaGetir($AnaNo)
 function AltSayfaGetir($AnaNo)
 {
   global $KullaniciAd;
   $Sql = "SELECT No,Isim,Aciklama FROM YonetimMenu WHERE AnaNo='$AnaNo' AND IslemKod='' AND YeniPencere='Hayir'";
   $Sonuc = sorgula($Sql);
   $i = 0;
   while(list($vt_No,$vt_Isim,$vt_Aciklama)=getir($Sonuc))
   {
    $AltSayfalar[$i]['No'] = $vt_No;
    $AltSayfalar[$i]['Isim'] = $vt_Isim;
    $AltSayfalar[$i]['Aciklama'] = $vt_Aciklama;
    $AltSayfalar[$i]['YeniPencereler'] = YeniPencereGetir($vt_No);
    $AltSayfalar[$i]['YetkiVar'] = YetkiVarmi($KullaniciAd,$vt_No);
    $AltSayfalar[$i]['YetkiSayi'] = AltYetkiSayi($vt_No);
    $i++;
   }
   return $AltSayfalar;  
 }
//}}}
//{{{Bilgiler listeleniyor
 $Sql = "SELECT Yetkiler FROM Yoneticiler WHERE KullaniciAd='$KullaniciAd'";  
 $Sonuc = sorgula($Sql);
 list($vt_Yetkiler) = getir($Sonuc);
 $Yetkiler = explode('#',$vt_Yetkiler);

 $Sql = "SELECT No,Isim,Aciklama FROM YonetimMenu WHERE AnaNo='0'";
 $Sonuc = sorgula($Sql);
 $i = 0;
 while(list($vt_No,$vt_Isim,$vt_Aciklama)=getir($Sonuc))
 {
   $AnaSayfalar[$i]['No']   = $vt_No;
   $AnaSayfalar[$i]['Isim'] = $vt_Isim;
   $AnaSayfalar[$i]['AltSayfalar'] = AltSayfaGetir($vt_No);
   $AnaSayfalar[$i]['YetkiVar'] = YetkiVarmi($KullaniciAd,$vt_No);
   $AnaSayfalar[$i]['Aciklama'] = $vt_Aciklama;
   $i++;
 }
 $smarty->assign('AnaSayfalar',$AnaSayfalar);
//}}}
?>
