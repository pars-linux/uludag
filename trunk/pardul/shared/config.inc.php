<?
// {{{ Anadizin ve Anasayfa

	$AnaDizin = "/var/www/par/pardul";
	$AnaSayfa = "http://192.168.0.200/par/pardul"; //http URI
	$SSLAnaSayfa = "https://192.168.0.200/par/pardul"; //https URI

	$AdminAnaDizin = "/var/www/par/pardul/admin";
	$AdminAnaSayfa = "http://192.168.0.200/par/pardul/admin"; //http URI

// }}}

// {{{ Tanimli Yollar

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
