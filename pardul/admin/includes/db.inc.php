<?
require_once("$KutuphaneDizin/Pear/DB.php");

$DSN="mysql://$AYAR_AdminVTKullanici:$AYAR_AdminVTSifre@$AYAR_AdminVTAdres/$AYAR_AdminVTIsim";
$vt=DB::connect($DSN);

if(DB::isError($vt))
	die('Veritabaný baðlantý hatasý');
?>
