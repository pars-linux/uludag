<?
if($get_SayfaNo) $SayfaNo = $get_SayfaNo; else $SayfaNo = $post_SayfaNo;
$Sql = "SELECT Isim FROM YonetimMenu WHERE No='$SayfaNo'";
$Sonuc = sorgula($Sql);
list($vt_Isim) = getir($Sonuc);
$smarty->assign('SayfaIsim',$vt_Isim);


if ($post_IslemKodEkle)
{
  $IslemKod = $post_IslemKod;
  $Aciklama = $post_Aciklama;
  $SqlKontrol = "SELECT * FROM YonetimMenu WHERE IslemKod='$IslemKod'";
  $SonucKontrol = sorgula($SqlKontrol);
  if (!$SonucKontrol->numRows()>0)
  {
    $Sql = "INSERT INTO YonetimMenu SET AnaNo='$SayfaNo',IslemKod='$IslemKod',Isim='$IslemKod',Aciklama='$Aciklama',YeniPencere='Hayir'";
    sorgula($Sql); 
  }
  else
   $smarty->assign('Uyari','Ayný iþlem koduna sahip bir alt yetki mevcut !');

}

$Sql = "SELECT No,Isim,IslemKod,Aciklama FROM YonetimMenu WHERE AnaNo='$SayfaNo' AND IslemKod<>''";
$Sonuc = sorgula($Sql);
$i = 0;
while(list($vt_No,$vt_Isim,$vt_IslemKod,$vt_Aciklama)=getir($Sonuc))
{
 $AltYetkiler[$i]['No']       = $vt_No;
 $AltYetkiler[$i]['IslemKod'] = $vt_IslemKod;
 $AltYetkiler[$i]['Isim']     = $vt_Isim;
 $AltYetkiler[$i]['Aciklama'] = $vt_Aciklama;
 $i++;
}
$smarty->assign('AltYetkiler',$AltYetkiler);
$smarty->assign('SayfaNo',$SayfaNo);




if ($post_YeniPencereEkle)
{
  $Isim = $post_YeniPencereIsim;
  $Adres = $post_YeniPencereAdres;
  $Aciklama = $post_YeniPencereAciklama;
  $SqlKontrol = "SELECT * FROM YonetimMenu WHERE Adres='$Adres'";
  $SonucKontrol = sorgula($SqlKontrol);
  if (!$SonucKontrol->numRows()>0)
  {
    $Sql = "INSERT INTO YonetimMenu SET AnaNo='$SayfaNo',Adres='$Adres',IslemKod='',Isim='$Isim',Aciklama='$Aciklama',YeniPencere='Evet'";
    sorgula($Sql);
  }
  else
   $smarty->assign('Uyari','Ayný iþlem koduna sahip bir yeni pencere mevcut !');
}





$Sql = "SELECT No,Isim,Adres,Aciklama FROM YonetimMenu WHERE AnaNo='$SayfaNo' AND YeniPencere='Evet'";
$Sonuc = sorgula($Sql);
$i = 0;
while(list($vt_No,$vt_Isim,$vt_Adres,$vt_Aciklama)=getir($Sonuc))
{
   
 $YeniPencereler[$i]['No']       = $vt_No;
 $YeniPencereler[$i]['Isim']     = $vt_Isim;
 $YeniPencereler[$i]['Aciklama'] = $vt_Aciklama;
 $YeniPencereler[$i]['Adres']    = $vt_Adres;
 $i++;
}
$smarty->assign('YeniPencereler',$YeniPencereler);



?>
