<?
// {{{ Uyari siliniyor
if($get_SilUyariNo)
{
    sorgula("UPDATE Uyarilar SET Durum='Pasif' WHERE No='$get_SilUyariNo'");
}
// }}}
// {{{ Uyarilar
$Sonuc = sorgula("SELECT No,Mesaj,TarihSaat,GerceklesmeSayi FROM Uyarilar WHERE Durum='Aktif' ORDER BY TarihSaat DESC");
$i = 0;
while(list($vt_No,$vt_Mesaj,$vt_TarihSaat,$vt_GerceklesmeSayi) = getir($Sonuc))
{
  $Uyarilar[$i]['No'] = $vt_No;
  $Uyarilar[$i]['Mesaj'] = $vt_Mesaj;
  $Uyarilar[$i]['TarihSaat'] = TarihGetir($vt_TarihSaat,"tam");
  $Uyarilar[$i]['GerceklesmeSayi'] = $vt_GerceklesmeSayi;
  $i++; 
}
$smarty->assign('Uyarilar',$Uyarilar);
// }}}
//{{{ Ziyaretçi bilgileri alýnýyor
$Sayilar    = ZiyaretciSayi();
$UyeSayi    = $Sayilar['Uye'];
$AnonimSayi = $Sayilar['Anonim'];
$smarty->assign('UyeGirisSayi',$UyeSayi);
$smarty->assign('AnonimGirisSayi',$AnonimSayi);
$smarty->assign('ToplamZiyaretci',$AnonimSayi + $UyeSayi);
//}}}
//{{{ Onaylanmayan yorum sayýsý
/*
$UrunYorumlar = UrunYorumlar();
$YorumSayi    = count($UrunYorumlar);
$smarty->assign('UyeYorumSayi',$YorumSayi);
*/
//}}}


//{{{ Üye görüþ ve önerileri
	$Sql = "SELECT * FROM GorusOneri WHERE AktifPasif='Aktif'";
	$Sonuc = sorgula($Sql);
	$GorusSayi = $Sonuc->numRows();
	$smarty->assign('GorusSayi',$GorusSayi);
//}}}
?>
