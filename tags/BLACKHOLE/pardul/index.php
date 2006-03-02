<?
include("config.inc.php");
require_once($INI_OrtakDosyalarDizin.'/functions/mail.php');
// error_reporting(E_ALL);
// {{{ SAYFA DEÐÝÞKENÝ AYARLANIYOR
if (isset($_COOKIE['pardulLang']))
 {
	$Lisan = $_COOKIE['pardulLang'];
 } 
 if ($_GET['Lisan']) {
  	$Lisan = $_GET['Lisan'];
	setcookie('pardulLang',$Lisan, time()+3600000); // 100 Saat icin dil ayarlandi
 } 
 if (!isset($_COOKIE['pardulLang'])&&!$_GET['Lisan']) {	// Kullanici istedigi an degistirebilir...
	$Lisan = "tr";		// Varsayilan Dil tr
	setcookie('pardulLang',$Lisan, time()+3600000);
 }
$smarty->assign('Lisan',$Lisan);
if($_GET['Page'])
        {
        $Page = $_GET['Page'];
        if(file_exists("$INI_TemplateDizin/$Page.tpl"))
                $Page = $_GET['Page'];
		else	$Page = 'Anasayfa';
        }
else
        $Page = 'Anasayfa';
if(!$Page)
        $Page = 'Anasayfa';

$Burasi = $AnaSayfa."/index.php?Page=$Page";
$smarty->assign('Burasi',$Burasi);

$SSayfa = $AnaSayfa.'/index.php?Page=';
$smarty->assign('SSayfa',$SSayfa);

$SSLSayfa = $SSLAnaSayfa.'/index.php?Page=';
$smarty->assign('SSLSayfa',$SSLSayfa);

include("$INI_KapsananDizin/db.inc.php");
include("$INI_KapsananDizin/auth.php");
ob_start();
include("$INI_KapsananDizin/class.gzip_encode.php");

//{{{ Kullanicý giriþi ile ilgili
//güvenlik.php dosyasýndan gelen deðiþkenler baþladý
$smarty->assign('OturumVar',$OturumVar);
$smarty->assign('OturumKullaniciAd',$OturumKullaniciAd);

//güvenlik.php dosyasýndan gelen deðiþkenler bitti
if ($OturumKullaniciAd) {
	$SqlGiris = "SELECT No,AdSoyad FROM Kullanicilar WHERE EPosta='$OturumKullaniciAd'";
	$SonucGiris = sorgula($SqlGiris);
	list($vt_No,$vt_AdSoyad) = getir($SonucGiris);
	$smarty->assign('OturumAdSoyad',$vt_AdSoyad);
	$smarty->assign('OturumKullaniciNo',$vt_No);
}
$smarty->assign('OturumMesaj',$OturumMesaj);

$OturumBilgiler = array();
$OturumBilgiler['OturumVar']			= $OturumVar;
$OturumBilgiler['OturumKullaniciAd']	= $OturumKullaniciAd;
$OturumBilgiler['OturumAdSoyad']		= $vt_AdSoyad;
$OturumBilgiler['OturumKullaniciNo']	= $vt_No;
$OturumBilgiler['OturumMesaj']			= $OturumMesaj;

$smarty->assign('OturumBilgiler',$OturumBilgiler);

$Sorgu1 = sorgula("SELECT Isim,Deger FROM Degiskenler");
while(list($vt_Isim,$vt_Deger) = $Sorgu1->fetchRow()) {
	$GLOBALS['sistem_'.$vt_Isim] = stripslashes($vt_Deger);
	$smarty->assign('sistem_'.$vt_Isim,stripslashes($vt_Deger));
}

foreach($HTTP_POST_VARS as $varname => $value)
	{
	$HTTP_POST_VARS[$varname]=trim(addslashes($value));
	$Asilvarname = eregi_replace("S_",'',eregi_replace("I_",'',eregi_replace("N_",'',$varname)));
	${"post_".$Asilvarname} = $HTTP_POST_VARS[$varname];
	}
foreach($HTTP_GET_VARS as $varname => $value)
	{
	$HTTP_GET_VARS[$varname]=trim(addslashes($value));
	${"get_".$varname} = $HTTP_GET_VARS[$varname];
	}

