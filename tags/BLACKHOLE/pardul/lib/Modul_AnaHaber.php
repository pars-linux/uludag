<?
//{{{ Haberler Cekiliyor: Aktif Olanlar...
 $Sql = "SELECT No,Baslik,Icerik,HaberSlogan,Resim FROM IcerikHaber WHERE Durum='Aktif' AND Manset='Pasif' ORDER BY No DESC LIMIT 0,1";
 $Sonuc = sorgula($Sql);
	$i = 0;
	$t=0;
	while(list($vt_No,$vt_Baslik,$vt_Icerik,$vt_HaberSlogan,$vt_Resim) = getir($Sonuc))
		{
		
		$Haberler[$i]['No']				= $vt_No;
		$Haberler[$i]['Baslik']			= $vt_Baslik;
		$Haberler[$i]['Icerik']			= $vt_Icerik;
		$Haberler[$i]['HaberSlogan']	= $vt_HaberSlogan;
		$Haberler[$i]['Resim']			= $vt_Resim;
		
		$i++;
		$t++;
	
		}
		$tdw = ceil(100/$i); // td width hesaplamasi..
$smarty->assign('tdw',$tdw);
$smarty->assign('Haberler',$Haberler);
//}}}
?>