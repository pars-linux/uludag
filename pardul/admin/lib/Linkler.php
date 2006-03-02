<?
//{{{ SSS Kategori silme
if ($get_KategoriSil)
{
  $SilKategoriNo = $get_KategoriSil;
  $Sql = "DELETE FROM LinkKategori WHERE No=$SilKategoriNo";
  sorgula($Sql);
  //$Sql = "DELETE FROM Linker WHERE KatNo=$SilKategoriNo";
 // sorgula($Sql);

}//if ($get_KategoriSil<>"")
//}}}
//{{{ Yeni Link ekleme
if ($post_YeniLinkEkle)
{
  $YeniLinkKategoriNo = $post_YeniLinkKategoriNo;
  $Link = addslashes($post_YeniLink);
  $Sql = "SELECT MAX(Sira) AS Sira FROM Linkler WHERE KatNo=$YeniLinkKategoriNo";
  $Sonuc = sorgula($Sql);
  list($vt_Sira) = getir($Sonuc);
  $Sira = $vt_Sira+1;
  $Sql = "INSERT INTO Linkler SET KatNo=$YeniLinkKategoriNo,Link='$Link',Aciklama='$post_YeniLinkAciklama',";
  $Sql.= "Sira=$Sira";
  sorgula($Sql);
}// if ($post_YeniSoruEkle<>"")
//}}}
//{{{ SSS Kategorilerinin Aþaðý-Yukarý sýralanmasý
$No = $get_No;
if ($No)
{
  $Sql = "SELECT Sira FROM LinkKategori WHERE No=$get_No";
  $Sonuc = sorgula($Sql);
  list($vt_Sira) = getir($Sonuc);
  $GelenSira = $vt_Sira;
  if ($get_Yukari==1)
  {
    $YeniSira = $GelenSira-1;
    $Sql = "SELECT No FROM LinkKategori WHERE Sira=$YeniSira";
    $Sonuc = sorgula($Sql);
    list($vt_No) = getir($Sonuc);
    $YukaridakiNo = $vt_No;
    $Sql = "UPDATE LinkKategori SET Sira=$YeniSira WHERE No=$No";
    sorgula($Sql);
    $Sql = "UPDATE LinkKategori SET Sira=$GelenSira WHERE No=$YukaridakiNo";
    sorgula($Sql);
  }
  if ($get_Asagi==1)
  {
    $YeniSira = $GelenSira+1;
    $Sql = "SELECT * FROM LinkKategori WHERE Sira=$YeniSira";
    $Sonuc = sorgula($Sql);
    list($vt_No) = getir($Sonuc);
    $AsagidakiNo = $vt_No;
    $Sql = "UPDATE LinkKategori SET Sira=$YeniSira WHERE No=$No";
    sorgula($Sql);
    $Sql = "UPDATE LinkKategori SET Sira=$GelenSira WHERE No=$AsagidakiNo";
    sorgula($Sql);
  }
}
//}}}
//{{{Yeni Link Kategorisi Ekleme
 if ($post_KategoriEkle)
 {
   $KategoriAd = $post_KategoriAd;
   $Aciklama   = $post_Aciklama;
   if (!KayitKontrol("LinkKategori","Ad",$KategoriAd))
   {
    $Sql = "SELECT MAX(Sira) AS Sira FROM LinkKategori";
    $Sonuc = sorgula($Sql);
    list($vt_Sira) = getir($Sonuc);
    $Sira = $vt_Sira+1;
    $Sql = "INSERT INTO LinkKategori SET Ad='$KategoriAd',Aciklama='$Aciklama',Sira=$Sira";
    sorgula($Sql);
   }
 }//if ($post_KategoriEkle<>"")
//}}}
//{{{SSS Kategorilerini bulalým
 $Sql = "SELECT MAX(Sira) AS Sira FROM LinkKategori";
 $Sonuc = sorgula($Sql);
 list($vt_Sira) = getir($Sonuc);
 $MaxSira = $vt_Sira;

 $Sql = "SELECT No,Ad,Sira FROM LinkKategori ORDER BY Sira";
 $Sonuc = sorgula($Sql);
 $i = 0; 
 while(list($vt_No,$vt_Ad,$vt_Sira) = getir($Sonuc))
 { 
   $LinkKategoriler[$i]['No'] = $vt_No;
   $LinkKategoriler[$i]['Ad'] = $vt_Ad;
   $LinkKategoriler[$i]['Sira'] = $vt_Sira;
   if ($vt_Sira==1)
    $LinkKategoriler[$i]['Yukari'] = false;
   else
    $LinkKategoriler[$i]['Yukari'] = true;
   if ($vt_Sira==$MaxSira)
    $LinkKategoriler[$i]['Asagi'] = false;
   else
    $LinkKategoriler[$i]['Asagi'] = true;
   $i++;
 }

 $smarty->assign('LinkKategoriler',$LinkKategoriler);
 if(count($LinkKategoriler)>0)
  $KategoriVar = true;
 else
  $KategoriVar = false;
 $smarty->assign('KategoriVar',$KategoriVar);