if(file_exists($INI_TemplateDizin.'/Stil.tpl'))
	$icerik = $smarty->fetch($INI_TemplateDizin.'/Stil.tpl');
$Sql = "SELECT BolumIsim,Satir,Sutun FROM KullaniciSayfalar WHERE SayfaIsim='$Page' ORDER BY Sutun,Satir";
$index_sonuc = $vt->query($Sql);
if($index_sonuc->numRows()==0)
	{
	if(file_exists($INI_IslemlerDizin.'/'.$Page.'.php'))
		{
		ignore_user_abort(true);
		include($INI_IslemlerDizin.'/'.$Page.'.php');
		ignore_user_abort(false);
		}
	if(file_exists($INI_TemplateDizin.'/'.$Page.'.tpl'))
		$icerik.= $smarty->fetch($INI_TemplateDizin.'/'.$Page.'.tpl');
	echo $icerik;
	}
else	{
	$SAYFA_TEMEL_SOL_SUTUN = "";
	$SAYFA_TEMEL_ORTA_SUTUN = "";
	$SAYFA_TEMEL_DIGER_SUTUNLAR = array();
	while($IndexSatir = $index_sonuc->fetchRow(DB_FETCHMODE_ASSOC))
		{
		// {{{ islem dosyasi
		if(file_exists($INI_IslemlerDizin.'/'.$IndexSatir['BolumIsim'].'.php'))
                {
			ignore_user_abort(true);
			include($INI_IslemlerDizin.'/'.$IndexSatir['BolumIsim'].'.php');
			ignore_user_abort(false);
                }

		if(file_exists($INI_TemplateDizin.'/'.$IndexSatir['BolumIsim'].'.tpl'))
			{
			if($IndexSatir['Sutun'] == 1)
				$SAYFA_TEMEL_SOL_SUTUN.=$smarty->fetch($INI_TemplateDizin.'/'.$IndexSatir['BolumIsim'].'.tpl');
			else if($IndexSatir['Sutun'] == 2)
				$SAYFA_TEMEL_ORTA_SUTUN.=$smarty->fetch($INI_TemplateDizin.'/'.$IndexSatir['BolumIsim'].'.tpl');
			else	$SAYFA_TEMEL_DIGER_SUTUNLAR[$IndexSatir['Sutun']-2].=$smarty->fetch($INI_TemplateDizin.'/'.$IndexSatir['BolumIsim'].'.tpl');
			}

		}
	$smarty->assign('SAYFA_TEMEL_DIGER_SUTUN_SAYI',count($SAYFA_TEMEL_DIGER_SUTUNLAR));
	if(file_exists($INI_IslemlerDizin.'/Header.php'))
		{
		ignore_user_abort(true);
		include($INI_IslemlerDizin.'/Header.php');
		ignore_user_abort(false);
		}
	if(file_exists($INI_TemplateDizin."/Header.tpl"))
		$SAYFA_TEMEL_UST_BOLUM = $smarty->fetch($INI_TemplateDizin."/Header.tpl");
	if(file_exists($INI_TemplateDizin."/Footer.tpl"))
		$SAYFA_TEMEL_ALT_BOLUM = $smarty->fetch($INI_TemplateDizin."/Footer.tpl");
	$smarty->assign('SAYFA_TEMEL_UST_BOLUM',$SAYFA_TEMEL_UST_BOLUM);
	$smarty->assign('SAYFA_TEMEL_ALT_BOLUM',$SAYFA_TEMEL_ALT_BOLUM);
	$smarty->assign('SAYFA_TEMEL_SOL_SUTUN',$SAYFA_TEMEL_SOL_SUTUN);
	$smarty->assign('SAYFA_TEMEL_ORTA_SUTUN',$SAYFA_TEMEL_ORTA_SUTUN);
	$smarty->assign('SAYFA_TEMEL_DIGER_SUTUNLAR',$SAYFA_TEMEL_DIGER_SUTUNLAR);
	$smarty->display('AnasayfaTemel.tpl');
	}

new gzip_encode();
?>
