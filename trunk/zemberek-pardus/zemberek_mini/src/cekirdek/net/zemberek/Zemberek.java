package net.zemberek;

import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Properties;
import java.util.Set;
import java.util.logging.Logger;

import net.zemberek.bilgi.KaynakYukleyici;
import net.zemberek.bilgi.ZemberekAyarlari;
import net.zemberek.bilgi.kokler.KokBulucu;
import net.zemberek.bilgi.kokler.Sozluk;
import net.zemberek.islemler.AsciiDonusturucu;
import net.zemberek.islemler.HataliKodlamaTemizleyici;
import net.zemberek.islemler.Heceleyici;
import net.zemberek.islemler.KelimeKokFrekansKiyaslayici;
import net.zemberek.islemler.KelimeUretici;
import net.zemberek.islemler.cozumleme.AsciiToleransliHDKiyaslayici;
import net.zemberek.islemler.cozumleme.KelimeCozumleyici;
import net.zemberek.islemler.cozumleme.KesinHDKiyaslayici;
import net.zemberek.islemler.cozumleme.OneriUretici;
import net.zemberek.islemler.cozumleme.StandartCozumleyici;
import net.zemberek.islemler.cozumleme.ToleransliCozumleyici;
import net.zemberek.yapi.DilAyarlari;
import net.zemberek.yapi.DilBilgisi;
import net.zemberek.yapi.Kelime;
import net.zemberek.yapi.Kok;
import net.zemberek.yapi.TurkceDilBilgisi;

/**
 * Zemberek projesine ust seviye erisim icin kullanilan sinif.
 * Ilk olsum sirasinda kokler okuma ve agac olusumu nedeniyle belli bir miktar gecikme
 * yasanabilir.
 */
public class Zemberek {

    static Logger log = Logger.getLogger(Zemberek.class.getName());
    private KelimeCozumleyici cozumleyici;
    private KelimeUretici kelimeUretici;
    private KelimeCozumleyici asciiToleransliCozumleyici;
    private HataliKodlamaTemizleyici temizleyici;
    private OneriUretici oneriUretici;
    private AsciiDonusturucu asciiDonusturucu;
    private Heceleyici heceleyici;
    private ZemberekAyarlari ayarlar;
    private DilBilgisi dilBilgisi;

    public Zemberek(DilAyarlari dilayarlari) {
        this.dilBilgisi = new TurkceDilBilgisi(dilayarlari);
        ayarlar = new ZemberekAyarlari(dilBilgisi.tur());
        initialize();
    }

    /**
     * Dosya sisteminden zemberek properties dosyasini yukleyip ZemberekAyarlari nesnesine atar.
     *
     * @param disKonfigurasyon
     * @return
     * @throws IOException
     */
    public static ZemberekAyarlari ayarOlustur(String disKonfigurasyon) throws IOException {
        URI uri = new File(disKonfigurasyon).toURI();
        Properties props = new KaynakYukleyici().konfigurasyonYukle(uri);
        return new ZemberekAyarlari(props);
    }

    private void initialize() {
        //Sozluk hazirla.
        Sozluk kokler = dilBilgisi.kokler();
        //Normal denetleyici-cozumleyici olusumu
        KokBulucu kokBulucu = kokler.getKokBulucuFactory().getKesinKokBulucu();
        cozumleyici = new StandartCozumleyici(
                kokBulucu,
                new KesinHDKiyaslayici(),
                dilBilgisi.alfabe(),
                dilBilgisi.ekler(),
                dilBilgisi.cozumlemeYardimcisi());

        // ASCII-Turkce donusturucu icin tukce toleransli cozumleyici olusumu.
        KokBulucu turkceToleransliKokBulucu = kokler.getKokBulucuFactory().getAsciiKokBulucu();
        asciiToleransliCozumleyici = new StandartCozumleyici(
                turkceToleransliKokBulucu,
                new AsciiToleransliHDKiyaslayici(),
                dilBilgisi.alfabe(),
                dilBilgisi.ekler(),
                dilBilgisi.cozumlemeYardimcisi());

        KokBulucu toleransliBulucu = kokler.getKokBulucuFactory().getToleransliKokBulucu(1);
        ToleransliCozumleyici toleransliCozumleyici = new ToleransliCozumleyici(
                toleransliBulucu,
                dilBilgisi.ekler(),
                dilBilgisi.alfabe(),
                dilBilgisi.cozumlemeYardimcisi());

        oneriUretici = new OneriUretici(
                dilBilgisi.cozumlemeYardimcisi(),
                cozumleyici,
                asciiToleransliCozumleyici,
                toleransliCozumleyici,
                ayarlar);

        asciiDonusturucu = new AsciiDonusturucu(dilBilgisi.alfabe());
        heceleyici = new Heceleyici(dilBilgisi.alfabe(), dilBilgisi.heceBulucu());

        kelimeUretici = new KelimeUretici(dilBilgisi.alfabe(), dilBilgisi.cozumlemeYardimcisi());
    }

