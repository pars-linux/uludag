<?
// {{{ KategoriSil düzenlendi
function KategoriSil($KatNo)
{
    $Sorgu1 = sorgula("SELECT TabloAd FROM UrunKategoriler WHERE No='$KatNo'");
    list($TabloAd) = getir($Sorgu1);
        if (!$TabloAd)
        return 'Gecersiz Kategori';
    // detay tablosu
    sorgula("DROP TABLE `$TabloAd`");
    // kategoriler tablosundaki satir
    sorgula("DELETE FROM UrunKategoriler WHERE No='$KatNo'");
    // Urunler Pasif Yapiliyor ve kategorileri sifirlaniyor
    sorgula("UPDATE Urunler SET KatNo='0',AktifPasif='Pasif' WHERE KatNo='$KatNo'");
    return 'KategoriSilBasarili';
}
// }}}
// {{{ KategoriOlustur  Düzenlendi
function KategoriOlustur($KatAd)
{
    global $WebUrunResimlerDizin;
    if($KatAd=='') return 'GecersizKatAdTabloAd';
    $uyari = "";
    $TabloAd = Turkcesiz(strtolower($KatAd));
    $TabloAd = eregi_replace("[^a-z0-9]","",$TabloAd);
    $TabloAd = "Urunler_".$TabloAd;
    // kontroller
    $sorgu1 = sorgula("SELECT * FROM UrunKategoriler WHERE TabloAd='$TabloAd'");
    if($sorgu1->numRows()!= 0)
        return 'Eklemek istediðiniz tablo mevcut!';
    $sorgu1 = sorgula("SELECT * FROM UrunKategoriler WHERE KatAd='$KatAd'");
    if($sorgu1->numRows()!= 0)
        return 'Eklemek istediðiniz kategori mevcut!';
    // Kategori Tablosundaki satir
    sorgula("INSERT INTO UrunKategoriler SET KatAd='$KatAd',TabloAd='$TabloAd'");
    $Sorgu1 = sorgula("SELECT MAX(No) FROM UrunKategoriler");
    list($KatNo) = getir($Sorgu1);
    // Veritabaninda Tablo
    sorgula("CREATE TABLE $TabloAd (UrunNo INT(11) NOT NULL ,PRIMARY KEY (UrunNo));");
    return 'KategoriEkleBasarili';
}
// }}}
// {{{ KategoriDuzenle  düzenlendi
function KategoriDuzenle($KatAd,$KatNo)
    {
    if($KatAd=='')
        return 'Geçersiz kategori ve tablo adý!';
    $Sorgu1 = sorgula("SELECT TabloAd FROM UrunKategoriler WHERE No='$KatNo'");
    list($TabloEskiAd) = getir($Sorgu1);
        if (!$TabloEskiAd)
        return 'Geçersiz Kategori adý!';
    $uyari = "";
    // kontroller
    $sorgu1 = sorgula("SELECT * FROM UrunKategoriler WHERE KatAd='$KatAd' AND No<>'$KatNo'");
    if($sorgu1->numRows() != 0)
        return 'Kategori mevcut!';
    // Kategori Tablosundaki satir
    sorgula("UPDATE UrunKategoriler SET KatAd='$KatAd' WHERE No='$KatNo'");
    return 'KategoriDuzenleBasarili';
    }
// }}}
// {{{ KategoriGuncelle düzenlendi
function KategoriGuncelle($KatNo,$GorunenIsim,$SonEk,$GirisNot,$FiltreAlanlar,$ListeAlanlar)
    {
    sorgula("UPDATE UrunKategoriler SET GorunenIsim='$GorunenIsim',SonEk='$SonEk',GirisNot='$GirisNot',FiltreAlanlar='$FiltreAlanlar',ListeAlanlar='$ListeAlanlar' WHERE No='$KatNo'");
    return 'BilgiGuncelBasarili';
    }
