<?
require("$AdminAnaDizin/jscript/fckeditor.php");
require_once("$KutuphaneDizin/Pear/HTTP/Upload.php");
$INI_KitaplarDizin  = $AnaDizin.'/templates/resimler/kitaplar';
$ResimlerYol = $AnaSayfa.'/templates/resimler/kitaplar';
//{{{ Yeni Haber Ekleme
$BugunTarihi=date('d.m.Y');
	$smarty->assign('BugunTarihi',$BugunTarihi);
if ($post_Gonder<>""&&YetkiKontrol('YeniHaberGiris'))
{
		
	list($g,$a,$y)=explode(".",$post_Tarih);
    $Tarih=$y."-".$a."-".$g;
       $Sql = "INSERT INTO IcerikHaber SET
       Baslik		='$post_Baslik',
       Icerik		='$post_Icerik',
	   Resim		='$post_Resim' ,
	   Tarih		='$Tarih'";
       sorgula($Sql);
       $Uyari="Kayýt Ýþlemi Baþarý ile Tamamlanmýþtýr!!! ";
$smarty->assign('Uyari',$Uyari);
}

//}}}

?>
