<?
	include ("domain.inc.php");

	$AnaDizin = "/var/www/pardul.uludag.org.tr/htdocs";
	$AnaSayfa = "http://$domain"; //http URI
	$SSLAnaSayfa = "https://$domain"; //https URI

	$AdminAnaDizin = "/var/www/pardul.uludag.org.tr/htdocs/admin";
	$AdminAnaSayfa = "http://$domain/admin"; //http URI

// }}}

// {{{ Tanimli Yollar

    $INI_OrtakDosyalarDizin = $AnaDizin.'/shared';
	$INI_KapsananDizin      = $AnaDizin.'/includes';
	$INI_TemplateDizin      = $AnaDizin.'/templates';
	$INI_CompileDizin       = $AnaDizin.'/templates_c';
	$INI_IslemlerDizin      = $AnaDizin.'/lib';
	$INI_ResimlerDizin      = $AnaDizin.'/images';

	$INI_AdminKapsananDizin = $AdminAnaDizin.'/includes';
	$INI_AdminTemplateDizin = $AdminAnaDizin.'/templates';
	$INI_AdminCompileDizin  = $AdminAnaDizin.'/templates_c';
	$INI_AdminIslemlerDizin = $AdminAnaDizin.'/lib';

// }}}

// {{{ Veritaban

	$AYAR_VTKullanici = 'pardul';
	$AYAR_VTSifre     = 'a2l3islkjss3lih';
	$AYAR_VTIsim      = 'pardul';
	$AYAR_VTAdres     = 'localhost';

	$AYAR_AdminVTKullanici = 'pardul';
	$AYAR_AdminVTSifre     = 'a2l3islkjss3lih';
	$AYAR_AdminVTIsim      = 'pardul';
	$AYAR_AdminVTAdres     = 'localhost';


// }}}

// {{{ Oturum

	$AYAR_OturumTablo = 'Kullanicilar';
	$AYAR_OturumKullanici = 'EPosta';
	$AYAR_OturumSifre = 'Sifre';

	$AYAR_AdminOturumTablo = 'Yoneticiler';
	$AYAR_AdminOturumKullanici = 'KullaniciAd';
	$AYAR_AdminOturumSifre = 'Sifre';

// }}}
?>
