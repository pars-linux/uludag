<?
//{{{ ipucu siliniyor
if ($get_Sil&&YetkiKontrol('IpucuSilme'))
{
 $Sql = "DELETE FROM Notlar WHERE No='$get_Sil'";
 sorgula($Sql);
}
//}}}
//{{{ Yeni ipucu ekleniyor
if($post_Ekle&&YetkiKontrol('IpucuEkleme'))
{
  if (!KayitKontrol('Notlar','Mesaj',$post_Ipucu))
  {
    $Sql = "INSERT INTO Notlar SET Mesaj='$post_Ipucu'";
    sorgula($Sql);
  }
  else 
  $Uyari = 'Eklemek istedi�iniz ipucu mevcut!';
  $smarty->assign('Uyari',$Uyari);
}
//}}}
//{{{ g�ncelleme yap�lacaksa
if ($get_Duzenle)
{
  $Sql = "SELECT No,Mesaj FROM Notlar WHERE No='$get_Duzenle'";  
  $Sonuc = sorgula($Sql);
  list($DuzenleNo,$DuzenleMesaj)=getir($Sonuc);
  $smarty->assign('DuzenleNo',$DuzenleNo);
  $smarty->assign('DuzenleMesaj',$DuzenleMesaj);
  $Sonuc = sorgula($Sql);
}
//}}}
//{{{ g�ncelleme yap�l�yor
if ($post_Guncelle&&YetkiKontrol('IpucuGuncelleme'))
{
  $Sql = "UPDATE Notlar SET Mesaj='$post_Ipucu' WHERE No='$post_DuzenleNo'";
  sorgula($Sql);
}
//}}}
//{{{ kayitli ipu�lar�n� alal�m
$Sql = "SELECT No,Mesaj FROM Notlar";
$Sonuc = sorgula($Sql);
$i = 0;
while(list($No,$Mesaj)=getir($Sonuc))
{
 $Notlar[$i]['No'] = $No;  
 $Notlar[$i]['Mesaj'] = $Mesaj;  
 $i++;
}
$smarty->assign('Notlar',$Notlar);
//}}}

?>
