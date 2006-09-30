package net.zemberek.demo;

import net.zemberek.araclar.turkce.YaziBirimi;
import net.zemberek.araclar.turkce.YaziBirimiTipi;
import net.zemberek.araclar.turkce.YaziIsleyici;
import net.zemberek.erisim.Zemberek;
import net.zemberek.islemler.IslemTipi;
import net.zemberek.islemler.TurkceYaziTesti;
import net.zemberek.yapi.Kelime;
import net.zemberek.yapi.DilBilgisi;
import net.zemberek.yapi.TurkDiliTuru;
import net.zemberek.tr.yapi.TurkiyeTurkcesi;
import net.zemberek.tm.yapi.Turkmence;

import java.util.*;

/**
 */
public class DemoYonetici {

    private Zemberek zemberek;
    private DilBilgisi dilBilgisi;
    private Map<TurkDiliTuru, Zemberek> zemberekler = new HashMap<TurkDiliTuru, Zemberek>();


    public DemoYonetici() {
        dilSec(TurkDiliTuru.TURKIYE);
    }

    public void dilSec(TurkDiliTuru dilTuru) {
        if (zemberekler.get(dilTuru) == null) {
            switch (dilTuru) {
                case TURKIYE:
                    zemberekler.put(dilTuru, new Zemberek(new TurkiyeTurkcesi()));
                    break;
                case TURKMEN:
                    zemberekler.put(dilTuru, new Zemberek(new Turkmence()));
                    break;
            }
        }
        this.zemberek = zemberekler.get(dilTuru);
        this.dilBilgisi = zemberek.dilBilgisi();
    }

    public char[] ozelKarakterDizisiGetir() {
        return dilBilgisi.alfabe().asciiDisiHarfler();
    }

    public String islemUygula(String islemTipi, String giris) {
        if (islemTipi.equals(IslemTipi.YAZI_DENETLE.toString()))
            return yaziDenetle(giris);
        if (islemTipi.equals(IslemTipi.YAZI_COZUMLE.toString()))
            return yaziCozumle(giris);
        if (islemTipi.equals(IslemTipi.ASCII_TURKCE.toString()))
            return asciiToTurkce(giris);
        if (islemTipi.equals(IslemTipi.TURKCE_ASCII.toString()))
            return turkceToAscii(giris);
        if (islemTipi.equals(IslemTipi.HECELE.toString()))
            return hecele(giris);
        if (islemTipi.equals(IslemTipi.ONER.toString()))
            return oner(giris);
        if (islemTipi.equals(IslemTipi.TEMIZLE.toString()))
            return temizle(giris);
        return "";
    }

    public String islemUygula(IslemTipi islemTipi, String giris) {
        if (islemTipi == IslemTipi.YAZI_DENETLE)
            return yaziDenetle(giris);
        if (islemTipi == IslemTipi.YAZI_COZUMLE)
            return yaziCozumle(giris);
        if (islemTipi == IslemTipi.ASCII_TURKCE)
            return asciiToTurkce(giris);
        if (islemTipi == IslemTipi.TURKCE_ASCII)
            return turkceToAscii(giris);
        if (islemTipi == IslemTipi.HECELE)
            return hecele(giris);
        if (islemTipi == IslemTipi.ONER)
            return oner(giris);
        if (islemTipi == IslemTipi.TEMIZLE)
            return temizle(giris);
        return "";
    }

    public String yaziDenetle(String giris) {
        List<YaziBirimi> analizDizisi = YaziIsleyici.analizDizisiOlustur(giris);
        StringBuffer sonuc = new StringBuffer();
        for (YaziBirimi birim : analizDizisi) {
            if (birim.tip == YaziBirimiTipi.KELIME) {
                if (!zemberek.kelimeDenetle(birim.icerik))
                    birim.icerik = "#" + birim.icerik;
            }
            sonuc.append(birim.icerik);
        }
        return sonuc.toString();
    }

    public String yaziCozumle(String giris) {
        List<YaziBirimi> analizDizisi = YaziIsleyici.analizDizisiOlustur(giris);
        StringBuffer sonuc = new StringBuffer();
        for (YaziBirimi birim : analizDizisi) {
            if (birim.tip == YaziBirimiTipi.KELIME) {
                Kelime[] cozumler = zemberek.kelimeCozumle(birim.icerik);

                if (cozumler.length == 0)
                    sonuc.append(birim.icerik).append(" :cozulemedi\n");
                else {
                    for (Kelime cozum : cozumler)
                        sonuc.append(cozum).append("\n");
                }
            }
        }
        return sonuc.toString();
    }


