<?
	if ($get_Sil) {
		$No = $get_Sil;
		sorgula("DELETE FROM Yorum WHERE No='$No'");
	}
	if ($get_Onayla) {
		$No = $get_Onayla;
		sorgula("UPDATE Yorum SET Durum='Onaylandi' WHERE No='$No'");
	}


	$HaberYorumlar = HaberYorumlar();
	$YorumSayi    = count($HaberYorumlar);
    $smarty->assign('UyeYorumSayi',$YorumSayi);	
    $smarty->assign('Yorumlar',$HaberYorumlar);

?>
