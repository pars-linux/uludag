/*
 * Created on 27.May.2005
 * MDA
 */
package net.zemberek.islemler.cozumleme;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

import net.zemberek.bilgi.ZemberekAyarlari;
import net.zemberek.islemler.KelimeKokFrekansKiyaslayici;
import net.zemberek.yapi.Kelime;

public class OneriUretici {

    private KelimeCozumleyici cozumleyici, asciiToleransliCozumleyici;
    private ToleransliCozumleyici toleransliCozumleyici;
    private CozumlemeYardimcisi yardimci;
    private ZemberekAyarlari ayarlar;


    public OneriUretici(CozumlemeYardimcisi yardimci,
                        KelimeCozumleyici cozumleyici,
                        KelimeCozumleyici asciiToleransliCozumleyici,
                        ToleransliCozumleyici toleransliCozumleyici,
                        ZemberekAyarlari ayarlar) {
        this.yardimci = yardimci;
        this.toleransliCozumleyici = toleransliCozumleyici;
        this.cozumleyici = cozumleyici;
        this.asciiToleransliCozumleyici = asciiToleransliCozumleyici;
        this.ayarlar = ayarlar;
    }

    /**
     * Verilen kelime i�in �neri �retir.
     * Yap�lan �neriler �u �ekildedir:
     * - K�kte 1, ekte 1 mesafeye kadar olmak �zere Levenshtein d�zeltme mesafesine uyan t�m �neriler
     * - Deasciifier'den d�n�� de�eri olarak gelen �neriler
     * - Kelimenin ayr�k iki kelimeden olu�mas� durumu i�in �neriler
     *
     * @param kelime : �neri ya�lmas� istenen giri� kelimesi
     * @return String[] olarak �neriler
     *         E�er �neri yoksa sifir uzunluklu dizi.
     */
    public String[] oner(String kelime) {
        // Once hatal� kelime i�in tek kelimelik �nerileri bulmaya �al��
        Kelime[] oneriler = toleransliCozumleyici.cozumle(kelime);
        //Deasciifierden bir �ey var m�?
        Kelime[] asciiTurkceOneriler = new Kelime[0];
        if (ayarlar.oneriDeasciifierKullan())
            asciiTurkceOneriler = asciiToleransliCozumleyici.cozumle(kelime);

        Set<String> ayriYazimOnerileri = Collections.EMPTY_SET;

        // Kelime yanlislikla bitisik yazilmis iki kelimeden mi olusmus?
        if (ayarlar.oneriBilesikKelimeKullan()) {
            for (int i = 1; i < kelime.length(); i++) {
                String s1 = kelime.substring(0, i);
                String s2 = kelime.substring(i, kelime.length());
                if (cozumleyici.denetle(s1) && cozumleyici.denetle(s2)) {

                    Set<String> set1 = new HashSet();
                    Kelime[] kelimeler1 = cozumleyici.cozumle(s1);
                    for (Kelime kelime1 : kelimeler1) {
                        yardimci.kelimeBicimlendir(kelime1);
                        set1.add(kelime1.icerik().toString());
                    }

                    Set<String> set2 = new HashSet();
                    Kelime[] kelimeler2 = cozumleyici.cozumle(s2);
                    for (Kelime kelime1 : kelimeler2) {
                        yardimci.kelimeBicimlendir(kelime1);
                        set2.add(kelime1.icerik().toString());
                    }

                    if (ayriYazimOnerileri.size() == 0) {
                        ayriYazimOnerileri = new HashSet();
                    }

                    for (String str1 : set1) {
                        for (String str2 : set2) {
                            ayriYazimOnerileri.add(str1 + " " + str2);
                        }
                    }
                }
            }
        }

        // erken donus..
        if (oneriler.length == 0 && ayriYazimOnerileri.size() == 0 && asciiTurkceOneriler.length == 0) {
            return new String[0];
        }

        // Onerileri puanland�rmak i�in bir listeye koy
        ArrayList<Kelime> oneriList = new ArrayList<Kelime>();
        oneriList.addAll(Arrays.asList(oneriler));
        oneriList.addAll(Arrays.asList(asciiTurkceOneriler));

        Collections.sort(oneriList, new KelimeKokFrekansKiyaslayici());

        // D�n�� listesi string olacak, Yeni bir liste olu�tur. 
        ArrayList<String> sonucListesi = new ArrayList();
        for (Kelime anOneriList : oneriList) {
            sonucListesi.add(anOneriList.icerik().toString());
        }

        //�ift sonu�lari liste sirasini bozmadan iptal et.
        ArrayList<String> rafineListe = new ArrayList();
        for (String aday : sonucListesi) {
            boolean aynisiVar = false;
            for (String aRafineListe : rafineListe) {
                if (aday.equals(aRafineListe)) {
                    aynisiVar = true;
                    break;
                }
            }
            if (!aynisiVar && rafineListe.size() < ayarlar.getOneriMax()) {
                rafineListe.add(aday);
            }
        }

        for (String oneri : ayriYazimOnerileri) {
            if (rafineListe.size() < ayarlar.getOneriMax())
                rafineListe.add(oneri);
            else
                break;
        }

        return rafineListe.toArray(new String[rafineListe.size()]);
    }
}
