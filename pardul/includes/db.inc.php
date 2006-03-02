<?php
require_once("$KutuphaneDizin/Pear/DB.php");
$DSN="mysql://$AYAR_VTKullanici:$AYAR_VTSifre@$AYAR_VTAdres/$AYAR_VTIsim";
$vt=DB::connect($DSN);
if(DB::isError($vt))
	die('DB Conncetion error!');
?>
