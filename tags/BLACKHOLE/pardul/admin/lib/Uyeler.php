<?
$Vilayetler = VilayetlerSelect('Tümü');
$smarty->assign('Vilayetler',$Vilayetler);

if ($post_Ara)
{
 $Sql = "SELECT No,AdSoyad,FirmaUnvan,FirmaAd,EPosta,Sifre,TelNo,Adres,Vilayet,Ulke,FaxNo,VergiDaire,VergiNo,WebAdres,UrunCesit,EANTip,HaberListe,UyelikTarih,UyelikOnay,MMNMVekalet,TOFBelge,OzelVekalet,GelirTablosu,SicilGazete,AktivasyonKod,SonGiris FROM Kullanicilar WHERE 1=1";
 $SqlEk='';
 if($post_AdSoyad)      $SqlEk.= " AND AdSoyad LIKE '%$post_AdSoyad%'"; 
 if($post_EPosta)       $SqlEk.= " AND EPosta LIKE '%$post_EPosta%'"; 
 if($post_FirmaAd) 		$SqlEk.= " AND FirmaAd LIKE '%$post_FirmaAd%'"; 
 if($post_Vilayet<>'')  $SqlEk.= " AND Vilayet='$post_Vilayet'"; 
 $Sql.=$SqlEk;
 $Sonuc = sorgula($Sql);
 $i = 0;
 while(list($vt_No,$vt_AdSoyad,$vt_FirmaUnvan,$vt_FirmaAd,$vt_EPosta,$vt_Sifre,$vt_TelNo,$vt_Adres,$vt_Vilayet,$vt_Ulke,$vt_FaxNo,$vt_VergiDaire,$vt_VergiNo,$vt_WebAdres,$vt_UrunCesit,$vt_EANTip,$vt_HaberListe,$vt_UyelikTarih,$vt_UyelikOnay,$vt_MMNMVekalet,$vt_TOFBelge,$vt_GelirTablosu,$vt_SicilGazete,$vt_AktivasyonKod,$vt_SonGiris)=getir($Sonuc))
 {
   $Uyeler[$i]['No']          = $vt_No;   
   $Uyeler[$i]['AdSoyad']     = $vt_AdSoyad;   
   $Uyeler[$i]['EPosta']      = $vt_EPosta;   
   $Uyeler[$i]['FirmaAd'] 	  = $vt_FirmaAd;
   $Uyeler[$i]['Vilayet'] 	  = $vt_Vilayet;
   $Uyeler[$i]['Tel'] 	 	  = $vt_TelNo;   
   $Uyeler[$i]['FirmaUnvan']  = $vt_FirmaUnvan;   
   $Uyeler[$i]['MMNMVekalet'] = $vt_MMNMVekalet;   
   $Uyeler[$i]['TOFBelge']    = $vt_TOFBelge; 
   $Uyeler[$i]['OzelVekalet'] = $vt_OzelVekalet;
   $Uyeler[$i]['GelirTablosu']= $vt_GelirTablosu;
   $Uyeler[$i]['SicilGazete'] = $vt_SicilGazete; 
   $Uyeler[$i]['UyelikTarih'] = TarihGetir($vt_UyelikTarih,'gun');
    
   $i++;
 }//while 
//{{{Sayfa linkleri ayarlanýyor
if ($Uyeler)
{
    $_GET['Grup'] = $post_SayfaNo;
    require_once "$KutuphaneDizin/Pear/Pager.php";

        $Degiskenler = array(
        'itemData' => $Uyeler,
        'perPage' => $sistem_UyeListeSayi,
        'delta' => 8,           // for 'Jumping'-style a lower number is better
        'append' => true,
        //'separator' => ' | ',
        'clearIfVoid' => false,
        'urlVar' => 'Grup',
        'useSessions' => true,
        'closeSession' => true,
        'mode'  => 'Sliding');  // Jumping de olabilir
        $SayfaAyrim = &new Pager($Degiskenler);
        $Uyeler = $SayfaAyrim->getPageData();
        $Kopruler = $SayfaAyrim->getLinks();

        $SonSayfa = $SayfaAyrim->numPages();
        if($SonSayfa > 1)       $smarty->assign('CokSayfali',true);
        if(!$post_SayfaNo)  $post_SayfaNo = 1;
        if($post_SayfaNo && $post_SayfaNo > 1 && $post_SayfaNo <= $SonSayfa)
                $smarty->assign('OncekiSayfa',"javascript:SayfaGonder(".($post_SayfaNo-1).");");
        if($SonSayfa > $post_SayfaNo)
                $smarty->assign('SonrakiSayfa',"javascript:SayfaGonder(".($post_SayfaNo+1).");");
        $SayfaKopruler = array();
        for($i=1;$i<=$SonSayfa;$i++)
                {
                if($i!=$post_SayfaNo)
                $SayfaKopruler[$i]['Adres'] = "javascript:SayfaGonder($i);";
                $SayfaKopruler[$i]['Isim'] = $i;
                }
        $smarty->assign('Sonuclar',$Sonuclar);
        $smarty->assign('SayfaKopruler',$SayfaKopruler);

}
//}}}
$smarty->assign('Uyeler',$Uyeler);
$smarty->assign('AdSoyad',$post_AdSoyad);
$smarty->assign('EPosta',$post_EPosta);
$smarty->assign('FirmaAd',$post_FirmaAd);
$smarty->assign('Vilayet',$post_Vilayet);
}//if($post_Ara)
?>
