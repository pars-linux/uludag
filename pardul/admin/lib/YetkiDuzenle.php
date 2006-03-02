<?
if ($get_SayfaNo)     $SayfaNo = $get_SayfaNo; else $SayfaNo = $post_SayfaNo;
if ($get_KullaniciAd) $KullaniciAd = $get_KullaniciAd; else $KullaniciAd = $post_KullaniciAd;
$Sql = "SELECT Isim FROM YonetimMenu WHERE No='$SayfaNo'";
$Sonuc = sorgula($Sql);
list($SayfaIsim) = getir($Sonuc);
//{{{ if ($post_Guncelle)
if ($post_Guncelle)
{
  $Sql = "SELECT No,Isim,IslemKod FROM YonetimMenu WHERE AnaNo='$SayfaNo' AND IslemKod<>''";
  $Sonuc = sorgula($Sql);
  $i = 0;
  while(list($vt_No)=getir($Sonuc))
  {
   $YetkiAd = 'Yetki'.$vt_No;
   $YetkiDeger = $$YetkiAd;
   if($YetkiDeger=='on') 
     $Eklenecek[] = $vt_No;
   else
     $Cikarilacak[] = $vt_No;
   $i++;
  }
  YetkiDuzenle($KullaniciAd,$Eklenecek,$Cikarilacak); 
}
//}}}
//{{{ Yetkiler listeleniyor
if ($SayfaNo)
{
 $Sql = "SELECT No,Isim,IslemKod,Aciklama FROM YonetimMenu WHERE AnaNo='$SayfaNo' AND IslemKod<>''";
 $Sonuc = sorgula($Sql);
 $i = 0;  
 while(list($vt_No,$vt_Isim,$vt_IslemKod,$vt_Aciklama)=getir($Sonuc))
 {
  $Yetkiler[$i]['No'] = $vt_No;
  $Yetkiler[$i]['Isim'] = $vt_Isim;
  $Yetkiler[$i]['Aciklama'] = $vt_Aciklama;
  $Yetkiler[$i]['YetkiVar']= YetkiVarmi($KullaniciAd,$vt_No); 
  $i++;
 }
 $smarty->assign('Yetkiler',$Yetkiler);
}
//}}}
$smarty->assign('SayfaNo',$SayfaNo);
$smarty->assign('SayfaIsim',$SayfaIsim);
$smarty->assign('KullaniciAd',$KullaniciAd);
?>
