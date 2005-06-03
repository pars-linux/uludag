<?
//{{{ SSS Kategori silme
if ($get_KategoriSil&&YetkiKontrol('SssKategoriSilme'))
{
  $SilKategoriNo = $get_KategoriSil;
  $Sql = "DELETE FROM SssKategori WHERE No=$SilKategoriNo";
  sorgula($Sql);
  $Sql = "DELETE FROM SssSorular WHERE KatNo=$SilKategoriNo";
  sorgula($Sql);

}//if ($get_KategoriSil<>"")
//}}}
//{{{ Yeni soru-cevap ekleme
if ($post_YeniSoruEkle&&YetkiKontrol('SssYeniSoruEkleme'))
{
  $YeniSoruKategoriNo = $post_YeniSoruKategoriNo;
  $Soru = addslashes($post_YeniSoru);
  $Cevap = addslashes($post_YeniCevap);
  $Sql = "SELECT MAX(Sira) AS Sira FROM SssSorular WHERE KatNo=$YeniSoruKategoriNo";
  $Sonuc = sorgula($Sql);
  list($vt_Sira) = getir($Sonuc);
  $Sira = $vt_Sira+1;
  $Sql = "INSERT INTO SssSorular SET KatNo=$YeniSoruKategoriNo,Soru='$Soru',Cevap='$Cevap',";
  $Sql.= "Sira=$Sira";
  sorgula($Sql);
}// if ($post_YeniSoruEkle<>"")
//}}}
//{{{ SSS Kategorilerinin Aþaðý-Yukarý sýralanmasý
$No = $get_No;
if ($No&&YetkiKontrol('SssKategoriSiralama'))
{
  $Sql = "SELECT Sira FROM SssKategori WHERE No=$get_No";
  $Sonuc = sorgula($Sql);
  list($vt_Sira) = getir($Sonuc);
  $GelenSira = $vt_Sira;
  if ($get_Yukari==1)
  {
    $YeniSira = $GelenSira-1;
    $Sql = "SELECT No FROM SssKategori WHERE Sira=$YeniSira";
    $Sonuc = sorgula($Sql);
    list($vt_No) = getir($Sonuc);
    $YukaridakiNo = $vt_No;
    $Sql = "UPDATE SssKategori SET Sira=$YeniSira WHERE No=$No";
    sorgula($Sql);
    $Sql = "UPDATE SssKategori SET Sira=$GelenSira WHERE No=$YukaridakiNo";
    sorgula($Sql);
  }
  if ($get_Asagi==1)
  {
    $YeniSira = $GelenSira+1;
    $Sql = "SELECT * FROM SssKategori WHERE Sira=$YeniSira";
    $Sonuc = sorgula($Sql);
    list($vt_No) = getir($Sonuc);
    $AsagidakiNo = $vt_No;
    $Sql = "UPDATE SssKategori SET Sira=$YeniSira WHERE No=$No";
    sorgula($Sql);
    $Sql = "UPDATE SssKategori SET Sira=$GelenSira WHERE No=$AsagidakiNo";
    sorgula($Sql);
  }
}
//}}}
//{{{Yeni SSS Kategorisi Ekleme
 if ($post_KategoriEkle&&YetkiKontrol('SssKategoriEkleme'))
 {
   $KategoriAd = $post_KategoriAd;
   $Aciklama   = $post_Aciklama;
   if (!KayitKontrol("SssKategori","Ad",$KategoriAd))
   {
    $Sql = "SELECT MAX(Sira) AS Sira FROM SssKategori";
    $Sonuc = sorgula($Sql);
    list($vt_Sira) = getir($Sonuc);
    $Sira = $vt_Sira+1;
    $Sql = "INSERT INTO SssKategori SET Ad='$KategoriAd',Aciklama='$Aciklama',Sira=$Sira";
    sorgula($Sql);
   }
 }//if ($post_KategoriEkle<>"")
//}}}
//{{{SSS Kategorilerini bulalým
 $Sql = "SELECT MAX(Sira) AS Sira FROM SssKategori";
 $Sonuc = sorgula($Sql);
 list($vt_Sira) = getir($Sonuc);
 $MaxSira = $vt_Sira;

 $Sql = "SELECT No,Ad,Sira FROM SssKategori ORDER BY Sira";
 $Sonuc = sorgula($Sql);
 $i = 0; 
 while(list($vt_No,$vt_Ad,$vt_Sira) = getir($Sonuc))
 { 
   $SssKategoriler[$i]['No'] = $vt_No;
   $SssKategoriler[$i]['Ad'] = $vt_Ad;
   $SssKategoriler[$i]['Sira'] = $vt_Sira;
   if ($vt_Sira==1)
    $SssKategoriler[$i]['Yukari'] = false;
   else
    $SssKategoriler[$i]['Yukari'] = true;
   if ($vt_Sira==$MaxSira)
    $SssKategoriler[$i]['Asagi'] = false;
   else
    $SssKategoriler[$i]['Asagi'] = true;
   $i++;
 }

 $smarty->assign('SssKategoriler',$SssKategoriler);
 if(count($SssKategoriler)>0)
  $KategoriVar = true;
 else
  $KategoriVar = false;
 $smarty->assign('KategoriVar',$KategoriVar);
