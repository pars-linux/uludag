<?

if ($get_No) $No = $get_No; else $No = $post_No;
//{{{ 
if ($post_Guncelle)
{
  $Sql = "UPDATE IcerikSozluk SET 
          Kelime='$post_Kelime',
          Aciklama='$post_Aciklama'
          WHERE No='$No'";  
  $Sonuc=sorgula($Sql);
  $smarty->assign('TumSozcukler',$TumSozcukler); 
  $Uyari="Kayýt Ýþlemi Baþarý ile Tamamlanmýþtýr!!! ";
  $smarty->assign('Uyari',$Uyari);
}
$Sql= "SELECT No,Kelime,Aciklama FROM IcerikSozluk WHERE No='$No'";
$Sonuc=sorgula($Sql);
$i=0;
while(list($vt_No,$vt_Kelime,$vt_Aciklama)= getir($Sonuc)) {
			
			$smarty->assign('No',$vt_No);
			$smarty->assign('Kelime',$vt_Kelime);
			$smarty->assign('Aciklama',$vt_Aciklama);
		 	$i++;
	  }
//}}}
?>
