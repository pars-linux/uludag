<?
 if ($post_Sayfa)
 {
   $Sql = "SELECT * FROM Yardim WHERE Sayfa='$post_Sayfa'";
   $Sonuc = sorgula($Sql);
   if($Sonuc->numRows()==0)
   {
    $YeniMetin = addslashes($YeniMetin);
    $Sql = "INSERT INTO Yardim SET Sayfa='$post_Sayfa',Metin='$YeniMetin'";
    sorgula($Sql);
   } 
   else
   { 
	 $YeniMetin = addslashes($YeniMetin);
     $Sql = "UPDATE Yardim SET Metin='$YeniMetin' WHERE Sayfa='$post_Sayfa'";   
     sorgula($Sql);
   }
 }
 if ($get_Sayfa) $Sayfa = $get_Sayfa;else $Sayfa = $post_Sayfa;
 $YardimVar = true;
 $Sql = "SELECT Metin FROM Yardim WHERE Sayfa='$Sayfa'";
 $Sonuc = sorgula($Sql);
 list($vt_Metin) = getir($Sonuc);
 $YazilacakMetin = nl2br(stripslashes($vt_Metin));
 $Metin = stripslashes($vt_Metin);
 if ($Metin=="") $YardimVar = false;
 
 $Sql = "SELECT Isim FROM YonetimMenu WHERE Adres='$Sayfa'";
 $Sonuc = sorgula($Sql);
 list($vt_Isim) = getir($Sonuc);
 $SayfaAdi = $vt_Isim;
 $smarty->assign('Metin',$Metin);
 $smarty->assign('YazilacakMetin',$YazilacakMetin);
 $smarty->assign('SayfaAdi',$SayfaAdi);
 $smarty->assign('Sayfa',$Sayfa);
 $smarty->assign('YardimVar',$YardimVar);
?>
