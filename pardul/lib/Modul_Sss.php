<?
$SoruSayi = $sistem_SssModulSoruSayi;
$Sql = "SELECT No,Soru FROM SssSorular ORDER BY RAND() LIMIT $SoruSayi";
$Sonuc = sorgula($Sql);
$i = 0;
while(list($No,$Soru)=getir($Sonuc))
{
  $Sorular[$i]['No']   = $No;
  $Sorular[$i]['Soru'] = $Soru;
  $i++;
}
$smarty->assign('Sorular',$Sorular);
?>
