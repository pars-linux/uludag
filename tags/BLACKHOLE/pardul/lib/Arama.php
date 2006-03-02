<?
if($post_Haberler)
{
    $Sql = "SELECT No,Baslik,Icerik,HaberSlogan,Kaynak,Durum,Tarih FROM IcerikHaber  WHERE 1=1 AND Durum='Aktif'";
    $Sql.= " AND (Baslik LIKE '%$post_Anahtar%' OR Icerik LIKE '%$post_Anahtar%' OR HaberSlogan LIKE '%$post_Anahtar%')";
    $Sonuc = sorgula($Sql);
    $numrows=$Sonuc->numRows();
    $smarty->assign('Sayi',$numrows);
    $Bulunamadi="1";
    $smarty->assign('Bulunamadi',$Bulunamadi);
    $smarty->assign('Anahtar',$post_Anahtar);
    $i = 0;
    while(list($vt_No,$vt_Baslik,$vt_Icerik,$vt_HaberSlogan,$vt_Kaynak,$vt_Durum,$vt_Tarih) = getir($Sonuc))
       {
        $TumHaberler[$i]['No']		= $vt_No;
        $TumHaberler[$i]['Baslik']		= $vt_Baslik;
        $TumHaberler[$i]['Icerik']		= $vt_Icerik;
        $TumHaberler[$i]['HaberSlogan']     = $vt_HaberSlogan;
        $TumHaberler[$i]['Kaynak']		= $vt_Kaynak;
        $TumHaberler[$i]['Durum']		= $vt_Durum;
        list($y,$a,$g) = explode("-",$vt_Tarih);
        $TumHaberler[$i]['Tarih']		= $g.".".$a.".".$y;
        $i++;
       }
    $HaberSayi = count($TumHaberler);
    $smarty->assign('HaberSayi',$HaberSayi);
    $smarty->assign('TumHaberler',$TumHaberler);
}
?>
