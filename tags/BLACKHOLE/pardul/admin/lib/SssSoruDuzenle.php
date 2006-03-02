<?
if ($post_SoruNo<>"")
{
 $get_SoruNo = $post_SoruNo;
 $get_SoruGoster = $post_SoruKategoriNo;
}// if ($post_SoruNo<>"")


//////////////////////////////////////////////////////////////////////////////////////
//Soru ve Cevap güncelleniyor
if ($post_SoruGuncelle<>"")
{
  $Soru = addslashes($post_Soru);
  $Cevap = addslashes($post_Cevap);
  $Sql = "UPDATE SssSorular SET Soru='$Soru',Cevap='$Cevap' WHERE No=$post_SoruNo ";
  $Sql.= "AND KatNo=$post_SoruKategoriNo";
  sorgula($Sql);
}//if ($SoruGuncelle<>"")
/////////////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////////////
//Soru bulunacak
if ($get_SoruNo<>"")
{
   $SoruNo = $get_SoruNo;
   $SoruKategoriNo = $get_SoruGoster;
   $Sql = "SELECT Soru,Cevap FROM SssSorular WHERE No=$SoruNo AND KatNo=$SoruKategoriNo";
   $Sonuc = sorgula($Sql);
   list($vt_Soru,$vt_Cevap) = getir($Sonuc);
   $Soru = stripslashes($vt_Soru);
   $Cevap = stripslashes($vt_Cevap);

   $smarty->assign('Soru',$Soru);
   $smarty->assign('Cevap',$Cevap);
   $smarty->assign('SoruNo',$SoruNo);
   $smarty->assign('SoruKategoriNo',$SoruKategoriNo);
   $Duzenlenecek = "Soru";
}
//////////////////////////////////////////////////////////////////////////////////////

$smarty->assign('Duzenlenecek',$Duzenlenecek);
?>
