<?
//{{{ Görüþü pasif yap
if($get_Sil&&YetkiKontrol('GorusSilme'))
{
 $Sql= "UPDATE GorusOneri SET AktifPasif='Pasif' WHERE No='$get_Sil'";
 sorgula($Sql);
}
//}}}


if ($post_Ara) {
	$Sql = "SELECT No,AdSoyad,EPosta,KullaniciNo,Mesaj,TarihSaat,AktifPasif,CevapDurum FROM GorusOneri WHERE 1=1";
	$SqlEk = '';
	if($post_AdSoyad)            $SqlEk.= " AND AdSoyad LIKE '%$post_AdSoyad%'";
    if($post_EPosta)             $SqlEk.= " AND EPosta LIKE '%$post_EPosta%'";
    if($post_AktifPasif<>'Tumu') $SqlEk.= " AND AktifPasif='$post_AktifPasif'";
    if($post_CevapDurum<>'')     $SqlEk.= " AND CevapDurum='$post_CevapDurum'";
    $Sql.=$SqlEk;
} else {
	$Sql="SELECT No,AdSoyad,EPosta,KullaniciNo,Mesaj,TarihSaat,AktifPasif,CevapDurum from GorusOneri WHERE AktifPasif='Aktif' ORDER BY TarihSaat DESC";
}

$Sonuc = sorgula($Sql);
	$numrows=$Sonuc->numRows();
	$smarty->assign('TumSayi',$numrows);
$i = 0;
while (list($No,$AdSoyad,$EPosta,$KullaniciNo,$Mesaj,$TarihSaat,$AktifPasif,$CevapDurum)=getir($Sonuc)) {
   $Dizi[$i]['No']          = $No;
   $Dizi[$i]['AdSoyad']     = $AdSoyad;
   $Dizi[$i]['EPosta']      = $EPosta;
   $Dizi[$i]['KullaniciNo'] = $KullaniciNo;
   $Dizi[$i]['Mesaj']       = substr($Mesaj,0,70);
   $Dizi[$i]['TarihSaat']   = TarihGetir($TarihSaat,'tam');
   $Dizi[$i]['AktifPasif']  = $AktifPasif;
   $Dizi[$i]['CevapDurum']  = $CevapDurum;
   $i++;
}
if(count($Dizi))
{
	//$post_SayfaNo=1;
	$_GET['Grup'] = $post_SayfaNo;
	require_once "$KutuphaneDizin/Pear/Pager.php";
	$Degiskenler = array(
	'itemData' => $Dizi,
	'perPage' => $sistem_UyeGorusSayi,
	'delta' => 8,		// for 'Jumping'-style a lower number is better
	'append' => true,
	//'separator' => ' | ',
	'clearIfVoid' => false,
	'urlVar' => 'Grup',
	'useSessions' => true,
	'closeSession' => true,
	'mode'  => 'Sliding');  // Jumping de olabilir
	$SayfaAyrim = &new Pager($Degiskenler);
	$Dizi = $SayfaAyrim->getPageData();
	$Kopruler = $SayfaAyrim->getLinks();

	$SonSayfa = $SayfaAyrim->numPages();
	if($SonSayfa > 1)	$smarty->assign('CokSayfali',true);
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
$smarty->assign('Dizi',$Dizi);
$smarty->assign('KayitSayi',count($Dizi));
if(!$post_AktifPasif) $post_AktifPasif = 'Aktif';
$smarty->assign('AdSoyad',$post_AdSoyad);
$smarty->assign('EPosta',$post_EPosta);
$smarty->assign('KullaniciNo',$post_KullaniciNo);
$smarty->assign('AktifPasif',$post_AktifPasif);
$smarty->assign('CevapDurum',$post_CevapDurum);
?>
