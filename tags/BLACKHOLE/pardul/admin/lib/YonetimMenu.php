<?
if ($post_Ekle)
{
  $MenuIsim = $post_MenuIsim;
  $KaynakIsim = $post_KaynakIsim;
  $SqlKontrol = "SELECT * FROM YonetimMenu WHERE Adres='$KaynakIsim'";
  $SonucKontrol = sorgula($SqlKontrol);
  if (!$SonucKontrol->numRows()>0)
  {
    $Sql = "INSERT INTO YonetimMenu SET AnaNo='$post_AnaSayfa',Isim='$MenuIsim',Adres='$KaynakIsim'";
    sorgula($Sql);
  }
  else
   $smarty->assign('Uyari','Eklemek istediðini kaynak ismine sahip bir dosya zaten var');
}

if ($post_AnaSayfa)
{
  $SayfaNo = $post_AnaSayfa;
  $Sql = "SELECT Isim FROM YonetimMenu WHERE No='$SayfaNo'";
  $Sonuc = sorgula($Sql);
  list($vt_SayfaIsim) = getir($Sonuc);
  $smarty->assign('SayfaIsim',$vt_SayfaIsim);

  $smarty->assign('SeciliAnaSayfa',$SayfaNo);
  $Sql = "SELECT No,Isim FROM YonetimMenu WHERE AnaNo='$SayfaNo' AND IslemKod='' AND YeniPencere='Hayir'";
  $Sonuc = sorgula($Sql);
  $i = 0;
  while(list($vt_No,$vt_Isim)=getir($Sonuc))
  {
   $AltSayfalar[$i]['No']   = $vt_No;
   $AltSayfalar[$i]['Isim'] = $vt_Isim;
   $i++;
  }
  $smarty->assign('AltSayfalar',$AltSayfalar);
}

$Sql = "SELECT No,Isim FROM YonetimMenu WHERE AnaNo=0";
$Sonuc = sorgula($Sql);
while(list($vt_No,$vt_Isim)=getir($Sonuc)) $AnaSayfalar[$vt_No] = $vt_Isim;
$smarty->assign('AnaSayfalar',$AnaSayfalar);
?>