// }}}
// {{{ AlanEkle düzenlendi
// Bilgilerin eksik gonderilmeyecegini varsayar
function AlanEkle($KatNo,$AlanAd,$AlanBoyut,$AlanTip,$AlanVarsayilan)
    {
    $Sorgu1 = sorgula("SELECT TabloAd,AlanSirasi,GorunenIsim,SonEk,GirisNot FROM UrunKategoriler WHERE No='$KatNo'");
    list($vt_TabloAd,$vt_AlanSirasi,$vt_GorunenIsim,$vt_SonEk,$vt_GirisNot)=getir($Sorgu1);
    $sorgu1 = sorgula("SELECT * FROM $vt_TabloAd");
    $AlanSayisi = $sorgu1->numCols();
    $Alanlar = $sorgu1->TableInfo();
    $AlanMevcut = false;

    for($i=0;$i<$AlanSayisi;$i++)   // ilk alan varsayilan ortak birincil anahtar = no , atlaniyor
        if($Alanlar[$i]['name'] == $AlanAd)
            $AlanMevcut = true;
    if($AlanMevcut)
        return 'Alan adý mevcut!';
    else    {
        if($AlanBoyut!=''){
            $AlanTip.="($AlanBoyut)";
            
        }elseif ($AlanTip=='VARCHAR')
            $AlanTip.="(50)";
        if($AlanVarsayilan)
            $SqlEk = "DEFAULT '$AlanVarsayilan'".$SqlEk;
        if(!sorgula("ALTER TABLE $vt_TabloAd ADD $AlanAd $AlanTip $SqlEk"))
            return "SQL Hatasi!";
        else    // basarili
            {
            // GorunenIsim, SonEk ve GirisNot duzenleniyor
            $GorunenIsim = $vt_GorunenIsim."##";
            $SonEk = $vt_SonEk."##";
            $GirisNot = $vt_GirisNot."##";
            if($vt_AlanSirasi)
                $AlanSirasi = $vt_AlanSirasi.",$AlanAd";
            else    $AlanSirasi = $AlanAd;
            sorgula("UPDATE UrunKategoriler SET GorunenIsim='$GorunenIsim',SonEk='$SonEk',GirisNot='$GirisNot',AlanSirasi='$AlanSirasi' WHERE No='$KatNo'");
            }
        }
    return 'AlanEkleBasarili';
    }
// }}}
// {{{ AlanDuzenle düzenlendi
function AlanDuzenle($AlanEskiAd,$KatNo,$AlanAd,$AlanBoyut,$AlanTip,$AlanVarsayilan)
    {
    $Sorgu1 = sorgula("SELECT TabloAd,AlanSirasi FROM UrunKategoriler WHERE No='$KatNo'");
    list($vt_TabloAd,$vt_AlanSirasi) = getir($Sorgu1);
    $sorgu1 = sorgula("SELECT * FROM $vt_TabloAd");
    $AlanSayisi = $sorgu1->numCols();
    $Alanlar = $sorgu1->tableInfo();
    for($i=1;$i<$AlanSayisi;$i++)
        if($Alanlar[$i]['type'] ==='blob')
            $Alanlar[$i]['type'] =='text';
    // Eski isimdeki alan araniyor
    $AlanMevcut = false;
    for($i=1;$i<$AlanSayisi;$i++)   // ilk alan varsayilan ortak birincil anahtar = no , atlaniyor
        if($Alanlar[$i]['name'] == $AlanEskiAd)
            $AlanMevcut = true;
    if(!$AlanMevcut)
        return 'Alan adi yok';
    // Yeni alan ismi araniyor
    if($AlanEskiAd != $AlanAd)
        {
        $AlanMevcut = false;
    
        for($i=0;$i<$AlanSayisi;$i++)
            if($Alanlar[$i]['name'] == $AlanAd)
                $AlanMevcut = true;
        if($AlanMevcut)
            return 'Alan adi mevcut!';
        }

    if($AlanBoyut!='')
        $AlanTip.="($AlanBoyut)";
    if($AlanVarsayilan)
        $SqlEk = "DEFAULT '$AlanVarsayilan'".$SqlEk;
    if(!sorgula("ALTER TABLE $vt_TabloAd CHANGE `$AlanEskiAd` `$AlanAd` $AlanTip $SqlEk"))
        return 'SQL Hatasi';
    // AlanSirasi alanýndaki isim deðiþtiriliyor...
    $AlanSirasi = eregi_replace("$AlanEskiAd","$AlanAd",$vt_AlanSirasi);
    sorgula("UPDATE UrunKategoriler SET AlanSirasi='$AlanSirasi' WHERE No='$KatNo'");
    return 'AlanDuzenleBasarili';
    }
