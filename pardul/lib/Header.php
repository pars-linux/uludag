<?
//{{{ Oturum varsa kullanýcý ad soyadýný ve sepetindeki ürün sayýsýný bulalým
if($OturumBilgiler['OturumKullaniciNo']) {
	$KullaniciNo = $OturumBilgiler['OturumKullaniciNo'];
}
//}}}}

//{{{ sayfada gösterilecek bannerý bulalým
$Sonuc = sorgula("SELECT No FROM Bannerlar WHERE Anasayfa='Rastgele'");
list($SeciliAnasayfaBanner) = getir($Sonuc);
if(!$SeciliAnasayfaBanner) {
    $Sonuc = sorgula("SELECT No FROM Bannerlar WHERE Anasayfa='Evet'");
    list($SeciliAnasayfaBanner) = getir($Sonuc);
	if(!$SeciliAnasayfaBanner)
		$SeciliAnasayfaBanner = 'Bos';
}
else
    $SeciliAnasayfaBanner = 'Rastgele';

switch($SeciliAnasayfaBanner) {
	case 'Bos':
		$BannerDosya = 'Bos';
	break;
	case 'Rastgele':
		$Sonuc = sorgula("SELECT Dosya FROM Bannerlar WHERE Tur='Genel' ORDER BY Rand() LIMIT 1");
		list($BannerDosya) = getir($Sonuc);
	break;
	default:
		$Sonuc = sorgula("SELECT Dosya FROM Bannerlar WHERE No='$SeciliAnasayfaBanner'");
		list($BannerDosya) = getir($Sonuc);
	break;
}

if($BannerDosya!='Bos')
	list($BannerDosya,$Uzanti) = explode('.',$BannerDosya);

$smarty->assign('BannerDosya',$BannerDosya);
//}}}

//{{{ Header Bolumu icin sayfaya gore resim adlarini atayalim. Default Resim Marka Islemlerine Ait.
// tamamen patentofisim.com'a ozel bir yapidir.
if (ereg("^Marka",$Page)) {
   $AktifMenuImg = "marka_on.gif";
   $AktifFooter  = "marka_footer.gif";
   if ($Page == "MarkaIslemler") {
   		$AktifMenuBg  = "marka_banner.gif";
   		$AktifHeaderForm = "MarkaBanner.tpl";
		} else {
		$AktifMenuBg  = "marka_bg.gif";
		$AktifHeaderForm = "MarkaForm.tpl";
		}
} else if (ereg("^Patent",$Page)) {
   $AktifMenuImg = "patent_on.gif";
   $AktifFooter  = "patent_footer.gif";
   if ($Page == "PatentIslemler") {
		$AktifMenuBg  = "patent_banner.gif";
   		$AktifHeaderForm = "PatentBanner.tpl";
		} else {
		$AktifMenuBg  = "patent_bg.gif";
		$AktifHeaderForm = "PatentForm.tpl";
		}
} else if (ereg("^Tasarim",$Page)) {
   $AktifMenuImg = "tasarim_on.gif";
   $AktifFooter  = "tasarim_footer.gif";
   if ($Page == "TasarimIslemler") {
   		$AktifMenuBg  = "tasarim_banner.gif";
   		$AktifHeaderForm = "TasarimBanner.tpl";
		} else {
		$AktifMenuBg  = "tasarim_bg.gif";
		$AktifHeaderForm = "TasarimForm.tpl";
		}
} else if (ereg("^Danisma",$Page)) {
   $AktifMenuImg = "danisma_on.gif";
   $AktifFooter  = "danisma_footer.gif";
   if ($Page == "DanismaOfisi") {
   		$AktifMenuBg  = "danisma_banner.gif";
   		$AktifHeaderForm = "DanismaBanner.tpl";
		} else {
		$AktifMenuBg  = "danisma_bg.gif";
		$AktifHeaderForm = "DanismaForm.tpl";
		}
} else if (ereg("^Yenileme",$Page)) {
   $AktifMenuImg = "yenileme_on.gif";
   $AktifFooter  = "yenileme_footer.gif";
   if ($Page == "YenilemeIslemler") {
   		$AktifMenuBg  = "yenileme_banner.gif";
   		$AktifHeaderForm = "YenilemeBanner.tpl";
		} else {
		$AktifMenuBg  = "yenileme_bg.gif";
		$AktifHeaderForm = "YenilemeForm.tpl";
		}
} else if (ereg("^Takip",$Page)) {
   $AktifMenuImg = "takip_on.gif";
   $AktifFooter  = "takip_footer.gif";
   if ($Page == "TakipIslemler") {
   		$AktifMenuBg  = "takip_banner.gif";
   		$AktifHeaderForm = "TakipBanner.tpl";
		} else {
		$AktifMenuBg  = "takip_bg.gif";
		$AktifHeaderForm = "TakipForm.tpl";
		}
} else {
   $AktifMenuImg = "marka_on.gif";
   $AktifMenuBg  = "marka_bg.gif";
   $AktifFooter  = "default_footer.gif";
   $AktifHeaderForm = "DefaultForm.tpl";
}

$smarty->assign('AktifMenuImg',$AktifMenuImg);
$smarty->assign('AktifMenuBg',$AktifMenuBg);
$smarty->assign('AktifFooterBg',$AktifFooter);
$smarty->assign('AktifHeaderForm',$AktifHeaderForm);

//}}}
?>