    public KelimeCozumleyici cozumleyici() {
        return cozumleyici;
    }

    public KelimeUretici kelimeUretici() {
        return kelimeUretici;
    }

    public KelimeCozumleyici asciiToleransliCozumleyici() {
        return asciiToleransliCozumleyici;
    }

    public OneriUretici oneriUretici() {
        return oneriUretici;
    }

    public Heceleyici heceleyici() {
        return heceleyici;
    }

    /**
     * girisin imla denetimini yapar.
     *
     * @param giris
     * @return true: imla denetimi basarili. false: Denetim basarisiz.
     */
    public boolean kelimeDenetle(String giris) {
        return cozumleyici.denetle(giris);
    }

    /**
     * giris kelimesinin olasi tum (kok+ekler) cozumlemelerini dondurur.
     *
     * @param giris
     * @return Kelime sinifi cinsinden dizi. Eger dizinin boyu 0 ise kelime cozumlenemedi demektir.
     *         Kelime kokune erisim icin kok(), eklere erisim icin Ek cinsinden nesne listesi donduren
     *         ekler() metodu kullanilir.
     * @see net.zemberek.yapi.Kelime
     */
    public Kelime[] kelimeCozumle(String giris) {
        return cozumleyici.cozumle(giris);
    }

    /**
     * giris kelimesinin ascii karakter toleransli olarak cozumleyip
     * Kelime cinsinden(kok+ekler) cozumlemelerini dondurur.
     * Birden cok cozumun oldugu durumda simdilik donen adaylarin
     * hangisinin gercekten yazidaki kelime olup olmadigi belirlenmiyor. ancak donen sonuclar
     * basitce kok kullanim frekansina gore dizilir. Yani ilk kelime buyuk ihtimalle kastedilen kelimedir.
     *
     * @param giris
     * @return Kelime sinifi cinsinden dizi. Eger dizinin boyu 0 ise kelime cozumlenemedi demektir.
     *         Kelime kokune erisim icin kok(), eklere erisim icin Ek cinsinden nesne listesi donduren
     *         ekler() metodu kullanilir.  Kelimenin String cinsinden ifadesi icin icerik().toString()
     *         metodu kullanilabilir.
     * @see net.zemberek.yapi.Kelime
     */
    public Kelime[] asciiCozumle(String giris) {
        Kelime[] sonuclar = asciiToleransliCozumleyici.cozumle(giris);
        Arrays.sort(sonuclar, new KelimeKokFrekansKiyaslayici());
        return sonuclar;
    }

    /**
     * asciiCozumle ile benzer bir yapidadir. Farki String[] dizisi donmesi ve
     * donus degerlerinin tekil olmasidir, yani ayni kelime tekrari olmaz.
     *
     * @param giris
     * @return yazilan kelimenin olasi turkce karakter iceren halleri.
     */
    public String[] asciidenTurkceye(String giris) {
        Kelime[] kelimeler = asciiCozumle(giris);
        // cift olusumlari temizle.
        Set<String> olusumlar = new HashSet();
        for (Kelime kelime : kelimeler) {
            String olusum = kelime.icerik().toString();
            if (!olusumlar.contains(olusum))
                olusumlar.add(olusum);
        }
        //kumeyi tekrar diziye donustur.
        return olusumlar.toArray(new String[olusumlar.size()]);
    }

    /**
     * kelime icindeki dile ozel karakterleri ASCII benzer formalarina dondurur.
     *
     * @param giris
     * @return turkce karakter tasimayan String.
     */
    public String asciiyeDonustur(String giris) {
        return asciiDonusturucu.toAscii(giris);
    }

    /**
     * girilen kelimeyi heceler.
     *
     * @param giris
     * @return String dizisi. Eger dizi boyu 0 ise kelime hecelenememis demektir.
     */
    public String[] hecele(String giris) {
        return heceleyici.hecele(giris);
    }

    /**
     * giris kelimesine yakin Stringleri dondurur. Yani eger kelime bozuk ise bu kelimeye
     * benzeyen dogru kelime olasiliklarini dondurur. simdilik
     * - 1 harf eksikligi
     * - 1 harf fazlaligi
     * - 1 yanlis harf kullanimi
     * - yanyana yeri yanlis harf kullanimi.
     * hatalarini giderecek sekilde cozumleri donduruyor. Bu metod dogru kelimeler icin de
     * isler, yani giris "kedi" ise donus listesinde kedi ve kedi'ye benzesen kelimeler de doner.
     * Ornegin "kedim", "yedi" .. gibi.
     *
     * @return String sinifi cinsinden dizi. Eger dizinin boyu 0 ise kelime cozumlenemedi demektir.
     * @see net.zemberek.yapi.Kelime
     */
    public String[] oner(String giris) {
        return oneriUretici.oner(giris);
    }

