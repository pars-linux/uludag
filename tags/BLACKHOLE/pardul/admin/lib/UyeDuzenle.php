<?
$EPostaKimden = $sistem_SifremiUnuttumAdres;
$EPostaTur = $sistem_SifremiUnuttumGonderimSekli;
if ($get_UyeNo) $UyeNo = $get_UyeNo; else $UyeNo = $post_UyeNo;
$post_EPosta=$post_EPosta1;
$Vilayetler = VilayetlerSelect('Bos');
$Ulkeler = UlkelerSelect('Bos');
//{{{ Üye silinecekse
if ($get_Sil&&YetkiKontrol('UyeSilme'))
{
  $Sql = "DELETE FROM Kullanicilar WHERE No='$UyeNo'";
  if (sorgula($Sql))
  {
    ?>
     <script>
       alert('Üye Silindi');
       self.close();
       self.opener.location.reload();
     </script>
    <?
  
  }
}
//}}}
//{{{ Yeni þifre gönderilecekse
if ($get_SifreGonder&&YetkiKontrol('UyeSifreGonderme'))
{
  $Sql = "SELECT AdSoyad,EPosta FROM Kullanicilar WHERE No='$UyeNo'";
  $Sonuc = sorgula($Sql);
  $KayitSayi = $Sonuc->numRows();
  list($AdSoyad,$EPostaAdres) = getir($Sonuc);
  if ($KayitSayi>0) //eðer gerçekten böyle bir kullanýcý varsa
  {
     //Yeni þifresini gönderelim
     $UyeYeniSifre = Rastgele(6,'TamKarisik');
     $YeniSifre = md5($UyeYeniSifre);
     $Degiskenler['AdSoyad']   = $AdSoyad;
     $Degiskenler['YeniSifre'] = $UyeYeniSifre;
     $EMail=new Ileti();
     $EMail->IcerikHazir('Sifremi Unuttum',$Degiskenler,$EPostaTur);
     $EMail->Baslik('Yeni Þifreniz');
     $EMail->Gonderen($EPostaKimden);
     if ($EMail->Gonder($EPostaAdres)) //mail gönderilebildiyse deðiþikliði yapabiliriz
     {
       $Sql = "UPDATE Kullanicilar SET Sifre='$YeniSifre' WHERE EPosta='$EPostaAdres'";
       sorgula($Sql);
       $Mesaj = 'Yeni þifre gönderildi.';
     }
     else
     {
        $Mesaj = "E-Posta sistemindeki bir problemden dolayý yeni þifre gönderilemedi!";
     }
  }
  else
     $Mesaj = 'Hatalý E-Posta adresi!';
  $smarty->assign('Mesaj',$Mesaj);
}
//}}}
//{{{ Üye bilgileri güncellenecekse
if ($post_Guncelle&&YetkiKontrol('UyeGuncelleme'))
{
  //gold kart no ve epostanýn önceki deðerlerden farklý olup olmadýðýna bakalým
  $Sql = "SELECT EPosta FROM Kullanicilar WHERE No='$UyeNo'";
  $Sonuc = sorgula($Sql); 
  list($OncekiEPosta) = getir($Sonuc);

  $EPostaIslemTamam = true;
 
  /*if ($OncekiEPosta<>$post_EPosta)
  {
      echo "E Posta ile baðlantýlý herþey deðiþmeli";
  } */
  
  ///
  
  if ($post_HaberListe=='on')
    $post_HaberListe='Evet';
  else 
    $post_HaberListe='Hayir';
   
  if ($post_MMNMBasvuru=='on')
    $post_MMNMBasvuru='Evet';
  else 
    $post_MMNMBasvuru='Hayir';  
    
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

  $Sql1 = "UPDATE Kullanicilar SET 
          AdSoyad='$post_AdSoyad',        
          EPosta='$post_EPosta',
          FirmaAd='$post_FirmaAd',
          FirmaUnvan='$post_FirmaUnvan',
          TelNo='$post_TelNo',	          
          FaxNo='$post_FaxNo',
          Ulke='$post_Ulke',          
          Adres='$post_Adres',
          VergiNo='$post_VergiNo', 
          VergiDaire='$post_VergiDaire',
          WebAdres='$post_WebAdres',
          UrunCesit='$post_UrunCesit',
          EANTip='$post_EANTip',		
          MMNMVekalet='$post_MMNMVekalet',
          TOFBelge='$post_TOFBelge',		
          OzelVekalet='$post_OzelVekalet',
          GelirTablosu='$post_GelirTablosu',		
          SicilGazete='$post_SicilGazete',         
          Vilayet='$post_Vilayet',          
          TescilNo='$post_TescilNo',
          DosyaNo='$post_DosyaNo',
          HaberListe='$post_HaberListe',MMNMBasvuru='$post_MMNMBasvuru' WHERE No='$UyeNo'";           
  		  
  		  $Uyari="Güncelleme Ýþlemi Baþarý ile Tamamlanmýþtýr!!! ";
          $smarty->assign('Uyari',$Uyari);          
          if ($EPostaIslemTamam)  sorgula($Sql1);
  		
  
 }//guncelle

