<?
// error_reporting(E_ALL);
require("$AdminAnaDizin/jscript/fckeditor.php");
require_once("$INI_OrtakDosyalarDizin/Fonksiyonlar/ileti.php");
// require("$AdminAnaDizin/jscript/editor/filemanager/browser/default/connectors/php/connector.php");
//{{{ Görüþü pasif yap
if($post_Cevapla)
{
	
	$No = $post_No;
	$Sql="SELECT No,AdSoyad,EPosta,KullaniciNo,Mesaj,TarihSaat,AktifPasif,CevapDurum FROM GorusOneri WHERE AktifPasif='Aktif' AND No='$No'";
	$Sonuc = sorgula($Sql);
	list($No,$AdSoyad,$EPosta,$KullaniciNo,$Mesaj,$TarihSaat,$AktifPasif,$CevapDurum)=getir($Sonuc);
			//echo $No.$AdSoyad.$EPosta.$KullaniciNo.$Mesaj.$TarihSaat.$AktifPasif.$CevapDurum;
			$EPostaKimden = $sistem_VarsayilanGonderen;
     		$EPostaTur    = $sistem_VarsayilanGonderimSekli;
			$KullaniciEPosta = $EPosta;
			$Cevap = stripslashes($post_Mesaj);
		    $EPostaBaslik = "Cevap Servisi";
        	$EPostaDegiskenler['AdSoyad']    = $AdSoyad;
	        $EPostaDegiskenler['Mesaj']      = $Mesaj;
    	    $EPostaDegiskenler['Cevap']      = $Cevap;
        	$EPostaDegiskenler['MesajTarih'] = TarihGetir($TarihSaat,'tamgun');
		    $EPosta=new Ileti();
   		    $EPosta->IcerikHazir('GorusCevapla',$EPostaDegiskenler,$EPostaTur);
        	$EPosta->Baslik($EPostaBaslik);
        	$EPosta->Gonderen($EPostaKimden);
    	    $EPosta->Gonder($EPosta);	
    	    if($EPosta->Gonder($EPosta)){
    		$sql="UPDATE GorusOneri SET CevapDurum='Cevaplandi' WHERE AktifPasif='Aktif' AND No='$No'";    
    		sorgula($sql);
    	    }
    	    	

}
//}}}



$Sql="SELECT No,AdSoyad,EPosta,KullaniciNo,Mesaj,TarihSaat,AktifPasif,CevapDurum from GorusOneri WHERE AktifPasif='Aktif' AND No='$get_No'";
$Sonuc = sorgula($Sql);
$i = 0;
while (list($No,$AdSoyad,$EPosta,$KullaniciNo,$Mesaj,$TarihSaat,$AktifPasif,$CevapDurum)=getir($Sonuc)) {
   $Dizi[$i]['No']          = $No;
   $Dizi[$i]['AdSoyad']     = $AdSoyad;
   $Dizi[$i]['EPosta']      = $EPosta;
   $Dizi[$i]['KullaniciNo'] = $KullaniciNo;
   $Dizi[$i]['Mesaj']       = $Mesaj;
   $Dizi[$i]['TarihSaat']   = TarihGetir($TarihSaat,'tam');
   $Dizi[$i]['AktifPasif']  = $AktifPasif;
   $Dizi[$i]['CevapDurum']  = $CevapDurum;
   $i++;
}
$smarty->assign('Dizi',$Dizi);
$smarty->assign('KayitSayi',count($Dizi));
if(!$post_AktifPasif) $post_AktifPasif = 'Aktif';
$smarty->assign('AdSoyad',$post_AdSoyad);
$smarty->assign('EPosta',$post_EPosta);
$smarty->assign('KullaniciNo',$post_KullaniciNo);
$smarty->assign('AktifPasif',$post_AktifPasif);
$smarty->assign('CevapDurum',$post_CevapDurum);
$smarty->assign('No',$No);

// echo $Config['UserFilesPath'];



?>
<?/*
	if($get_No) $No = $get_No; else $No = $post_No;
	//{{{ bilgiler al?n?yor
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
		    $EPostaBaslik = $post_Baslik;
        	$EPostaDegiskenler['AdSoyad']    = $AdSoyad;
	        $EPostaDegiskenler['Mesaj']      = $Mesaj;
    	    $EPostaDegiskenler['Cevap']      = $Cevap;
        	$EPostaDegiskenler['MesajTarih'] = TarihGetir($TarihSaat,'tamgun');
		    $EPosta=new Ileti();
   		    $EPosta->IcerikHazir('GorusCevapla',$EPostaDegiskenler,$sistem_VarsayilanGonderimSekli);
        	$EPosta->Baslik($EPostaBaslik);
	        $EPosta->Gonderen($sistem_VarsayilanGonderen);
    	    $Sonuc = $EPosta->Gonder($KullaniciEPosta);
        	if(!$Sonuc) {
				$HataMesaj = 'E-Posta gönderilemedi!';
			} else	{
				$Simdi = Simdi();
				$YoneticiAd = $OturumKullaniciAd;
				$Sql = "UPDATE GorusOneri SET Cevap='$post_Cevap',CevapDurum='Cevaplandi',AktifPasif='Pasif',CevapTarih='$Simdi',Cevaplayan='$YoneticiAd' WHERE No='$No'";
				sorgula($Sql);
			}
			$smarty->assign('HataMesaj',$HataMesaj);
		}
	//{{{ bilgiler al?n?yor
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
*/
?>
