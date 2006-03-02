<?


if ($post_SssKategoriNo<>"")
{
 $get_SssKategoriNo = $post_SssKategoriNo;
}

//////////////////////////////////////////////////////////////////////////////////////
//SSS Kategorisi güncelleniyor
if ($post_KategoriGuncelle<>"")
{
  $Sql = "UPDATE SssKategori SET Ad='$post_KategoriAd',Aciklama='$post_Aciklama' ";
  $Sql.= "WHERE No=$get_SssKategoriNo";
  sorgula($Sql);
}// if ($post_KategoriGuncele<>"")
//////////////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////////////
//SSS Kategorisi bulunacak
if ($get_SssKategoriNo<>"")
{
 $Sql = "SELECT Ad,Aciklama FROM SssKategori WHERE No=$get_SssKategoriNo";
 $Sonuc = sorgula($Sql);
 list($vt_Ad,$vt_Aciklama) = getir($Sonuc);
 $smarty->assign('KategoriAd',$vt_Ad);
 $smarty->assign('Aciklama',$vt_Aciklama);
 $smarty->assign('SssKategoriNo',$get_SssKategoriNo);
 $Duzenlenecek = "Kategori";
}
//////////////////////////////////////////////////////////////////////////////////////

$smarty->assign('Duzenlenecek',$Duzenlenecek);
?>
