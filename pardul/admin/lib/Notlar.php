<?
//{{{ ipucu siliniyor
if ($get_Sil&&YetkiKontrol('IpucuSilme'))
{
 $Sql = "DELETE FROM notes WHERE No='$get_Sil'";
 sorgula($Sql);
}
//}}}
//{{{ Yeni ipucu ekleniyor
if($post_Ekle&&YetkiKontrol('IpucuEkleme'))
{
  if (!KayitKontrol('notes','Mesaj',$post_Ipucu))
  {
    $Sql = "INSERT INTO notes SET Mesaj='$post_Ipucu'";
    sorgula($Sql);
  }
  else 
  $Uyari = 'Eklemek istediðiniz ipucu mevcut!';
  $smarty->assign('Uyari',$Uyari);
}
//}}}
//{{{ güncelleme yapýlacaksa
if ($get_Duzenle)
{
  $Sql = "SELECT No,Mesaj FROM notes WHERE No='$get_Duzenle'";  
  $Sonuc = sorgula($Sql);
  list($DuzenleNo,$DuzenleMesaj)=getir($Sonuc);
  $smarty->assign('DuzenleNo',$DuzenleNo);
  $smarty->assign('DuzenleMesaj',$DuzenleMesaj);
  $Sonuc = sorgula($Sql);
}
//}}}
//{{{ güncelleme yapýlýyor
if ($post_Guncelle&&YetkiKontrol('IpucuGuncelleme'))
{
  $Sql = "UPDATE notes SET Mesaj='$post_Ipucu' WHERE No='$post_DuzenleNo'";
  sorgula($Sql);
}
//}}}
//{{{ kayitli ipuçlarýný alalým
$Sql = "SELECT No,Mesaj FROM notes";
$Sonuc = sorgula($Sql);
$i = 0;
while(list($No,$Mesaj)=getir($Sonuc))
{
 $notes[$i]['No'] = $No;  
 $notes[$i]['Mesaj'] = $Mesaj;  
 $i++;
}
$smarty->assign('notes',$notes);
//}}}

?>