    /**
     * giris kelime ya da yazisi icindeki cesitli kodlama hatalarindan kaynkalanan
     * bozulmalari onarir. Bu metod kelime ya da kelime dizisi icin calisir
     * Bazi bozulmalar henuz duzeltilemiyor olabilir.
     *
     * @param giris
     * @return girisin temizlenmis hali.
     */
    public String temizle(String giris) {
        if (temizleyici == null) {
            temizleyici = new HataliKodlamaTemizleyici();
            try {
                temizleyici.initialize();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        if (temizleyici == null) return null;
        return temizleyici.temizle(giris);
    }

    /**
     * nesnenin olusumu sirasinda kullanilan DilBilgisi arabirimine sahip dili dondurur.
     * Eger nesne hic parametre kullanilmadan olusturulmussa bir adet TurkiyeTurkcesi nesnesi doner.
     *
     * @return bu nesneyi olustururken kullanilan DilBilgisi arayuzune sahip nesne.
     */
    public DilBilgisi dilBilgisi() {
        return dilBilgisi;
    }

    /**
     * Istenilen kok ve ek listesi ile kelime uretir.
     *
     * @return String olarak uretilen kelime.
     */
    public String kelimeUret(Kok kok, List ekler) {
        return kelimeUretici.kelimeUret(kok, ekler);
    }

    /**
     * Istenilen kelimenin olasi String acilimlarini bulur.
     * Ornegin, "alayim" icin
     * "al-a-yim" ve "ala-yim" cozumleri String dizileri seklinde uretilir.
     * sonucta olusan diziler bir Listeye eklenir.
     *
     * @return Kok ve ek olusumlarini ifade eden String dizilerini tasiyan List.
     *         List<List<String>>
     *         Eger kelime ayristirilamiyorsa sifir uzunluklu String dizisi tasiyan tek elemanli
     *         liste doner. .
     */
    public List<List<String>> kelimeAyristir(String kelime) {
        Set<List<String>> sonuclar = new HashSet();
        Kelime[] cozumler = cozumleyici.cozumle(kelime);
        for (Kelime kel : cozumler) {
            sonuclar.add(kelimeUretici.ayristir(kel));
        }
        return new ArrayList(sonuclar);
    }

    /**
     * Zemberek konfigurasyon parametrelerini dondurur.
     *
     * @return ayarlar.
     */
    public ZemberekAyarlari ayarlar() {
        return ayarlar;
    }

/*    public static void main(String[] args) throws IOException {

        Zemberek zemberek;
        if (args.length == 3) {
            String propFile = args[2];
            ZemberekAyarlari ayarlar = Zemberek.ayarOlustur(propFile);
            zemberek = new Zemberek(ayarlar, new TurkiyeTurkcesi(ayarlar));
            log.info("dis konfigurasyon dosyasina erisildi.");
        } else
            zemberek = new Zemberek();
        if (args == null || args.length < 2) {
            System.out.println("En az  veri girmelisiniz." +
                    "\n denetle <kelime>," +
                    "\n hecele <kelime>," +
                    "\n denetle <kelime>," +
                    "\n deasc <kelime>," +
                    "\n oner <kelime>-");
            System.exit(1);
        }
        String komut = args[0];
        String kelime = args[1];

        if (komut.equals("hecele")) {
            String[] sonuclar = zemberek.hecele(kelime);
            if (sonuclar.length == 0)
                System.out.println("kelime hecelenemez.");
            else {
                StringBuffer bfr = new StringBuffer("[");
                for (int j = 0; j < sonuclar.length - 1; j++)
                    bfr.append(sonuclar[j]).append("-");
                bfr.append(sonuclar[sonuclar.length - 1]).append("]");
                kelime = bfr.toString();
            }
            System.out.println("sonuc = " + kelime);
        } else if (komut.equals("denetle")) {
            Kelime[] sonuclar = zemberek.kelimeCozumle(kelime);
            for (int i = 0; i < sonuclar.length; i++) {
                Kelime kelime1 = sonuclar[i];
                System.out.println(kelime1);
            }
        } else if (komut.equals("denetle"))
            System.out.println(zemberek.kelimeDenetle(kelime));
        else if (komut.equals("deasc")) {
            Kelime[] sonuclar = zemberek.asciiCozumle(kelime);
            kelimeYaz(sonuclar);
        } else if (komut.equals("oner")) {
            Kelime[] sonuclar = zemberek.asciiCozumle(kelime);
            kelimeYaz(sonuclar);
        } else
            System.out.println("bilinmeyen komut..");
    }*/

    private static void kelimeYaz(Kelime[] sonuclar) {
        for (int i = 0; i < sonuclar.length; i++) {
            Kelime kelime1 = sonuclar[i];
            System.out.println(kelime1.icerik());
        }
    }


}