//}}}
//{{{Soru silinmesi
if ($get_Sil)
{
  $SilinecekLinkNo = $get_Sil;
  $SilinecekKategoriNo = $get_LinkGoster;
  $Sql = "DELETE FROM Linkler WHERE KatNo=$SilinecekKategoriNo AND No=$SilinecekLinkNo";
  sorgula($Sql);
}
//}}}
//{{{Sorularýn aþaðý-yukarý sýralanmasý
$LinkNo = $get_LinkNo;
$LinkKategoriNo = $get_LinkGoster;
if ($LinkNo)
{
  $Sql = "SELECT Sira FROM Linkler WHERE KatNo=$LinkKategoriNo AND No=$LinkNo";
  $Sonuc = sorgula($Sql);
  list($vt_Sira) = getir($Sonuc);
  $GelenSira = $vt_Sira;
  if ($get_LinkYukari==1)
  {
   if ($GelenSira>1)
   {
    $Sql = "SELECT MAX(Sira) AS YeniSira FROM Linkler WHERE Sira<$GelenSira";
    $Sonuc = sorgula($Sql);
    list($vt_YeniSira) = getir($Sonuc); 
    $YeniSira = $vt_YeniSira;
    $Sql = "SELECT No FROM Linkler WHERE Sira=$YeniSira AND KatNo=$LinkKategoriNo";
    $Sonuc = sorgula($Sql);
    list($vt_No) = getir($Sonuc);
    $YukaridakiNo = $vt_No;
    $Sql = "UPDATE Linkler SET Sira=$YeniSira WHERE No=$LinkNo AND KatNo=$LinkKategoriNo";
    sorgula($Sql);
    $Sql = "UPDATE Linkler SET Sira=$GelenSira WHERE No=$YukaridakiNo AND KatNo=$LinkKategoriNo";
    sorgula($Sql);
   }
  }
  if ($get_LinkAsagi==1)
  {
    $Sql = "SELECT MIN(Sira) AS YeniSira FROM Linkler WHERE Sira>$GelenSira";
    $Sonuc = sorgula($Sql);
    list($vt_YeniSira) = getir($Sonuc);
    $YeniSira = $vt_YeniSira;
    $Sql = "SELECT No FROM Linkler WHERE Sira=$YeniSira AND KatNo=$LinkKategoriNo";
    $Sonuc = sorgula($Sql);
    list($vt_No) = getir($Sonuc);
    $AsagidakiNo = $vt_No;
    $Sql = "UPDATE Linkler SET Sira=$YeniSira WHERE No=$LinkNo AND KatNo=$LinkKategoriNo";
    sorgula($Sql);
    $Sql = "UPDATE Linkler SET Sira=$GelenSira WHERE No=$AsagidakiNo AND KatNo=$LinkKategoriNo";
    sorgula($Sql);
  }
}//if ($SoruNo<>"")
//}}}
//{{{SSS Kategorilerine ait sorularý bulalým
if ($get_LinkGoster<>"")
{
 $KategoriNo = $get_LinkGoster;
 $Sql = "SELECT Ad FROM LinkKategori WHERE No=$KategoriNo";
 $Sonuc = sorgula($Sql);
 list($vt_Ad) = getir($Sonuc);
 $KategoriAd = $vt_Ad;

 $Sql = "SELECT MAX(Sira) AS Sira FROM Linkler WHERE KatNo=$KategoriNo";
 $Sonuc = sorgula($Sql);
 list($vt_Sira) = getir($Sonuc); 
 $MaxSira = $vt_Sira;
 $Sql = "SELECT No,Link,Sira,Aciklama FROM Linkler WHERE KatNo=$KategoriNo ORDER BY Sira";
 $Sonuc = sorgula($Sql);

 $i = 0;
 while (list($vt_No,$vt_Link,$vt_Sira,$vt_Aciklama)=getir($Sonuc))
 {
   $Linkler[$i]['No'] = $vt_No;
   $Linkler[$i]['Link'] = $vt_Link;
   $Linkler[$i]['Sira'] = $vt_Sira;
   $Linkler[$i]['Aciklama'] = $vt_Aciklama;
   if ($vt_Sira==1)
    $Linkler[$i]['Yukari'] = false;
   else
    $Linkler[$i]['Yukari'] = true;
   if ($vt_Sira==$MaxSira)
    $Linkler[$i]['Asagi'] = false;
   else
    $Linkler[$i]['Asagi'] = true;
   $i++;
 }
 $smarty->assign('Linkler',$Linkler);
 if (count($Linkler)>0) $LinkVar = true; else $LinkVar = false;
 $smarty->assign('LinkVar',$LinkVar);
 $smarty->assign('Listelendi',1);
 $smarty->assign('LinkKategoriAd',$KategoriAd);
 $smarty->assign('LinkKategoriNo',$KategoriNo);
 $smarty->assign('LinkGoster',$get_LinkGoster);
}// if ($get_SoruGoster<>"")
//}}}
?>
