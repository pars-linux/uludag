<?
require_once("$KutuphaneDizin/Pear/Auth/Auth.php");

$dsn="mysql://$AYAR_VTKullanici:$AYAR_VTSifre@$AYAR_VTAdres/$AYAR_VTIsim";
$guvenlikvt=array();
$guvenlikvt['table']=$AYAR_OturumTablo;
$guvenlikvt['usernamecol']=$AYAR_OturumKullanici;
$guvenlikvt['passwordcol']=$AYAR_OturumSifre;
$guvenlikvt['dsn']=$dsn;

$Oturum=new Auth("DB",$guvenlikvt,"",false);
$Oturum->setSessionname("pardulOturum");
$Oturum->setShowLogin(false);

$Oturum->setIdle(864000,true);	// simdilik 24 saat sonra degiskene baglanacak
$Oturum->setExpire(864000,true);	// simdilik 24 saat sonra degiskene baglanacak
$Oturum->start();
if ($Oturum->getAuth())
{
  $OturumKullaniciAd = $Oturum->getUserName();
  $OturumVar = true;
  $Sql = "SELECT UyelikOnay FROM Kullanicilar WHERE EPosta='$OturumKullaniciAd'";
  $Sonuc = sorgula($Sql);
  list($vt_UyelikOnay) = getir($Sonuc);
  if ($vt_UyelikOnay=='Onaylanmadi') 
  {
     $OturumVar = false;
     $Oturum->logout();
     $OturumMesaj='Giri� yapabilmek i�in EPosta adresinize g�nderilen aktivasyon i�lemini ger�ekle�tirmelisiniz!';
  }
  else 
    $OturumVar=true;
}
else
  $OturumVar = false;

$Simdi = Simdi();
$MisafirIp = getenv('REMOTE_ADDR');

$OzelKod = $_COOKIE['CookieKod'];

if($OturumVar) {
	sorgula("UPDATE Kullanicilar SET SonGiris=$Simdi WHERE EPosta='$OturumKullaniciAd'");
	sorgula("DELETE FROM Anonim WHERE Kod='$OzelKod'");
} else {
	$SqlKod = "SELECT Kod FROM Anonim WHERE Kod='$OzelKod'";
	$SonucKod = sorgula($SqlKod);
	if ($SonucKod->numRows()) {
		sorgula("UPDATE Anonim SET SonGiris=$Simdi WHERE Kod='$OzelKod'");
	} else {
		$OzelKod = Rastgele(14);	
		setcookie('CookieKod',$OzelKod);
		sorgula("INSERT INTO Anonim SET SonGiris=$Simdi,Kod='$OzelKod',Ip='$MisafirIp'");
	}
}
/* 
	Dil Secimi Islemleri Yapiliyor. Buradan Alinan Degisken Degerleri,
	index.php dosyasindan smarty'e gonderiliyor.
*/

$OturumDurum = $Oturum->getStatus();
if($OturumDurum==AUTH_WRONG_LOGIN)
  $OturumMesaj = 'Hatal� Kullan�c� veya �ifre!';
elseif($OturumDurum==AUTH_EXPIRED)
  $OturumMesaj = 'Oturum sona erdi!';
?>
