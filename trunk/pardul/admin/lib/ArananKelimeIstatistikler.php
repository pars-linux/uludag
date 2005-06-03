<?php
if($post_Ara)
{
	$Sql= "SELECT No,Kelime,ArananSayfaTur,AramaSayisi,SonBulunanKayitSayisi FROM ArananKelimeler WHERE 1=1";
	if($post_Kelime)      	    $SqlEk.= " AND Kelime LIKE '%$post_Kelime%'"; 
	if($post_ArananSayfa)       $SqlEk.= " AND ArananSayfaTur LIKE '%$post_ArananSayfa%'"; 
 	if($post_AramaSayisi)       $SqlEk.= " AND AramaSayisi='$post_AramaSayisi'";
 	 $Sql.=$SqlEk;
}else{
$Sql= "SELECT No,Kelime,ArananSayfaTur,AramaSayisi,SonBulunanKayitSayisi FROM ArananKelimeler ORDER BY AramaSayisi DESC LIMIT 0,100";
}
$Sonuc=sorgula($Sql);
$i=0;
while(list($vt_No,$vt_Kelime,$vt_ArananSayfaTur,$vt_AramaSayisi,$vt_SonBulunanKayitSayisi)= getir($Sonuc)) {

		   $ArananKelimeler [$i]['No']	= $vt_No;
		   $ArananKelimeler [$i]['ArananSayfa']	= $vt_ArananSayfaTur;
		   $ArananKelimeler [$i]['AramaSayisi']	= $vt_AramaSayisi;
		   $ArananKelimeler [$i]['KayitSayisi']	= $vt_SonBulunanKayitSayisi;
		   $ArananKelimeler [$i]['Kelime']		= $vt_Kelime;
		 $i++;
	  }
$smarty->assign('ArananKelimeler',$ArananKelimeler);
?>
