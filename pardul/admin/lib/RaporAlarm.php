<?
// {{{ Gerekli Bilgiler
$AlarmTurler = array();
$AlarmTurler['Fiyat'] = 'Fiyat';
$AlarmTurler['Stok'] = 'Stok';

$AlarmDurumlar = array();
$AlarmDurumlar['YeniEklendi'] = 'Bekliyor';
$AlarmDurumlar['Uyarildi'] = 'Kullanýcý Uyarýldý';


$Kategoriler = KategoriSelect();

$smarty->assign('AlarmTurler',$AlarmTurler);
$smarty->assign('AlarmDurumlar',$AlarmDurumlar);
$smarty->assign('Kategoriler',$Kategoriler);
// }}}
// {{{ Sayfaya gelen degiskenler
if($post_Gore)
	$Bilgiler['Gore'] = $post_Gore;
else	
	{
	$post_Gore = 'EnUzunGore';
	$Bilgiler['Gore'] = 'EnUzunGore';
	}

if($post_Gore=='UruneGore')
	{
	if($post_KategoriNo)
		{
		$Bilgiler['KategoriNo'] = $post_KategoriNo;
		$SorguEkler[] = "K.No='$post_KategoriNo'";
		}
	}
else if($post_Gore=='KullaniciyaGore')
	{
	if($post_KullaniciAd)
		{
		$Bilgiler['KullaniciAd'] = $post_KullaniciAd;
		$SorguEkler[] = "KUL.EPosta LIKE '%$post_KullaniciAd%'";
		}
	}
if($post_EnUzunSayi)
	{
	$Bilgiler['EnUzunSayi'] = $post_EnUzunSayi;
	$SorguSonEk = "LIMIT 0,$post_EnUzunSayi";
	}
else	{
	$Bilgiler['EnUzunSayi'] = 10;
	$SorguSonEk = "LIMIT 0,10";
	}
if($post_AlarmTur)
	{
	$Bilgiler['AlarmTur'] = $post_AlarmTur;
	$SorguEkler[] = "A.Tur='$post_AlarmTur'";
	}
if($post_AlarmDurum)
	{
	$Bilgiler['AlarmDurum'] = $post_AlarmDurum;
	$SorguEkler[] = "A.Durum='$post_AlarmDurum'";
	}
$smarty->assign('Bilgiler',$Bilgiler);
// }}}
// {{{ Kayitlar Listeleniyor
if(count($SorguEkler))
	$SorguEk = " AND ".implode(" AND ",$SorguEkler);
else	$SorguEk = "";
$Sorgu1 = sorgula("SELECT K.KatAd,KUL.EPosta,U.Marka,U.Model,A.Tur,A.Durum,KUL.AdSoyad,A.EklenmeZaman FROM Urunler U,KullaniciAlarm A,UrunKategoriler K,Kullanicilar KUL WHERE A.UrunNo=U.No AND U.KatNo=K.No AND KUL.No=A.KullaniciNo$SorguEk ORDER BY A.EklenmeZaman $SorguSonEk");
for($i=0;list($vt_Kategori,$vt_EPosta,$vt_Marka,$vt_Model,$vt_Tur,$vt_Durum,$vt_KullaniciAd,$vt_EklenmeZaman) = getir($Sorgu1);$i++)
	{
        $vt_Urun = $vt_Marka.' '.$vt_Model;
	if($vt_Durum == 'YeniEklendi')
		$vt_Durum = 'Bekliyor...';
	else	$vt_Durum = 'Kullanýcý Uyarýldý';
	$Liste[$i]['Kullanici'] = $vt_KullaniciAd;
	$Liste[$i]['EPosta'] = $vt_EPosta;
	$Liste[$i]['Kategori'] = $vt_Kategori;
	$Liste[$i]['Urun'] = $vt_Urun;
	$Liste[$i]['AlarmTur'] = $vt_Tur;
	$Liste[$i]['AlarmDurum'] = $vt_Durum;
	$Liste[$i]['EklenmeTarih'] = tarihgetir($vt_EklenmeZaman,"tamgun");
	}
if($i==0)
	$smarty->assign('SonucYok',true);
$smarty->assign('Liste',$Liste);
// }}}
?>