/////////////////}}}
//{{{Üye bilgileri alýnýyor
if($UyeNo)
{
   
  $Sql = "SELECT No,AdSoyad,FirmaUnvan,FirmaAd,EPosta,Sifre,TelNo,Adres,Vilayet,Ulke,FaxNo,VergiDaire,VergiNo,WebAdres,UrunCesit,EANTip,HaberListe,UyelikTarih,UyelikOnay,MMNMVekalet,TOFBelge,OzelVekalet,GelirTablosu,SicilGazete,AktivasyonKod,SonGiris,TescilNo,DosyaNo,MMNMBasvuru FROM Kullanicilar WHERE No='$UyeNo'"; 
  $Sonuc = sorgula($Sql);
  list($vt_No,$vt_AdSoyad,$vt_FirmaUnvan,$vt_FirmaAd,$vt_EPosta,$vt_Sifre,$vt_TelNo,$vt_Adres,$vt_Vilayet,$vt_Ulke,$vt_FaxNo,$vt_VergiDaire,$vt_VergiNo,$vt_WebAdres,$vt_UrunCesit,$vt_EANTip,$vt_HaberListe,$vt_UyelikTarih,$vt_UyelikOnay,$vt_MMNMVekalet,$vt_TOFBelge,$vt_OzelVekalet,$vt_GelirTablosu,$vt_SicilGazete,$vt_AktivasyonKod,$vt_SonGiris,$vt_TescilNo,$vt_DosyaNo,$vt_MMNMBasvuru)=getir($Sonuc);  
  $Uye['No']              = $vt_No;
  $Uye['AdSoyad']         = $vt_AdSoyad;  
  $Uye['EPosta']          = $vt_EPosta;  
  $Uye['FirmaAd'] 	      = $vt_FirmaAd;  
  $Uye['FirmaUnvan']      = $vt_FirmaUnvan;  
  $Uye['TelNo']    	      = $vt_TelNo;  
  $Uye['FaxNo']           = $vt_FaxNo;  
  $Uye['Ulke']     	      = $vt_Ulke;  
  $Uye['UyelikTarih']     = $vt_UyelikTarih;  
  $Uye['Adres']           = $vt_Adres;  
  $Uye['Vilayet']         = $vt_Vilayet;
  $Uye['VergiNo']         = $vt_VergiNo;
  $Uye['VergiDaire']  	  = $vt_VergiDaire;
  $Uye['WebAdres']  	  = $vt_WebAdres;
  $Uye['UrunCesit']	      = $vt_UrunCesit;
  $Uye['EANTip']	      = $vt_EANTip;
  $Uye['DosyaNo']	      = $vt_DosyaNo;
  $Uye['TescilNo']	      = $vt_TescilNo;
  
  //$Uye['MMNMVekalet']	  = $vt_MMNMVekalet;
  //$Uye['TOFBelge']	      = $vt_TOFBelge;
  //$Uye['OzelVekalet']	  = $vt_OzelVekalet;
  //$Uye['GelirTablosu']	  = $vt_GelirTablosu;
  //$Uye['SicilGazete']	  = $vt_SicilGazete;

  if ($vt_HaberListe=='Evet')
    $Uye['HaberListe']  = true;  
  else 
    $Uye['HaberListe']  = false;
    
  if ($vt_MMNMBasvuru=='Evet')
    $Uye['MMNMBasvuru']  = true;  
  else 
    $Uye['MMNMBasvuru']  = false;  
    
  if ($vt_MMNMVekalet=='Var')
    $Uye['MMNMVekalet']  = true;  
  else 
    $Uye['MMNMVekalet']  = false;
    
    if ($vt_TOFBelge=='Var')
    $Uye['TOFBelge']  = true;  
  else 
    $Uye['TOFBelge']  = false;
    
    if ($vt_OzelVekalet=='Var')
    $Uye['OzelVekalet']  = true;  
  else 
    $Uye['OzelVekalet']  = false;
    
    if ($vt_GelirTablosu=='Var')
    $Uye['GelirTablosu']  = true;  
  else 
    $Uye['GelirTablosu']  = false;
    
    if ($vt_SicilGazete=='Var')
    $Uye['SicilGazete']  = true;  
  else 
    $Uye['SicilGazete']  = false;  
  
  
  
  $smarty->assign('Uye',$Uye);
  $smarty->assign('Vilayetler',$Vilayetler); 
  $smarty->assign('Ulkeler',$Ulkeler); 
  
  
}
//}}}
?>
