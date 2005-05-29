<?
$INI_OrtakDosyalarDizin = '/var/www/pardul/shared';
include($INI_OrtakDosyalarDizin.'/config.inc.php');
require_once($INI_OrtakDosyalarDizin.'/functions/general.php');
require_once($AnaDizin.'/functions/general.php');
$KutuphaneDizin = $INI_KapsananDizin;
//debug icin
//error_reporting(E_WARNING || E_PARSE);
//error_reporting(E_ALL);

define('SMARTY_DIR',"$INI_KapsananDizin/Smarty/");
require(SMARTY_DIR.'Smarty.class.php');

$smarty=new Smarty;

$smarty->left_delimiter = "{{";  // Tek { kullanmak yerine {{ kullanarak, jscriptler icin <literal> tag'indan 
$smarty->right_delimiter = "}}"; // kurtulmuþ oluyoruz.

$smarty->config_dir		= $AnaDizin."/lisan";
// $smarty->config_dir		= $AnaDizin."/".$Lisan";
$smarty->template_dir	= $INI_TemplateDizin;
$smarty->compile_dir	= $INI_CompileDizin;
// $smarty->compile_id		= "tr";
$smarty->compile_check	= true;
$smarty->caching		= true;
$smarty->cache_dir		= $AnaDizin.'/cached';
$smarty->cache_lifetime	= 0;


$SmartyIletiIcerik=new Smarty;
$SmartyIletiIcerik->left_delimiter = "{{";
$SmartyIletiIcerik->right_delimiter = "}}";
$SmartyIletiIcerik->template_dir = $INI_AdminTemplateDizin."/ileti";
$SmartyIletiIcerik->compile_dir = $INI_AdminCompileDizin;
$SmartyIletiIcerik->compile_check = true;
$SmartyIletiIcerik->caching = false;
$SmartyIletiIcerik->cache_lifetime = 0;
// Translation
require("$INI_KapsananDizin/Smarty/smarty_ttranslate.php");
$smarty->register_block('t', 'smarty_translate');

// }}}
$IcerikResimler = $AnaSayfa.'/templates/resimler/Image';
$IcerikBelge = $AnaSayfa.'/templates/resimler/File';
$WebResimler	= $AnaSayfa.'/templates/resimler/Image/sistem/tasarim';
$SSLWebResimler = $SSLAnaSayfa.'/templates/resimler/Image/sistem/tasarim';
$Banners		= $AnaSayfa.'/templates/resimler/banners';
$SSLBanners		= $SSLAnaSayfa.'/templates/resimler/banners';
$StilAnaSayfa	= $AnaSayfa.'/templates';
$SunumLogolar	= $AnaSayfa.'/templates/resimler/Image/logo/sunumlar';
if($_SERVER['SERVER_PORT']=="443") 
{
  $WebResimler	= $SSLWebResimler;
  $StilAnaSayfa = $SSLAnaSayfa.'/templates';
  $Banners		= $SSLWebResimler;
}

$smarty->assign('WebResimler',$WebResimler);
$smarty->assign('IcerikBelge',$IcerikBelge);
$smarty->assign('IcerikResimler',$IcerikResimler);
$smarty->assign('SunumLogolar',$SunumLogolar);
$smarty->assign('SSLWebResimler',$SSLWebResimler);
$smarty->assign('Banners',$Banners);
$smarty->assign('SSLBanners',$SSLBanners);
$smarty->assign('AnaDizin',$AnaDizin);
$smarty->assign('AnaSayfa',$AnaSayfa);
$smarty->assign('StilAnaSayfa',$StilAnaSayfa);
$smarty->assign('AdminAnaSayfa',$AdminAnaSayfa);
$smarty->assign('AdminAnaDizin',$AdminAnaDizin);

//$HEX 		= array ('#f6c257','#e7edff','#56789e','#e0e5ef','#5c5c5c','#000000','#efeee8','#333333');
$HEX 		= array ('#396bad','#ffffff','#ffffff','#C9D9ED','#ffffff','#ffffff','#ffffff','#ffffff');
$smarty->assign('HEX',$HEX);

$Mail		= array();
	$Mail['bilgi'] 		='bilgi@linux.org.tr';
	$Mail['Uye'] 		='uye@linux.org.tr';
	$Mail['bilgi'] 		='admin@linux.org.tr';
	$Mail['web'] 		='web-cg@linux.org.tr';

$smarty->assign('Mail',$Mail);
//$smarty->load_filter('output','gzip');
?>