//}}}
//{{{Soru silinmesi
if ($get_Sil&&YetkiKontrol('SssSoruSilme'))
{
  $SilinecekSoruNo = $get_Sil;
  $SilinecekKategoriNo = $get_SoruGoster;
  $Sql = "DELETE FROM SssSorular WHERE KatNo=$SilinecekKategoriNo AND No=$SilinecekSoruNo";
  sorgula($Sql);
}
//}}}
//{{{Sorularýn aþaðý-yukarý sýralanmasý
$SoruNo = $get_SoruNo;
$SoruKategoriNo = $get_SoruGoster;
if ($SoruNo&&YetkiKontrol('SssSoruSiralama'))
{
  $Sql = "SELECT Sira FROM SssSorular WHERE KatNo=$SoruKategoriNo AND No=$SoruNo";
  $Sonuc = sorgula($Sql);
  list($vt_Sira) = getir($Sonuc);
  $GelenSira = $vt_Sira;
  if ($get_SoruYukari==1)
  {
   if ($GelenSira>1)
   {
    $Sql = "SELECT MAX(Sira) AS YeniSira FROM SssSorular WHERE Sira<$GelenSira";
    $Sonuc = sorgula($Sql);
    list($vt_YeniSira) = getir($Sonuc); 
    $YeniSira = $vt_YeniSira;
    $Sql = "SELECT No FROM SssSorular WHERE Sira=$YeniSira AND KatNo=$SoruKategoriNo";
    $Sonuc = sorgula($Sql);
    list($vt_No) = getir($Sonuc);
    $YukaridakiNo = $vt_No;
    $Sql = "UPDATE SssSorular SET Sira=$YeniSira WHERE No=$SoruNo AND KatNo=$SoruKategoriNo";
    sorgula($Sql);
    $Sql = "UPDATE SssSorular SET Sira=$GelenSira WHERE No=$YukaridakiNo AND KatNo=$SoruKategoriNo";
    sorgula($Sql);
   }
  }
  if ($get_SoruAsagi==1)
  {
    $Sql = "SELECT MIN(Sira) AS YeniSira FROM SssSorular WHERE Sira>$GelenSira";
    $Sonuc = sorgula($Sql);
    list($vt_YeniSira) = getir($Sonuc);
    $YeniSira = $vt_YeniSira;
    $Sql = "SELECT No FROM SssSorular WHERE Sira=$YeniSira AND KatNo=$SoruKategoriNo";
    $Sonuc = sorgula($Sql);
    list($vt_No) = getir($Sonuc);
    $AsagidakiNo = $vt_No;
    $Sql = "UPDATE SssSorular SET Sira=$YeniSira WHERE No=$SoruNo AND KatNo=$SoruKategoriNo";
    sorgula($Sql);
    $Sql = "UPDATE SssSorular SET Sira=$GelenSira WHERE No=$AsagidakiNo AND KatNo=$SoruKategoriNo";
    sorgula($Sql);
  }
}//if ($SoruNo<>"")
//}}}
//{{{SSS Kategorilerine ait sorularý bulalým
if ($get_SoruGoster<>"")
{
 $KategoriNo = $get_SoruGoster;
 $Sql = "SELECT Ad FROM SssKategori WHERE No=$KategoriNo";
 $Sonuc = sorgula($Sql);
 list($vt_Ad) = getir($Sonuc);
 $KategoriAd = $vt_Ad;

 $Sql = "SELECT MAX(Sira) AS Sira FROM SssSorular WHERE KatNo=$KategoriNo";
 $Sonuc = sorgula($Sql);
 list($vt_Sira) = getir($Sonuc); 
 $MaxSira = $vt_Sira;
 $Sql = "SELECT No,Soru,Sira FROM SssSorular WHERE KatNo=$KategoriNo ORDER BY Sira";
 $Sonuc = sorgula($Sql);

 $i = 0;
 while (list($vt_No,$vt_Soru,$vt_Sira)=getir($Sonuc))
 {
   $Sorular[$i]['No'] = $vt_No;
   $Sorular[$i]['Soru'] = $vt_Soru;
   $Sorular[$i]['Sira'] = $vt_Sira;
   if ($vt_Sira==1)
    $Sorular[$i]['Yukari'] = false;
   else
    $Sorular[$i]['Yukari'] = true;
   if ($vt_Sira==$MaxSira)
    $Sorular[$i]['Asagi'] = false;
   else
    $Sorular[$i]['Asagi'] = true;
   $i++;
 }
 $smarty->assign('Sorular',$Sorular);
 if (count($Sorular)>0) $SoruVar = true; else $SoruVar = false;
 $smarty->assign('SoruVar',$SoruVar);
 $smarty->assign('Listelendi',1);
 $smarty->assign('SssKategoriAd',$KategoriAd);
 $smarty->assign('SssKategoriNo',$KategoriNo);
 $smarty->assign('SoruGoster',$get_SoruGoster);
}// if ($get_SoruGoster<>"")
//}}}
?>
