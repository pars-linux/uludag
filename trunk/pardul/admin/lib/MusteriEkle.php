<?php
require_once("$INI_OrtakDosyalarDizin/Fonksiyonlar/ileti.php");
$EPostaKimden = $sistem_VarsayilanGonderen;
$EPostaTur    = $sistem_VarsayilanGonderimSekli;

$Vilayetler = VilayetlerSelect();
$Ulkeler = UlkelerSelect();
$Simdi = Simdi();
if ($post_HaberListe == "Evet") ($HaberListe="Evet"); else  $HaberListe = "Hayir";

//{{{ HaberListesineEkle($EPosta)
function HaberListesineEkle($EPosta)
{
  $Simdi = Simdi();
  if (!EPostaGecerli($EPosta)) return 'Gecersiz';
  $Sql = "SELECT EPosta FROM HaberListe WHERE EPosta='$EPosta'";
  $Sonuc = sorgula($Sql);
  if ($Sonuc->numRows()>0)
   return 'Mevcut';
  else
  {
    sorgula("INSERT INTO HaberListe SET EPosta='$EPosta',TarihSaat='$Simdi'");
    return 'Eklendi';
  }
}
//}}}
if ($post_UyeKayit<>"")
{
  $IslemUyari = KayitKontrol("Kullanicilar","EPosta","$post_EPosta");
  $post_Sifre = md5($post_Sifre);

  if($IslemUyari == false)
   {
     $Mesaj = '�yeli�inizin aktifle�tirilmesi i�in l�tfen E-Posta adresinize g�nderilen do�rulama i�lemini ger�ekle�tiriniz.';
     //Aktivasyon mailini g�nderelim
     $AktivasyonKod = Rastgele(10,'TamKarisik');
     $AktivasyonAdres = $SSayfa."UyeAktivasyon&Kod=$AktivasyonKod";
     $Degiskenler['AdSoyad'] = $post_AdSoyad;
     $Degiskenler['Adres']   = $AktivasyonAdres;
     $EPosta=new Ileti();
     $EPostaTur='Html';
     $EPosta->IcerikHazir('�yelik Onay�',$Degiskenler,$EPostaTur);
     $EPosta->Baslik('�yelik Aktivasyonu');
     $EPosta->Gonderen($EPostaKimden);
     if($EPosta->Gonder($post_EPosta1))
     {
     	
  if ($post_TOFBelge)
    $post_TOFBelge='Var';
  else 
    $post_TOFBelge='Yok'; 
    
    if ($post_OzelVekalet)
    $post_OzelVekalet='Var';
  else 
    $post_OzelVekalet='Yok'; 
   
   if ($post_GelirTablosu)
    $post_GelirTablosu='Var';
  else 
    $post_GelirTablosu='Yok';
    
    if ($post_SicilGazete)
    $post_SicilGazete='Var';
  else 
    $post_SicilGazete='Yok';
      
   if ($post_MMNMVekalet)
    $post_MMNMVekalet='Var';
  else 
    $post_MMNMVekalet='Yok'; 
  
  
     	
       $Sql = "INSERT INTO Kullanicilar SET
       AdSoyad    ='$post_AdSoyad',
       EPosta     ='$post_EPosta1',
       Sifre      ='$post_Sifre',
       FirmaUnvan ='$post_FirmaUnvan',
       FirmaAd   ='$post_FirmaAd',TelNo='$post_Tel',
       FaxNo      ='$post_Fax',
       Adres     ='$post_Adres',
       HaberListe ='$HaberListe',
       Vilayet    ='$post_Vilayet',Ulke='$post_Ulke',
       UyelikTarih = '$Simdi',
       AktivasyonKod ='$AktivasyonKod',VergiDaire='$post_VergiDaire',VergiNo='$post_VergiNo',WebAdres='$post_URL',UrunCesit='$post_UrunCesit',MMNMDurum='$post_MMNMDurum',MMNMVekalet='$post_MMNMVekalet',TOFBelge='$post_TOFBelge',OzelVekalet='$post_OzelVekalet',GelirTablosu='$post_GelirTablosu',SicilGazete='$post_SicilGazete',EANTip='$post_EANTip',Ciro='$post_Ciro'";
       if($post_TescilNumarasi<>'Tescil Numaras�...'){
  		$Sql.=",TescilNo='$post_TescilNumarasi'";
  		}
  		 if($post_MMNMBasvuru){
  		$Sql.=",MMNMBasvuru='$post_MMNMBasvuru'";
  		}
  	   sorgula($Sql);
       $Uyari="Kay�t ��lemi Ba�ar� ile Tamamlanm��t�r!!! ";
       $smarty->assign('Uyari',$Uyari);
       //HaberListesine ekle
       if ($post_HaberListe == "Evet"){
       	$Durum = HaberListesineEkle($post_EPosta1);
       	$smarty->assign('Durum',$Durum);
     	}
     }
     else
     {
      $Mesaj ='�yelik i�lemleriniz E-Posta sistemindeki problemden dolay� ger�ekle�tirilemedi! En k�sa zamanda size d�n�lecektir.';
      $UyariMesaj = "<b>$post_EPosta</b> adresine �yelik aktivasyon maili g�nderilemedi�inden kullan�c� �ye olamad�! E-Posta sistemi �al��m�yor! �ye olamayan m��terinin telefonu $post_Telefon";
      UyariEkle($UyariMesaj);
     }
   }
   else
     $Mesaj = 'Belirtti�iniz E-Posta adresinde bir kullan�c� mevcut!';
}
$smarty->assign('Vilayetler',$Vilayetler);
$smarty->assign('Ulkeler',$Ulkeler);
$smarty->assign('IslemUyari',$Mesaj);
?>
