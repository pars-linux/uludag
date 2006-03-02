<?
//error_reporting(E_ALL & ~E_NOTICE);
//{{{ Haber Silme
if ($get_SilNo)
{
  $Sql = "DELETE FROM IcerikSozluk WHERE No='$get_SilNo'"; 
  sorgula($Sql);
}
//}}}
$smarty->assign('IslemUyari',$Mesaj);
//}}}
//{{{ Yazi Ekle
if($post_Ekle){
	$Sql = "INSERT INTO IcerikSozluk SET
       Kelime 		='$post_Sozcuk',
       Aciklama	    ='$post_Aciklama'";
       sorgula($Sql);
       // Debug icin aciniz.
       //echo $Sql;
       $Uyari="Kayýt Ýþlemi Baþarý ile Tamamlanmýþtýr!!! ";
       $smarty->assign('Uyari',$Uyari);
}
//}}}
//{{{ Haberler Listeleme
if($post_YaziAra){
 $Sql = "SELECT No,Kelime,Aciklama FROM IcerikSozluk WHERE 1=1";
 if($post_Anahtar)       $SqlEk.= " AND (Kelime LIKE '%$post_Anahtar%' OR Aciklama LIKE '%$post_Anahtar%')"; 
 $Sql.=$SqlEk;
}else{
$Sql= "SELECT No,Kelime,Aciklama FROM IcerikSozluk ORDER BY Kelime";
}
$Sonuc=sorgula($Sql);
$i=0;
while(list($vt_No,$vt_Kelime,$vt_Aciklama)= getir($Sonuc)) {

		   $TumSozcukler [$i]['No']	    = $vt_No;
		   $TumSozcukler [$i]['Kelime']  = $vt_Kelime;
    	   $TumSozcukler [$i]['Aciklama']= $vt_Aciklama;
		$i++;
	  }
$smarty->assign('TumSozcukler',$TumSozcukler);
//}}}
?>
