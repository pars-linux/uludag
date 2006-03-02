<?
require_once("$INI_OrtakDosyalarDizin/functions/mail.php");
	if($get_No) $No = $get_No; else $No = $post_No;
	//{{{ bilgiler alýnýyor
	$Sql = "SELECT AdSoyad,EPosta,Mesaj,TarihSaat,Cevap,Cevaplayan,CevapTarih FROM GorusOneri WHERE No='$No'";
	$Sonuc = sorgula($Sql);
	list($AdSoyad,$EPosta,$Mesaj,$TarihSaat,$Cevap,$Cevaplayan,$CevapTarih) = getir($Sonuc);
	$Mesaj = stripslashes($Mesaj);
	$smarty->assign('Mesaj',$Mesaj);	
	$smarty->assign('AdSoyad',$AdSoyad);	
	$smarty->assign('EPosta',$EPosta);	
	$smarty->assign('GondermeTarih',TarihGetir($TarihSaat,'tam'));
	$smarty->assign('Cevap',stripslashes($Cevap));	
	$smarty->assign('Cevaplayan',$Cevaplayan);	
	$smarty->assign('CevapTarih',TarihGetir($CevapTarih,'tam'));
	//}}}

	if ($post_Gonder) {
		$KullaniciEPosta = $EPosta;
		$SqlKontrol = "SELECT No FROM GorusOneri WHERE No='$No' AND Cevap='$post_Cevap'";
		$SonucKontrol = sorgula($SqlKontrol);
		if(!$SonucKontrol->numRows()) {
			$Cevap = stripslashes($post_Cevap);
		    $EPostaBaslik = "deneme";
        	$EPostaDegiskenler['AdSoyad']    = $AdSoyad;
	        //$EPostaDegiskenler['Mesaj']      = $Mesaj;
    	    $EPostaDegiskenler['Cevap']      = $Cevap;
        	$EPostaDegiskenler['MesajTarih'] = TarihGetir($TarihSaat,'tamgun');
        	$EPostaTur="Html";
		    $EPosta=new Ileti();
   		    $EPosta->IcerikHazir('Tavsiye',$EPostaDegiskenler,$EPostaTur);
        	$EPosta->Baslik($EPostaBaslik);
	        $EPosta->Gonderen($sistem_VarsayilanGonderen);
    	    
        	if(!$EPosta->Gonder($KullaniciEPosta)) {
				$HataMesaj = 'E-Posta gönderilemedi!';
			} else	{
				$Simdi = Simdi();
				$YoneticiAd = $OturumKullaniciAd;
				$Sql = "UPDATE GorusOneri SET Cevap='$post_Cevap',CevapDurum='Cevaplandi',AktifPasif='Pasif',CevapTarih='$Simdi',Cevaplayan='$YoneticiAd' WHERE No='$No'";
				sorgula($Sql);
			}
			$smarty->assign('HataMesaj',$HataMesaj);
		}
	//{{{ bilgiler alýnýyor
	$Sql = "SELECT AdSoyad,EPosta,Mesaj,TarihSaat,Cevap,Cevaplayan,CevapTarih FROM GorusOneri WHERE No='$No'";
	$Sonuc = sorgula($Sql);
	list($AdSoyad,$EPosta,$Mesaj,$TarihSaat,$Cevap,$Cevaplayan,$CevapTarih) = getir($Sonuc);
	$Mesaj = stripslashes($Mesaj);
	$smarty->assign('Mesaj',$Mesaj);	
	$smarty->assign('AdSoyad',$AdSoyad);	
	$smarty->assign('EPosta',$EPosta);	
	$smarty->assign('GondermeTarih',TarihGetir($TarihSaat,'tam'));
	$smarty->assign('Cevap',stripslashes($Cevap));	
	$smarty->assign('Cevaplayan',$Cevaplayan);	
	$smarty->assign('CevapTarih',TarihGetir($CevapTarih,'tam'));
	//}}}
	}
	$smarty->assign('No',$No);
?>
