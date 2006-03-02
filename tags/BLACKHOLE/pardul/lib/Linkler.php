<?
//{{{ function SssSoruVarmi($KategoriNo)
function  LinklerVarmi($KategoriNo)
{
  $Sql = "SELECT * FROM  Linkler WHERE KatNo='$KategoriNo'"; 
  $Sonuc = sorgula($Sql);
  if ($Sonuc->numRows()>0)
    return true;
  else
    return false;
}
//}}}
//{{{Sss kategorileri bulalým
 $Sql = "SELECT No,Ad FROM LinkKategori ORDER BY Sira";
 $Sonuc = sorgula($Sql);
 $numrows=$Sonuc->numRows();
 $smarty->assign('TumHaberSayi',$numrows);
 $i = 0;
 while(list($vt_No,$vt_Ad) = getir($Sonuc))
 {
   if (!LinklerVarmi($vt_No)) continue;
   $KategoriDizi[$i]['No'] = $vt_No;
   $KategoriDizi[$i]['Ad']   = $vt_Ad;
   $i++;
 }

//}}} 
//{{{Sss soru ve cevaplarý bulalým
 $Sql = "SELECT No,KatNo,Link,Aciklama FROM Linkler ORDER BY Sira LIMIT 0,$sistem_LinkSayi";
 $Sonuc = sorgula($Sql);
 $Sql1 = "SELECT DISTINCT(KatNo) FROM Linkler ORDER BY Sira";
 $Sonuc1 = sorgula($Sql1);
 $numrows=$Sonuc1->numRows();
 $smarty->assign('TumHaberSayi',$numrows);
 $i = 0;
 while(list($vt_No,$vt_KatNo,$vt_Link,$vt_Aciklama) = getir($Sonuc))
 {
   $Linkler[$i]['No']    = $vt_No;
   $Linkler[$i]['KatNo'] = $vt_KatNo;
   $Linkler[$i]['Aciklama'] = $vt_Aciklama;
   $Linkler[$i]['Link']  = stripslashes($vt_Link);
   
   $i++;
 }// for
 
 $smarty->assign('Linkler',$Linkler);
  $smarty->assign('Kategoriler',$KategoriDizi);
//}}}
?>
