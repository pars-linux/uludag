<?
//debug icin
//error_reporting(E_ALL);
$INI_OrtakDosyalarDizin = '/var/www/pardul.uludag.org.tr/htdocs/shared';
require_once($INI_OrtakDosyalarDizin.'/config.inc.php');
require_once($INI_OrtakDosyalarDizin.'/functions/general.php');
$KutuphaneDizin = $INI_KapsananDizin;
require_once($AdminAnaDizin.'/functions/general.php');
require_once($AdminAnaDizin.'/functions/hardware.php');
require_once($INI_OrtakDosyalarDizin.'/functions/mail.php');

define('SMARTY_DIR',"$INI_KapsananDizin/Smarty/");
require(SMARTY_DIR.'Smarty.class.php');

$smarty=new Smarty;

$smarty->left_delimiter = "{{";
$smarty->right_delimiter = "}}";

$smarty->template_dir = $INI_AdminTemplateDizin;
$smarty->compile_dir = $INI_AdminCompileDizin;
$smarty->compile_check = true;
$smarty->caching = false;
$smarty->cache_lifetime = 0;

$SmartyIletiIcerik = new Smarty;
$SmartyIletiIcerik->left_delimiter = "{{";
$SmartyIletiIcerik->right_delimiter = "}}";
$SmartyIletiIcerik->template_dir = $INI_AdminTemplateDizin.'/mail';
$SmartyIletiIcerik->compile_dir = $INI_AdminCompileDizin;

$WebResimler		= $AnaSayfa.'/templates/images';
$WebResimlerDizin	= $AnaDizin.'/templates/images';
$WebAdminResimler   = $AdminAnaSayfa.'/images';
$ASSayfa            = $AdminAnaSayfa.'/index.php?Page=';

$smarty->assign('WebUrunResimler',$WebUrunResimler);
$smarty->assign('WebUrunResimlerDizin',$WebUrunResimlerDizin);
$smarty->assign('WebNesneler',$WebNesneler);
$smarty->assign('WebNesnelerDizin',$WebNesnelerDizin);
$smarty->assign('WebAdminResimler',$WebAdminResimler);
$smarty->assign('AnaDizin',$AnaDizin);
$smarty->assign('AnaSayfa',$AnaSayfa);
$smarty->assign('AdminAnaSayfa',$AdminAnaSayfa);
$smarty->assign('AdminAnaDizin',$AdminAnaDizin);
?>
