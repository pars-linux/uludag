<?
//{{{ function SssSoruVarmi($KategoriNo)
function SssSoruVarmi($KategoriNo)
{
  $Sql = "SELECT * FROM SssSorular WHERE KatNo='$KategoriNo'"; 
  $Sonuc = sorgula($Sql);
  if ($Sonuc->numRows()>0)
    return true;
  else
    return false;
}
//}}}
//{{{Sss kategorileri bulal�m
 $Sql = "SELECT No,Ad FROM SssKategori ORDER BY Sira";
 $Sonuc = sorgula($Sql);
 $i = 0;
 while(list($vt_No,$vt_Ad) = getir($Sonuc))
 {
   if (!SssSoruVarmi($vt_No)) continue;
   $KategoriDizi[$i]['No'] = $vt_No;
   $KategoriDizi[$i]['Ad']   = $vt_Ad;
   $i++;
 }
 $smarty->assign('Kategoriler',$KategoriDizi);
//}}} 
//{{{Sss soru ve cevaplar� bulal�m
 $Sql = "SELECT No,KatNo,Soru,Cevap FROM SssSorular";
 if($get_SssNo){
 	$Cevap="1";
  $smarty->assign('Cevap',$Cevap);	
 $Sql.=	" WHERE No='$get_SssNo' ORDER BY Sira";
 }else{
 	$Sql.=	" ORDER BY Sira";
 }
 $Sonuc = sorgula($Sql);
 $i = 0;
 while(list($vt_No,$vt_KatNo,$vt_Soru,$vt_Cevap) = getir($Sonuc))
 {
   $Sorular[$i]['No']    = $vt_No;
   $Sorular[$i]['KatNo'] = $vt_KatNo;
   $Sorular[$i]['Soru']  = stripslashes($vt_Soru);
   $Sorular[$i]['Cevap'] = stripslashes($vt_Cevap);
   $i++;
 }// for
 $smarty->assign('Sorular',$Sorular);
//}}}
?>