    public String asciiToTurkce(String giris) {
        List<YaziBirimi> analizDizisi = YaziIsleyici.analizDizisiOlustur(giris);
        StringBuffer sonuc = new StringBuffer();
        for (YaziBirimi birim : analizDizisi) {
            if (birim.tip == YaziBirimiTipi.KELIME) {
                Kelime[] sonuclar = zemberek.asciiCozumle(birim.icerik);
                Set<String> tekilSonuclar = new HashSet(2);
                for (Kelime s : sonuclar) {
                    tekilSonuclar.add(s.icerik().toString());
                }

                if (tekilSonuclar.size() == 0)
                    birim.icerik = "#" + birim.icerik;
                else if (tekilSonuclar.size() == 1)
                    birim.icerik = (String) tekilSonuclar.iterator().next();
                else {
                    StringBuffer bfr = new StringBuffer("[ ");
                    for (Iterator iterator = tekilSonuclar.iterator(); iterator.hasNext();) {
                        String s = (String) iterator.next();
                        bfr.append(s).append(" ");
                    }
                    bfr.append("]");
                    birim.icerik = bfr.toString();
                }
            }
            sonuc.append(birim.icerik);
        }
        return sonuc.toString();
    }


    public String turkceToAscii(String giris) {
        List analizDizisi = YaziIsleyici.analizDizisiOlustur(giris);
        StringBuffer sonuc = new StringBuffer();
        for (int i = 0; i < analizDizisi.size(); i++) {
            YaziBirimi birim = (YaziBirimi) analizDizisi.get(i);
            if (birim.tip == YaziBirimiTipi.KELIME)
                birim.icerik = zemberek.asciiyeDonustur(birim.icerik);
            sonuc.append(birim.icerik);
        }
        return sonuc.toString();
    }

    public String hecele(String giris) {
        List analizDizisi = YaziIsleyici.analizDizisiOlustur(giris);
        StringBuffer sonuc = new StringBuffer();
        for (int i = 0; i < analizDizisi.size(); i++) {
            YaziBirimi birim = (YaziBirimi) analizDizisi.get(i);
            if (birim.tip == YaziBirimiTipi.KELIME) {
                birim.icerik = dilBilgisi.alfabe().ayikla(birim.icerik);
                if (dilBilgisi.alfabe().cozumlemeyeUygunMu(birim.icerik) == false)
                    birim.icerik = "#" + birim.icerik;
                else {
                    String[] sonuclar = zemberek.hecele(birim.icerik);
                    if (sonuclar.length == 0)
                        birim.icerik = "#" + birim.icerik;
                    else {
                        StringBuffer bfr = new StringBuffer("[");
                        for (int j = 0; j < sonuclar.length - 1; j++)
                            bfr.append(sonuclar[j]).append("-");
                        bfr.append(sonuclar[sonuclar.length - 1]).append("]");
                        birim.icerik = bfr.toString();
                    }
                }
            }
            sonuc.append(birim.icerik);
        }
        return sonuc.toString();
    }

    public String oner(String giris) {
        List analizDizisi = YaziIsleyici.analizDizisiOlustur(giris);
        StringBuffer sonuc = new StringBuffer();
        for (int i = 0; i < analizDizisi.size(); i++) {
            YaziBirimi birim = (YaziBirimi) analizDizisi.get(i);
            if (birim.tip == YaziBirimiTipi.KELIME) {
                String[] cozumler = zemberek.oner(birim.icerik);
                if (cozumler.length == 0)
                    birim.icerik = "#" + birim.icerik;
                else if (cozumler.length == 1)
                    birim.icerik = (cozumler[0]).toString();
                else {
                    StringBuffer bfr = new StringBuffer("[ ");
                    for (int j = 0; j < cozumler.length; j++) {
                        bfr.append(cozumler[j]);
                        if (j < cozumler.length - 1)
                            bfr.append(", ");
                    }
                    bfr.append("]");
                    birim.icerik = bfr.toString();
                }
            }
            sonuc.append(birim.icerik);
        }
        return sonuc.toString();
    }

    public String temizle(String giris) {
        return zemberek.temizle(giris);
    }

    public String turkceTest(String giris) {
        int sonuc = zemberek.dilTesti(giris);
        if (sonuc == TurkceYaziTesti.HIC)
            return "Turkce degil";
        if (sonuc == TurkceYaziTesti.AZ)
            return "Yazi Turkce degil ama turkce olabilecek kelimeler iceriyor";
        if (sonuc == TurkceYaziTesti.ORTA)
            return "Turkce. Cok miktarda yanlis yazilmis ya da yabanci kelime iceriyor ";
        if (sonuc == TurkceYaziTesti.YUKSEK)
            return "Turkce. Yanlis yazilmis ya da yabanci kelimeler iceriyor";
        return "Turkce";
    }
}
