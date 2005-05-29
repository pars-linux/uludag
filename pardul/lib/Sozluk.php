<?php
if($get_Harf){
$Arama=1;
$smarty->assign('Arama',$Arama);
$harf=$get_Harf;
$Sql= "SELECT No,Kelime,Aciklama FROM IcerikSozluk WHERE (Kelime LIKE '$Harf%')";
$Sonuc=sorgula($Sql);
$numrows=$Sonuc->numRows();
$smarty->assign('Sayi',$numrows);
$i=0;
while(list($vt_No,$vt_Kelime,$vt_Aciklama)= getir($Sonuc)) {

		   $Harfler [$i]['No']	    = $vt_No;
		   $Harfler [$i]['Kelime']  = $vt_Kelime;
    	   $Harfler [$i]['Aciklama']= $vt_Aciklama;
		 $i++;
	  }
$smarty->assign('Harfler',$Harfler);
}
if($post_Ara){
$harf=$get_Harf;
$Sql= "SELECT No,Kelime,Aciklama FROM IcerikSozluk WHERE (Kelime LIKE '%$post_Anahtar%' OR Aciklama LIKE '%$post_Anahtar%')";
$Sonuc=sorgula($Sql);
$numrows=$Sonuc->numRows();
$smarty->assign('Sayi',$numrows);
$i=0;
while(list($vt_No,$vt_Kelime,$vt_Aciklama)= getir($Sonuc)) {

		   $Harfler [$i]['No']	    = $vt_No;
		   $Harfler [$i]['Kelime']  = $vt_Kelime;
    	   $Harfler [$i]['Aciklama']= $vt_Aciklama;
		 $i++;
	  }
	
$smarty->assign('Anahtar',$post_Anahtar);
$smarty->assign('Harfler',$Harfler);	
	
}
?>
