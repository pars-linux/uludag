<?
$INI_OrtakDosyalarDizin = '/var/www/pardul.uludag.org.tr/htdocs/shared';
include($INI_OrtakDosyalarDizin.'/config.inc.php');
require_once($INI_OrtakDosyalarDizin.'/functions/general.php');
require_once($INI_OrtakDosyalarDizin.'/functions/class.jabber.php');
require_once($AnaDizin.'/functions/general.php');
$KutuphaneDizin = $INI_KapsananDizin;
//debug icin
//error_reporting(E_WARNING || E_PARSE);
//error_reporting(E_ALL);

define('SMARTY_DIR',"$INI_KapsananDizin/Smarty/");
require(SMARTY_DIR.'Smarty.class.php');

$smarty=new Smarty;

$smarty->left_delimiter = "{{";  // Tek { kullanmak yerine {{ kullanarak,  
$smarty->right_delimiter = "}}"; //jscriptlerde <literal> tag'indan gerekmiyor

$smarty->template_dir	= $INI_TemplateDizin;
$smarty->compile_dir	= $INI_CompileDizin;
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

$WebResimler	= $AnaSayfa.'/templates/images';
$SSLWebResimler = $SSLAnaSayfa.'/templates/images';
$Banners		= $AnaSayfa.'/templates/banners';
$SSLBanners		= $SSLAnaSayfa.'/templates/banners';
$StilAnaSayfa	= $AnaSayfa.'/templates';

if($_SERVER['SERVER_PORT']=="443") 
{
  $WebResimler	= $SSLWebResimler;
  $StilAnaSayfa = $SSLAnaSayfa.'/templates';
  $Banners		= $SSLWebResimler;
}

$smarty->assign('WebResimler',$WebResimler);
$smarty->assign('SSLWebResimler',$SSLWebResimler);
$smarty->assign('Banners',$Banners);
$smarty->assign('SSLBanners',$SSLBanners);
$smarty->assign('AnaDizin',$AnaDizin);
$smarty->assign('AnaSayfa',$AnaSayfa);
$smarty->assign('StilAnaSayfa',$StilAnaSayfa);
$smarty->assign('AdminAnaSayfa',$AdminAnaSayfa);
$smarty->assign('AdminAnaDizin',$AdminAnaDizin);

$Mail		= array();
	$Mail['bilgi'] 		='pardul-info@uludag.org.tr';
	$Mail['Uye'] 		='pardul-uye@uludag.org.tr';
	$Mail['bilgi'] 		='pardul-admin@uludag.org.tr';
	$Mail['web'] 		='pardul-web@uludag.org.tr';

$smarty->assign('Mail',$Mail);
//$smarty->load_filter('output','gzip');
?>