// }}}
// {{{ AlanSil düzenlendi
function AlanSil($KatNo,$AlanAd)
    {
    $Sorgu1 = sorgula("SELECT TabloAd,AlanSirasi,GorunenIsim,SonEk,GirisNot,FiltreAlanlar,ListeAlanlar FROM UrunKategoriler WHERE No='$KatNo'");
    list($vt_TabloAd,$vt_AlanSirasi,$vt_GorunenIsim,$vt_SonEk,$vt_GirisNot,$vt_FiltreAlanlar,$vt_ListeAlanlar) = getir($Sorgu1);
    // GorunenIsim, SonEk. GirisNot, FiltreAlanlar ve ListeAlanlar duzenleniyor
    $AlanSirasi = explode(",",$vt_AlanSirasi);
    $GorunenIsim = explode("##",$vt_GorunenIsim);
    $SonEk = explode("##",$vt_SonEk);
    $GirisNot = explode("##",$vt_GirisNot);
    $FiltreAlanlar = explode("##",$vt_FiltreAlanlar);
    $ListeAlanlar = explode("##",$vt_ListeAlanlar);

    $SonFiltreAlan = "";
    $SonListeAlan = "";
    if(is_array($FiltreAlanlar) && count($FiltreAlanlar))
        {
        $SonFiltreAlanlar = array();
        foreach($FiltreAlanlar as $FAlan)
            {
            if($FAlan!=$AlanAd)
                $SonFiltreAlanlar[] = $FAlan;
            }
        if(count($SonFiltreAlanlar))
            $SonFiltreAlan = implode("##",$SonFiltreAlanlar);
        }
    if(is_array($ListeAlanlar) && count($ListeAlanlar))
        {
        $SonListeAlanlar = array();
        foreach($ListeAlanlar as $LAlan)
            if($LAlan!=$AlanAd)
                $SonListeAlanlar[] = $LAlan;
        if(count($SonListeAlanlar))
            $SonListeAlan = implode("##",$SonListeAlanlar);
        }

    $Sorgu1 = sorgula("SELECT $vt_AlanSirasi FROM $vt_TabloAd");
    $AlanSayisi = $Sorgu1->numCols();
    $Alanlar = $Sorgu1->tableInfo();
    $SonAlanSirasi = array();
    $SonGorunenIsimler = array(); 
    $SonSonEkler = array(); 
    $SonGirisNotlar = array(); 
    for($i=0;$i<$AlanSayisi;$i++)   // ilk alan UrunNo atliyoruz
        {
        if($Alanlar[$i]['name'] != $AlanAd)
            {
            $SonAlanSirasi[] = $AlanSirasi[$i];
            $SonGorunenIsimler[] = $GorunenIsim[$i];
            $SonSonEkler[] = $SonEk[$i];
            $SonGirisNotlar[] = $GirisNot[$i];
            }
        }
    $SonGorunenIsim = implode("##",$SonGorunenIsimler);
    $SonSonEk = implode("##",$SonSonEkler);
    $SonGirisNotlar = implode("##",$SonGirisNotlar);
    $SonAlanSirasi = implode(",",$SonAlanSirasi);
    sorgula("ALTER TABLE $vt_TabloAd DROP $AlanAd");
    sorgula("UPDATE UrunKategoriler SET AlanSirasi='$SonAlanSirasi',GorunenIsim='$SonGorunenIsim',SonEk='$SonSonEk',GirisNot='$SonGirisNotlar',FiltreAlanlar='$SonFiltreAlan',ListeAlanlar='$SonListeAlan' WHERE No='$KatNo'");
    return 'AlanSilBasarili';
    }
// }}}
?>
