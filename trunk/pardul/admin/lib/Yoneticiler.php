<?
//{{{Yeni y�netici ekleniyorsa
if ($post_KullaniciEkle&&YetkiKontrol('YoneticiEkleme'))
{
  $Sql = "SELECT KullaniciAd FROM Yoneticiler WHERE KullaniciAd='$post_YeniKullaniciAd'";
  $Sonuc = sorgula($Sql);
  if ($Sonuc->numRows()>0)
  {
    $smarty->assign('Uyari','Ayn� kullan�c� ad�na sahip bir y�netici mevcut');
  }
  else
  {
     $YeniSifre = md5($post_Sifre);
     $Sql = "INSERT INTO Yoneticiler SET AdSoyad='$post_YeniKullaniciAdSoyad',KullaniciAd='$post_YeniKullaniciAd',Sifre='$YeniSifre'";       
     Sorgula($Sql);
  }
}
//}}}
//{{{ bir y�netici aktif yada pasif yap�ld�ysa
if ($post_Degistir&&YetkiKontrol('YoneticiDurumDegistirme'))
{
  $Sql = "UPDATE Yoneticiler SET Durum='$post_YeniDurum' WHERE KullaniciAd='$post_KullaniciAd'";
  sorgula($Sql);
}
//}}}
//{{{mevcut y�neticiler al�n�yor
$Sql = "SELECT KullaniciAd,Sifre,AdSoyad,Durum FROM Yoneticiler ORDER BY AdSoyad";
$Sonuc = sorgula($Sql);
$i = 0;
while(list($KullaniciAd,$Sifre,$AdSoyad,$Durum) = getir($Sonuc))
{
 $Yoneticiler[$i]['KullaniciAd'] = $KullaniciAd;
 $Yoneticiler[$i]['Sifre']       = $Sifre;
 $Yoneticiler[$i]['AdSoyad']     = $AdSoyad;
 $Yoneticiler[$i]['Durum']       = $Durum;
 if ($Durum=='Aktif')
   $Yoneticiler[$i]['OlacakDurum'] = 'Pasif';
 else
   $Yoneticiler[$i]['OlacakDurum'] = 'Aktif';


 $i++;
}
$smarty->assign('Yoneticiler',$Yoneticiler);
//}}}
?>
