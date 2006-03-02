<?php
//Max Sirayý Bul
 $Sql = "SELECT MAX(Sira) AS Sira FROM SSMModul WHERE AnaNo=0";
 $Sonuc = sorgula($Sql);
 list($vt_Sira) = getir($Sonuc);
 $MaxSira = $vt_Sira;
 

/*------------------Üst Kategorilerin Aþaðý Yukarý Sýralanmasý-------------------*/ 
if($get_KYukari){
	$Sql = "SELECT Sira FROM SSMModul WHERE No=$get_No";
  	$Sonuc = sorgula($Sql);
  	list($vt_Sira) = getir($Sonuc);
 	$GelenSira = $vt_Sira;
	
	$YeniSira = $GelenSira-1;
	$Sql = "SELECT No FROM SSMModul WHERE Sira=$YeniSira AND AnaNo=0";
    $Sonuc = sorgula($Sql);
    list($vt_No) = getir($Sonuc);
    $YukaridakiNo = $vt_No;
    
    $Sql = "UPDATE SSMModul SET Sira=$YeniSira WHERE No=$get_No";
    sorgula($Sql);
    
    $Sql = "UPDATE SSMModul SET Sira=$GelenSira WHERE No=$YukaridakiNo";
    sorgula($Sql);
}
if ($get_KAsagi==1)
  {
  $Sql = "SELECT Sira FROM SSMModul WHERE No=$get_No";
  $Sonuc = sorgula($Sql);
  list($vt_Sira) = getir($Sonuc);
  $GelenSira = $vt_Sira;
  
    $YeniSira = $GelenSira+1;
    $Sql = "SELECT No FROM SSMModul WHERE Sira=$YeniSira AND AnaNo=0";
    $Sonuc = sorgula($Sql);
    list($vt_No) = getir($Sonuc);
    $AsagidakiNo = $vt_No;
    $Sql = "UPDATE SSMModul SET Sira=$YeniSira WHERE No=$get_No";
    sorgula($Sql);
    $Sql = "UPDATE SSMModul SET Sira=$GelenSira WHERE No=$AsagidakiNo";
    sorgula($Sql);
  }
/*-------------------------Alt Kategorilerin Sýralanmasý--------------------*/ 
if($get_AYukari){
	$Sql = "SELECT Sira FROM SSMModul WHERE No=$get_No";
  	$Sonuc = sorgula($Sql);
  	list($vt_Sira) = getir($Sonuc);
 	$GelenSira = $vt_Sira;
	
	$YeniSira = $GelenSira-1;
	$Sql = "SELECT No FROM SSMModul WHERE Sira=$YeniSira AND AnaNo>0";
    $Sonuc = sorgula($Sql);
    list($vt_No) = getir($Sonuc);
    $YukaridakiNo = $vt_No;
    
    $Sql = "UPDATE SSMModul SET Sira=$YeniSira WHERE No=$get_No";
    sorgula($Sql);
    
    $Sql = "UPDATE SSMModul SET Sira=$GelenSira WHERE No=$YukaridakiNo";
    sorgula($Sql);
}
if ($get_AAsagi==1)
  {
  $Sql = "SELECT Sira FROM SSMModul WHERE No=$get_No";
  $Sonuc = sorgula($Sql);
  list($vt_Sira) = getir($Sonuc);
  $GelenSira = $vt_Sira;
  
    $YeniSira = $GelenSira+1;
    $Sql = "SELECT No FROM SSMModul WHERE Sira=$YeniSira AND AnaNo>0";
    $Sonuc = sorgula($Sql);
    list($vt_No) = getir($Sonuc);
    $AsagidakiNo = $vt_No;
    $Sql = "UPDATE SSMModul SET Sira=$YeniSira WHERE No=$get_No";
    sorgula($Sql);
    $Sql = "UPDATE SSMModul SET Sira=$GelenSira WHERE No=$AsagidakiNo";
    sorgula($Sql);
  }
/*-------------------------------------Silme Ýþlemi------------------------------*/
if ($get_SSayfa&&YetkiKontrol('SSMModulSilme'))
{
  $SilinecekNo = $get_SSayfa;
  $Sql = "DELETE FROM SSMModul WHERE No=$SilinecekNo";
  sorgula($Sql);
  $Uyari="Ýþleminiz Baþarý ile Tamamlanmýþtýr.";
  $smarty->assign('Uyari',$Uyari); 	
}


/*----------------------Menu Elemanlarýný Listele--------------------------------*/
$Sql = "SELECT No,AnaNo,Sira,Baslik,Adres,MenuDurum FROM SSMModul WHERE AnaNo=0 ORDER BY Sira ASC";
$Sonuc = sorgula($Sql);
$i=0;
while(list($vt_No,$vt_AnaNo,$vt_Sira,$vt_Baslik,$vt_Adres,$vt_MenuDurum)=getir($Sonuc)){
	/*Max alt kategori*/
	$Sql3 = "SELECT MAX(Sira) AS Sira FROM SSMModul WHERE MenuDurum='EvetAltKategori' AND AnaNo='$vt_No'";
	$Sonuc3 = sorgula($Sql3);
 	list($vt_SiraKontrol) = getir($Sonuc3);
 	$AMaxSira = $vt_SiraKontrol;
	
	//echo $AMaxSira."<br>";
	$Sayfalar[$i]["Baslik"] = $vt_Baslik;
	$Sayfalar[$i]["Adres"]  = $vt_Adres;
	$Sayfalar[$i]["No"]	    = $vt_No;
	$Sql1 = "SELECT No,AnaNo,Sira,Baslik,Adres,MenuDurum FROM SSMModul WHERE AnaNo=$vt_No ORDER BY Sira ASC";
	$Sonuc1 = sorgula($Sql1);
	
	$t=0;
    while(list($vt1_No,$vt1_AnaNo,$vt1_Sira,$vt1_Baslik,$vt1_Adres,$vt1_MenuDurum)=getir($Sonuc1)){
	
	$Sayfalar[$i]["AltMenu"][$t]["Baslik"] = $vt1_Baslik;
	$Sayfalar[$i]["AltMenu"][$t]["Adres"]  = $vt1_Adres;
	$Sayfalar[$i]["AltMenu"][$t]["No"]     = $vt1_No;
	
	
  			 if ($vt1_Sira==1)
    			 $Sayfalar[$i]["AltMenu"][$t]['Yukari'] =false;
 			  else
  			$Sayfalar[$i]["AltMenu"][$t]['Yukari'] = true;
   			 if ($vt1_Sira==$AMaxSira)
   			 $Sayfalar[$i]["AltMenu"][$t]['Asagi'] = false;
   			 else
   			 $Sayfalar[$i]["AltMenu"][$t]['Asagi'] = true;
	$t++;
    }
    if ($vt_Sira==1)
   		 $Sayfalar[$i]['Yukari'] = false;
   else
   		 $Sayfalar[$i]['Yukari'] = true;
   if ($vt_Sira==$MaxSira)
   		 $Sayfalar[$i]['Asagi'] = false;
   else
   		 $Sayfalar[$i]['Asagi'] = true;
	$i++;
	}
$smarty->assign('Sayfalar',$Sayfalar);

?>
