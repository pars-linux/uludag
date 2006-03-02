<?php
if($post_EkDuzenle){
$sql = "SELECT No,Sayfa,Hit,Ek FROM SayfalarHit WHERE Sayfa LIKE '%$post_Kategori%'";
$Sonuc=sorgula($sql);
		while(list($vt_No,$Sayfa,$Hit,$Ek)=getir($Sonuc)) {
			$NoAd			= 'post_'.$vt_No;
 			$NoDeger		= $$NoAd;
			$updateSql = "UPDATE SayfalarHit SET Ek='$NoDeger' WHERE No='$vt_No'";
 			sorgula($updateSql);
		 			
		} // while
}

if($post_Kategori<>''){
$Sql= "SELECT No,Sayfa,Hit,Ek FROM SayfalarHit WHERE Sayfa LIKE '%$post_Kategori%'";
$Sonuc=sorgula($Sql);
$i=0;
while(list($vt_No,$vt_Sayfa,$vt_Hit,$vt_Ek)= getir($Sonuc)) {
	$HaberNoVar=strstr($vt_Sayfa,'&');
	if($HaberNoVar<>''){
		   $Istatistikler [$i]['No']	= $vt_No;
		   $Istatistikler [$i]['Hit']	= $vt_Hit;
		   $Istatistikler [$i]['Ek']	= $vt_Ek;
		   $numrows=$numrows+$vt_Hit;
		   $smarty->assign('AltKategoriToplam',$numrows);
		   
	  //Haberler içinde ara...
	  	if($post_Kategori=="Haberler"){
		//Sayýyý al
		list($sol,$orta,$sayi)=explode('=',$vt_Sayfa);
		$Istatistikler [$i]['Sayfa']	= $sayi;
		//Sadece Haberler Sayfasýna girilmiþse...
		$sql = "SELECT No,Baslik,Icerik,Kaynak,Durum,Manset,Tarih FROM IcerikHaber WHERE No='$sayi' ORDER BY No DESC";		
		$sonuc = sorgula($sql);
		while(list($vt_No,$vt_Baslik,$vt_Icerik,$vt_Kaynak,$vt_Durum,$vt_Manset,$vt_Tarih) = getir($sonuc))
		{
			$HaberNoVar=strstr($vt_Sayfa,'&');
			if($HaberNoVar<>''){
			$Istatistikler [$i]['Konu']	= $vt_Baslik;
			}
		}//while
		}//post kategori
	  	
	  //Etkinlikler
	  if($post_Kategori=="Etkinlikler"){
	  	//Sayýyý al
		list($sol,$orta,$sayi)=explode('=',$vt_Sayfa);
		$Istatistikler [$i]['Sayfa']	= $sayi;
		//Sadece Haberler Sayfasýna girilmiþse...
		$sql = "SELECT No,Baslik,Icerik,Tarih,BitisTarihi,Durum FROM IcerikEtkinlikler WHERE No='$sayi' ORDER BY No DESC ";		
		$sonuc = sorgula($sql);
		while(list($vt_EtkinlikNo,$vt_EtkinlikBaslik,$vt_EtkinlikIcerik,$vt_EtkinlikTarih,$vt_EtkinlikBitisTarih,$vt_EtkinlikDurum) = getir($sonuc))
		{
			$HaberNoVar=strstr($vt_Sayfa,'&');
			if($HaberNoVar<>''){
			$Istatistikler [$i]['Konu']	= $vt_EtkinlikBaslik;
			}
		}//while
		}//post kategori
		
	  //Söyleþiler
	  	if($post_Kategori=="Soylesi"){
	  	//Sayýyý al
		list($sol,$orta,$sayi)=explode('=',$vt_Sayfa);
		$Istatistikler [$i]['Sayfa']	= $sayi;
		//Sadece Haberler Sayfasýna girilmiþse...
		$sql = "SELECT No,Konu,Tarih,Kimle,Aktif,Slogan FROM IcerikSoylesi WHERE No='$sayi'";		
		$sonuc = sorgula($sql);
		while(list($vt_SoylesiNo,$vt_SoylesiKonu,$vt_SoylesiTarih,$vt_SoylesiKimle,$vt_SoylesiAktif,$vt_SoylesiSlogan) = getir($sonuc))
		{
			$HaberNoVar=strstr($vt_Sayfa,'&');
			if($HaberNoVar<>''){
			$Istatistikler [$i]['Konu']	= $vt_SoylesiKonu;
			}
		}//while
		}//post kategori
	  
	  //Makaleler
	  	if($post_Kategori=="Makaleler"){
	  	//Sayýyý al
		list($sol,$orta,$sayi)=explode('=',$vt_Sayfa);
		$Istatistikler [$i]['Sayfa']	= $sayi;
		//Sadece Haberler Sayfasýna girilmiþse...
		$sql = "SELECT No,Konu,Icerik,Tarih,Durum,Yazar FROM IcerikMakaleler WHERE No='$sayi'";		
		$sonuc = sorgula($sql);
		while(list($vt_MakaleNo,$vt_MakaleKonu,$vt_MakaleIcerik,$vt_MakaleTarih,$vt_MakaleDurum,$vt_MakaleYazar) = getir($sonuc))
		{
			$HaberNoVar=strstr($vt_Sayfa,'&');
			if($HaberNoVar<>''){
			$Istatistikler [$i]['Konu']	= $vt_MakaleKonu;
			}
		}//while
		}//post kategori
	  
	  //Hukuki Alt Yapi....
	  if($post_Kategori=="Hukuki_Alt_Yapi"){
	  	//Sayýyý al
		list($sol,$orta,$sayi)=explode('=',$vt_Sayfa);
		$Istatistikler [$i]['Sayfa']	= $sayi;
		//Sadece Haberler Sayfasýna girilmiþse...
		$sql = "SELECT No,KatNo,Icerik,Aciklama,Tarih,Kaynak FROM Mevzuatlar WHERE No='$sayi'";		
		$sonuc = sorgula($sql);
		while(list($vt_No,$vt_KatNo,$vt_Mevzuat,$vt_Aciklama,$vt_Tarih,$vt_Kaynak) = getir($sonuc))
		{
			$HaberNoVar=strstr($vt_Sayfa,'&');
			if($HaberNoVar<>''){
			$Istatistikler [$i]['Konu']	= $vt_Aciklama;
			}
		}//while
		}//post kategori
	 
	 	//Patent Nedir....
	  if($post_Kategori=="PatentNedir"){
	  	//Sayýyý al
		list($sol,$orta,$sayi)=explode('=',$vt_Sayfa);
		$Istatistikler [$i]['Sayfa']	= $sayi;
		//Sadece Haberler Sayfasýna girilmiþse...
		$sql = "SELECT No,Konu,Icerik,Durum FROM IcerikEImzaNedir WHERE No='$sayi'";		
		$sonuc = sorgula($sql);
		while(list($vt_No,$vt_Konu,$vt_Icerik,$vt_Durum) = getir($sonuc))
		{
			$HaberNoVar=strstr($vt_Sayfa,'&');
			if($HaberNoVar<>''){
			$Istatistikler [$i]['Konu']	= $vt_Konu;
			}
		}//while
		}//post kategori
	  
	  	//Köþe Yazýlarý Ýçinde Ara....
	if($post_Kategori=="KoseYazisi"){
		//Sayýyý al
		list($sol,$HaberSayi)=explode('&',$vt_Sayfa);
		list($sol,$sayi)=explode('=',$HaberSayi);
		$Istatistikler [$i]['Sayfa']	= $sayi;
		//Sadece Haberler Sayfasýna girilmiþse...
		$sql = "SELECT No,Konu,Icerik,Yazar,Tarih,Durum FROM IcerikKoseYazilari WHERE No='$sayi'";
		$sonuc = sorgula($sql);
		while(list($vt_YaziNo,$vt_YaziKonu,$vt_YaziIcerik,$vt_YaziYazar,$vt_YaziTarih,$vt_YaziDurum)= getir($sonuc))
		{
			
			$Istatistikler [$i]['Konu']	= $vt_YaziKonu;
			
		}//while
	}//post kategori
	
		//Köþe Yazýsý Yazarý Ýçinde Ara....
	if($post_Kategori=="YazarNo"){
		//Sayýyý al
		list($sol,$HaberSayi,$sag)=explode('&',$vt_Sayfa);
		list($sol,$sayi)=explode('=',$sag);
		$Istatistikler [$i]['Sayfa']= $sayi;
		//Sadece Haberler Sayfasýna girilmiþse...
		$sql = "SELECT No,Ad,Soyad,Unvan,Resim,Etiket,EPosta,WebAdres FROM KoseYazarlari WHERE No='$sayi'";
		$sonuc = sorgula($sql);
		while(list($vt_No,$vt_Ad,$vt_Soyad,$vt_Unvan,$vt_Resim,$vt_Etiket,$vt_EPosta,$vt_WebAdres)= getir($sonuc))
		{
			$Yazar=$vt_Unvan." ".$vt_Ad." ".$vt_Soyad;
			$Istatistikler [$i]['Konu']	= $Yazar;
			
		}//while
		$Yazar="1";
		$smarty->assign('Yazar',$Yazar);
	}//post kategori
	  }else{
	  	$numrows=$numrows+$vt_Hit;
		$smarty->assign('Toplam',$numrows);
	  }
	  $i++;
}
$smarty->assign('Kategori',$post_Kategori);
$smarty->assign('Istatistikler',$Istatistikler);
}
?>
