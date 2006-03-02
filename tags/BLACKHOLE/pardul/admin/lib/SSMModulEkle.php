<?php
if($post_MenuEkle&&YetkiKontrol('MenuEkle')){
	if($post_MenuDurum=='Evet'){
	$Sql = "SELECT MAX(No),MAX(Sira) FROM SSMModul WHERE AnaNo=0 GROUP BY Baslik";
	$Sonuc = sorgula($Sql);
	list($No,$Sira)=getir($Sonuc);
	$Sira=$Sira+1;
	}else{
	
	$Sql = "SELECT MAX(No),MAX(Sira) FROM SSMModul WHERE AnaNo>0 GROUP BY Baslik";
	$Sonuc = sorgula($Sql);
	list($No,$Sira)=getir($Sonuc);
	$Sira=$Sira+1;	
	}
	 $Sql = "INSERT INTO SSMModul SET AnaNo='$post_Kategori',MenuDurum='$post_MenuDurum',Baslik='$post_Baslik',Adres='$post_Adres',Sira='$Sira'";
	 sorgula($Sql);
	 
	 $MenuId=$No+1;
	 $Sql2 = "INSERT INTO SSMModulIcerik SET MenuId='$MenuId',Icerik='$post_Icerik'";
	 sorgula($Sql2);
	
	$Uyari="Ýþleminiz Baþarý ile Tamamlanmýþtýr.";
    $smarty->assign('Uyari',$Uyari); 	
}

$Bolumler = array();
	/*$Dizin = opendir($INI_TemplateDizin);
	while($Dosya = readdir($Dizin))
		{
		if($Dosya == '.' || $Dosya == '..')
			continue;
		$Uzanti = substr(strrchr($Dosya,'.'),1);
		if(is_dir($INI_TemplateDizin.'/'.$Dosya))
			{
			$Dizin2 = opendir($INI_TemplateDizin.'/'.$Dosya);
			while($Dosya2 = readdir($Dizin2))
				{
				$Uzanti = substr(strrchr($Dosya2,'.'),1);
				if($Uzanti!='tpl')
					continue;
				$Bolumler[$Dosya.'/'.substr($Dosya2,0,strlen($Dosya2)-4)] = $Dosya.' / '.substr($Dosya2,0,strlen($Dosya2)-4);
				}
			continue;
			}
		if($Uzanti!='tpl')
			continue;
		$Bolumler[substr($Dosya,0,strlen($Dosya)-4)] = substr($Dosya,0,strlen($Dosya)-4);
		}
	asort($Bolumler);*/
	//Veri Tabnýndaki Sayfalarý Seç
	$Sql = "SELECT No,AnaNo,Sira,Baslik,Adres,MenuDurum FROM SSMModul WHERE AnaNo=0";
	$Sonuc = sorgula($Sql);
	while(list($vt_No,$vt_AnaNo,$vt_Sira,$vt_Baslik,$vt_Adres,$vt_MenuDurum)=getir($Sonuc)){
		$Bolumler[$vt_No]=$vt_Baslik;
	}
		
	$smarty->assign('YeniBolumler',$Bolumler);



?>
