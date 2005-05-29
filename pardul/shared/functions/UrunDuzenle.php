<?
// Resim Uzerine yazilacak yazinin resim dosyasi
$ImzaResim = $WebUrunResimlerDizin.'/'.$sistem_ResimImzaIsim;
function ResimDuzenle($ResimYol,$GenislikSinirli = false,$ResimImzala = false)
	{
	global $sistem_ResimEnFazlaEn,$sistem_ResimKucukEn,$sistem_ResimKucukBoy,$ImzaResim,$sistem_ResimImzaYazi,$sistem_ResimOrtaEn,$sistem_ResimOrtaBoy;
	global $WebUrunResimlerDizin;

	$ResimBoyutlar = getimagesize($ResimYol);
	$ResimEn = $ResimBoyutlar[0];
	$ResimBoy = $ResimBoyutlar[1];

	// Resmin boyutu belirlenen sinirlara cekiliyor
	if(($ResimEn > $sistem_ResimEnFazlaEn) && $GenislikSinirli)
		{
		$YeniResimBoy = (int)($sistem_ResimEnFazlaEn*$ResimBoy/$ResimEn);
		shell_exec("convert -geometry ".$sistem_ResimEnFazlaEn."x".$YeniResimBoy."! \"".$ResimYol."\" \"".$ResimYol."\"");
		chmod($ResimYol,0777);
		$ResimEn = $sistem_ResimEnFazlaEn;
		$ResimBoy = $YeniResimBoy;
		}
	// Resmin orta boy kopyasi olusturuluyor
	$OrtaResimYol = substr($ResimYol,0,strrpos("$ResimYol","/"))."/o".substr(strrchr("$ResimYol","/"),1);
	shell_exec("convert -geometry ".$sistem_ResimOrtaEn."x".$sistem_ResimOrtaBoy." \"".$ResimYol."\" \"".$OrtaResimYol."\"");
	chmod($OrtaResimYol,0777);
	
	// Resmin kucuk kopyasi olusturuluyor
	$KucukResimYol = substr($ResimYol,0,strrpos("$ResimYol","/"))."/k".substr(strrchr("$ResimYol","/"),1);
	$Komut =  "convert -geometry ".$sistem_ResimKucukEn."x".$sistem_ResimKucukBoy." \"".$ResimYol."\" \"".$KucukResimYol."\"";
	shell_exec($Komut);
	chmod($KucukResimYol,0777);
	
	// Resimler uzerine yazi yaziliyor
	$KucukResimBoyutlar = getimagesize($KucukResimYol);
	$KucukResimEn = $KucukResimBoyutlar[0];
	$KucukResimBoy = $KucukResimBoyutlar[1];

	$OrtaResimBoyutlar = getimagesize($OrtaResimYol);
	$OrtaResimEn = $OrtaResimBoyutlar[0];
	$OrtaResimBoy = $OrtaResimBoyutlar[1];

	chdir($WebUrunResimlerDizin);

	// Buyuk resme yaziliyor
	$ImzaResimEn = $ResimEn/1;
	$ImzaResimBoy = $ImzaResimEn/1;
	$ImzaSolBosluk = ($ResimEn-$ImzaResimEn)/2;
	$ImzaUstBosluk = ($ResimBoy-$ImzaResimBoy)-1;
	if($ResimImzala)
		shell_exec("convert -draw 'image Over $ImzaSolBosluk,$ImzaUstBosluk $ImzaResimEn,$ImzaResimBoy \"$ImzaResim\"' \"$ResimYol\" \"$ResimYol\"");

	// Orta boy resme yaziliyor
	$ImzaResimEn = $OrtaResimEn/1;
	$ImzaResimBoy = $ImzaResimEn/2;
	$ImzaSolBosluk = ($OrtaResimEn-$ImzaResimEn)/2;
	$ImzaUstBosluk = ($OrtaResimBoy-$ImzaResimBoy)-1;
	if($ResimImzala)
		shell_exec("convert -draw 'image Over $ImzaSolBosluk,$ImzaUstBosluk $ImzaResimEn,$ImzaResimBoy \"$ImzaResim\"' \"$OrtaResimYol\" \"$OrtaResimYol\"");

	// Kucuk resme yaziliyor
	
	$ImzaResimEn = $KucukResimEn/1;
	$ImzaResimBoy = $ImzaResimEn/2;
	$ImzaSolBosluk = ($KucukResimEn-$ImzaResimEn)/2;
	$ImzaUstBosluk = ($KucukResimBoy-$ImzaResimBoy)-1;
	if($ResimImzala)
		shell_exec("convert -draw 'image Over $ImzaSolBosluk,$ImzaUstBosluk $ImzaResimEn,$ImzaResimBoy \"$ImzaResim\"' \"$KucukResimYol\" \"$KucukResimYol\"");
	
	
	// Resimlere imza yaziliyor
	shell_exec("convert -comment \"%c $sistem_ResimImzaYazi\" \"$ResimYol\" \"$ResimYol\"");
	shell_exec("convert -comment \"%c $sistem_ResimImzaYazi\" \"$KucukResimYol\" \"$KucukResimYol\"");
	}
?>
