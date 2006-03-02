<?
if ($post_Ekle)
{
 $SqlKontrol = "SELECT * FROM Degiskenler WHERE Isim='$post_Isim'";
 $SonucKontrol = sorgula($SqlKontrol);
 if (!$SonucKontrol->numRows()>0)
 {
   if ($post_YeniKategori<>'') $Kategori = $post_YeniKategori; else $Kategori = $post_Kategori;
   $Sql = "INSERT INTO Degiskenler SET Isim='$post_Isim',Kategori='$Kategori',Deger='$post_Deger',Aciklama='$post_Aciklama',Degerler='$post_Degerler',Durum='$post_Durum'";
   sorgula($Sql);
 }
 else 
  $smarty->assign('Uyari','Ayný isme sahip bir sistem deðiþkeni mevcut !');
}


$Sql = "SELECT No,Isim,Kategori,Deger,Aciklama,Degerler,Durum FROM Degiskenler ORDER BY Kategori";
$Sonuc = sorgula($Sql);
$i = 0;
while(list($No,$Isim,$Kategori,$Deger,$Aciklama,$Degerler,$Durum)=getir($Sonuc))
{
 $Degiskenler[$i]['No'] = $No;
 $Degiskenler[$i]['Isim'] = $Isim;
 $Degiskenler[$i]['Kategori'] = $Kategori;
 $Degiskenler[$i]['Deger'] = $Deger;
 $Degiskenler[$i]['Aciklama'] = $Aciklama;
 $Degiskenler[$i]['Degerler'] = $Degerler;
 $Degiskenler[$i]['Durum'] = $Durum;
 $i++;
}
$smarty->assign('Degiskenler',$Degiskenler);

$Sql = "SELECT DISTINCT(Kategori) FROM Degiskenler ORDER BY Kategori";
$Sonuc = sorgula($Sql);
$i = 0 ;
while(list($Kategori)=getir($Sonuc)) $Kategoriler[$Kategori] = $Kategori;
$smarty->assign('Kategoriler',$Kategoriler);



?>
