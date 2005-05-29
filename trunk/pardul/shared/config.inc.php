<?
// {{{ Anadizin ve Anasayfa

	$AnaDizin = "/var/www/pardul";
	$AnaSayfa = "http://192.168.0.200/pardul";
	$SSLAnaSayfa = "https://192.168.0.200/pardul";

	$AdminAnaDizin = "/var/www/pardul/admin";
	$AdminAnaSayfa = "http://192.168.0.200/pardul/admin";

// }}}

// {{{ Tanimli Yollar

	$INI_KapsananDizin      = $AnaDizin.'/kapsanan';
	$INI_TemplateDizin      = $AnaDizin.'/templates';
	$INI_CompileDizin       = $AnaDizin.'/templates_c';
	$INI_IslemlerDizin      = $AnaDizin.'/islemler';
	$INI_ResimlerDizin      = $AnaDizin.'/templates/resimler/Image/sistem/tasarim';

	$INI_AdminKapsananDizin = $AdminAnaDizin.'/kapsanan';
	$INI_AdminTemplateDizin = $AdminAnaDizin.'/templates';
	$INI_AdminCompileDizin  = $AdminAnaDizin.'/templates_c';
	$INI_AdminIslemlerDizin = $AdminAnaDizin.'/islemler';

// }}}

// {{{ Veritabaný

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
