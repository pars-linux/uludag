<?
require_once("$KutuphaneDizin/Pear/Auth/Auth.php");

function GirisFormu($username)
{
       global $anasayfa,$anadizin;
       global $Oturum;
       global $smarty,$SolMenudenGeldi;
       $Durum = $Oturum->getStatus();
       if ($username)
       { 
        if (!empty($Durum) && $Durum == AUTH_EXPIRED)
                $UyariIleti = 'OturumBitti';
        else if (!empty($Durum) && $Durum == AUTH_IDLED)
                $UyariIleti = 'OturumBekledi';
        else if (!empty ($Durum) && $Durum == AUTH_WRONG_LOGIN)
                $UyariIleti = 'OturumHataliGiris';
       } 
       $smarty->assign('UyariIleti',$UyariIleti);
       if (!$SolMenudenGeldi)
       $smarty->display('GirisFormu.tpl');
}

$dsn="mysql://$AYAR_AdminVTKullanici:$AYAR_AdminVTSifre@$AYAR_AdminVTAdres/$AYAR_AdminVTIsim";
$guvenlikvt=array();
$guvenlikvt['table']=$AYAR_AdminOturumTablo;
$guvenlikvt['usernamecol']=$AYAR_AdminOturumKullanici;
$guvenlikvt['passwordcol']=$AYAR_AdminOturumSifre;
$guvenlikvt['dsn']=$dsn;

$Oturum=new Auth("DB",$guvenlikvt,"GirisFormu",false);
$Oturum->setSessionname("B2CAdminOturum");
$Oturum->setShowLogin(true);

$Oturum->setIdle(864000);	// simdilik 24 saat sonra degiskene baglanacak
$Oturum->setExpire(864000);	// simdilik 24 saat sonra degiskene baglanacak
$Oturum->start();
$OturumKullaniciAd = $Oturum->getUserName();
if ($Oturum->getAuth())
{
  $Sql = "SELECT Durum FROM Yoneticiler WHERE KullaniciAd='$OturumKullaniciAd'";
  $Sonuc = sorgula($Sql);
  list($Durum) = getir($Sonuc);
  if ($Durum=='Pasif')
  {
    echo "<center><br><br><b>Hesabýnýz pasif konumda olduðundan giriþ yapamazsýnýz.";
    exit();
  }
  else
  {
    $Sql = "SELECT * FROM Yoneticiler WHERE KullaniciAd='$OturumKullaniciAd'";
    $Sonuc = sorgula($Sql);
    $OturumBilgiler = getir($Sonuc,DB_FETCHMODE_ASSOC); 
  }
}

if(!$Oturum->getAuth())
	exit();
?>
