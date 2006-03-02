<?


if ($post_LinkKategoriNo<>"")
{
 $get_LinkKategoriNo = $post_LinkKategoriNo;
}

//////////////////////////////////////////////////////////////////////////////////////
//SSS Kategorisi güncelleniyor
if ($post_KategoriGuncelle<>"")
{
  $Sql = "UPDATE LinkKategori SET Ad='$post_KategoriAd',Aciklama='$post_Aciklama' ";
  $Sql.= "WHERE No=$get_LinkKategoriNo";
  sorgula($Sql);
}// if ($post_KategoriGuncele<>"")
//////////////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////////////
//SSS Kategorisi bulunacak
if ($get_LinkKategoriNo<>"")
{
 $Sql = "SELECT Ad,Aciklama FROM LinkKategori WHERE No=$get_LinkKategoriNo";
 $Sonuc = sorgula($Sql);
 list($vt_Ad,$vt_Aciklama) = getir($Sonuc);
 $smarty->assign('KategoriAd',$vt_Ad);
 $smarty->assign('Aciklama',$vt_Aciklama);
 $smarty->assign('LinkKategoriNo',$get_LinkKategoriNo);
 $Duzenlenecek = "Kategori";
}
//////////////////////////////////////////////////////////////////////////////////////

$smarty->assign('Duzenlenecek',$Duzenlenecek);
?>
