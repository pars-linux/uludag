<?
if ($post_LinkNo<>"")
{
 $get_LinkNo = $post_LinkNo;
 $get_LinkGoster = $post_LinkKategoriNo;
}// if ($post_SoruNo<>"")


//////////////////////////////////////////////////////////////////////////////////////
//Soru ve Cevap güncelleniyor
if ($post_LinkGuncelle<>"")
{
  $Link = addslashes($post_Link);
  $Sql = "UPDATE Linkler SET Link='$Link',Aciklama='$post_Aciklama' WHERE No=$post_LinkNo ";
  $Sql.= "AND KatNo=$post_LinkKategoriNo";
  sorgula($Sql);
}//if ($SoruGuncelle<>"")
/////////////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////////////
//Soru bulunacak
if ($get_LinkNo<>"")
{
   $LinkNo = $get_LinkNo;
   $LinkKategoriNo = $get_LinkGoster;
   $Sql = "SELECT Link,Aciklama FROM Linkler WHERE No=$LinkNo AND KatNo=$LinkKategoriNo";
   $Sonuc = sorgula($Sql);
   list($vt_Link,$vt_Aciklama) = getir($Sonuc);
   $Link = stripslashes($vt_Link);
   $smarty->assign('Aciklama',$vt_Aciklama);
   $smarty->assign('Link',$Link);
   $smarty->assign('LinkNo',$LinkNo);
   $smarty->assign('LinkKategoriNo',$LinkKategoriNo);
   $Duzenlenecek = "Link";
}
//////////////////////////////////////////////////////////////////////////////////////

$smarty->assign('Duzenlenecek',$Duzenlenecek);
?>
