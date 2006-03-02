<?php
if($get_Anahtar){
$Arama=1;
$smarty->assign('Arama',$Arama);
$kelime=$get_Anahtar;
$Sql= "SELECT No,Kelime,Aciklama FROM IcerikSozluk WHERE Kelime='$kelime'";
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
?>
