<?
$Sira = 0;
$Sorgu1 = sorgula("SELECT DISTINCT Kategori FROM Degiskenler WHERE Durum='Genel' ORDER BY Kategori");
for($i=0;list($vt_Kategori) = getir($Sorgu1);$i++)
	{
	$Sira++;
	$Kategoriler[$i]['Isim'] = $vt_Kategori;
	$Kategoriler[$i]['Sira'] = $Sira;
	$Degiskenler = array();
	$Sorgu2 = sorgula("SELECT No,Isim,Aciklama FROM Degiskenler WHERE Kategori='$vt_Kategori' AND Durum='Genel' ORDER BY Isim");
	for($j=0;list($vt_No,$vt_Isim,$vt_Aciklama) = getir($Sorgu2);$j++)
		{
		$Degiskenler[$j]['No'] = $vt_No;
		if($vt_No==$get_No)	
			$Kategoriler[$i]['Secili'] = true;
		$Degiskenler[$j]['Isim'] = $vt_Isim;
		$Degiskenler[$j]['Aciklama'] = $vt_Aciklama;
		}
	$Kategoriler[$i]['Degiskenler'] = $Degiskenler;
	}
$smarty->assign('Kategoriler',$Kategoriler);

if($post_Guncelle&&YetkiKontrol('DegiskenGuncelleme'))
	sorgula("UPDATE Degiskenler SET Deger='$post_Deger' WHERE No='$get_No'");

if($get_No)
	{
	$Sorgu1 = sorgula("SELECT Isim,Kategori,Deger,Degerler FROM Degiskenler WHERE No='$get_No'");
	list($vt_Isim,$vt_Kategori,$vt_Deger,$vt_Degerler) = getir($Sorgu1);
	$Bilgiler['No'] = $get_No;
	$Bilgiler['Isim'] = $vt_Isim;
	$Bilgiler['Deger'] = $vt_Deger;
	$Bilgiler['Kategori'] = $vt_Kategori;
	if($vt_Degerler)
		{
		$DegerIc = explode(",",$vt_Degerler);
		foreach($DegerIc as $Deger)
			$Degerler[$Deger] = $Deger;
		$smarty->assign('Degerler',$Degerler);
		}
	
	$smarty->assign('Bilgiler',$Bilgiler);
	}

$YeniKategoriler = array();
$Sorgu1 = sorgula("SELECT DISTINCT Kategori FROM Degiskenler WHERE Durum='Genel' ORDER BY Kategori");
while(list($vt_Kategori) = getir($Sorgu1))
	$YeniKategoriler[$vt_Kategori] = $vt_Kategori;
$smarty->assign('YeniKategoriler',$YeniKategoriler);
?>
