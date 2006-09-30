package net.zemberek.yapi;


/**
 * User: aakin
 * Date: Feb 24, 2004
 * Bu sinif Dil islemleri sirasinda Turkceye ozel islemler gerektiginden String-StringBuffer yerine kullanilir.
 * String gibi genel bir tasiyici degil ara islem nesnesi olarak kullanilmasi onerilir.
 * String'den farkli olarak "degistirilebilir" bir yapidadir ve Thread-safe degildir.
 */
public class HarfDizisi implements CharSequence {

    private TurkceHarf[] dizi;
    private int boy = 0;

    /**
     * default constructor. 7 boyutlu bir TurkceHarf referans dizisi olusturur.
     */
    public HarfDizisi() {
        dizi = new TurkceHarf[7];
    }

    /**
     * 'kapasite' boyutlu 'TurkceHarf' dizisine sahip nesne olusturur.
     *
     * @param kapasite
     */
    public HarfDizisi(int kapasite) {
        dizi = new TurkceHarf[kapasite];
    }

    /**
     * 'kapasite' boyutlu 'TurkceHarf' dizisine sahip nesne olusturur. daha sonra
     * girisi String'i icindeki karakterleri TurkceHarf seklinde TurkceHarf dizisine aktarir.
     * Eger String boyu kapasiteden buyukse kapasite'yi boy'a esitler.
     * Eger String icindeki karakter Alfabe'de yar almiyorsa "HARF_YOK" harfi olarak eklenir.
     *
     * @param str
     * @param kapasite
     */
    public HarfDizisi(String str, Alfabe alfabe, int kapasite) {
        if (kapasite < str.length())
            kapasite = str.length();
        dizi = new TurkceHarf[kapasite];
        boy = str.length();
        for (int i = 0; i < boy; i++)
            dizi[i] = alfabe.harf(str.charAt(i));
    }


    /**
     * Belirlenen alfabe ile String icerigini Harflere donusturur.
     *
     * @param str
     */
    public HarfDizisi(String str, Alfabe alfabe) {
        boy = str.length();
        dizi = new TurkceHarf[boy];
        for (int i = 0; i < boy; i++)
            dizi[i] = alfabe.harf(str.charAt(i));
    }

    /**
     * Copy-Constructor. gelen harf dizisi ile ayni icerige sahip olacak sekilde
     * TurkceHarf dizisi olusturur.
     *
     * @param hdizi
     */
    public HarfDizisi(HarfDizisi hdizi) {
        boy = hdizi.length();
        dizi = new TurkceHarf[boy];
        System.arraycopy(hdizi.dizi, 0, dizi, 0, boy);
    }

    /**
     * gelen TurkceHarf dizisini icerige kopyalar.
     *
     * @param hdizi
     */
    private HarfDizisi(TurkceHarf[] hdizi) {
        boy = hdizi.length;
        dizi = new TurkceHarf[boy];
        System.arraycopy(hdizi, 0, dizi, 0, boy);
    }

    /**
     * bu metod harf referansi dizisini serbest birakmaz,
     * sadece boyu sifira indirir.
     */
    public void sil() {
        boy = 0;
    }

    /**
     * Dizinin son harfini dondurur.
     *
     * @return varsa son harf, Yoksa HARF_YOK.
     */
    public final TurkceHarf sonHarf() {
        if (boy > 0)
            return dizi[boy - 1];
        else
            return Alfabe.HARF_YOK;
    }

    /**
     * dizideki son sesliyi dondurur. eger dizi boyu 0 ise ya da sesli harf yoksa
     * HARF_YOK doner.
     *
     * @return varsa son sesli yoksa HARF_YOK
     */
    public final TurkceHarf sonSesli() {
        for (int i = boy - 1; i >= 0; i--) {
            if (dizi[i].sesliMi())
                return dizi[i];
        }
        return Alfabe.HARF_YOK;
    }

    /**
     * ic metod. harf dizisinin boyutu yetersiz geldiginde "ek" miktarinda daha
     * fazla yere sahip yeni dizi olusturulup icerik yeni diziye kopyalanir.
     *
     * @param ek
     */
    private void kapasiteAyarla(int ek) {
        TurkceHarf[] yeniDizi = new TurkceHarf[dizi.length + ek];
        System.arraycopy(dizi, 0, yeniDizi, 0, dizi.length);
        dizi = yeniDizi;
    }

    /**
     * otomatik kapasite ayarlama. dizi boyu iki katina cikarilir.
     */
    private void kapasiteAyarla() {
        TurkceHarf[] yeniDizi = new TurkceHarf[dizi.length * 2];
        System.arraycopy(dizi, 0, yeniDizi, 0, dizi.length);
        dizi = yeniDizi;
    }

    /**
     * kelimenin sonuna harf ekler.
     *
     * @param harf
     */
    public HarfDizisi ekle(TurkceHarf harf) {
        if (boy == dizi.length)
            kapasiteAyarla(3);
        dizi[boy++] = harf;
        return this;
    }

    /**
     * girilen pozisyona herf ekler, bu noktadan sonraki harfler otelenir.
     *
     * @param index
     * @param harf
     */
    public void ekle(int index, TurkceHarf harf) {
        if (index < 0 || index > boy) throw new IndexOutOfBoundsException();
        if (boy == dizi.length)
            kapasiteAyarla();
        for (int i = boy - 1; i >= index; i--)
            dizi[i + 1] = dizi[i];
        dizi[index] = harf;
        boy++;
    }

    /**
     * Diziye baska bir harf dizisinin icerigini ular.
     *
     * @param hdizi
     */
    public HarfDizisi ekle(HarfDizisi hdizi) {
        int hboy = hdizi.length();
        if (boy + hboy > dizi.length)
            kapasiteAyarla(hboy);
        System.arraycopy(hdizi.dizi, 0, dizi, boy, hboy);
        boy += hdizi.length();
        return this;
    }

    /**
     * Diziye baska bir harf dizisinin icerigini index ile belirtilen harften itibaren ekler.
     *
     * @param hdizi
     */
    public HarfDizisi ekle(int index, HarfDizisi hdizi) {
        if (index < 0 || index > boy) throw new IndexOutOfBoundsException();
        
        //dizi kapasitesini ayarla
        int hboy = hdizi.length();
        if (boy + hboy > dizi.length)
            kapasiteAyarla(hboy);

        //sondan baslayarak this.dizinin index'ten sonraki kismini dizinin sonuna tasi
        for (int i = hboy + boy - 1; i >= hboy; i--)
            dizi[i] = dizi[i - hboy];

        //gelen diziyi kopyala ve boyutu degistir.
        System.arraycopy(hdizi.dizi, 0, dizi, index, hboy);
        boy += hdizi.length();
        return this;
    }


    /**
     * verilen pozisyondaki harfi dondurur. icerigi "kedi" olan HarfDizisi icin
     * harf(1) dondurur.
     *
     * @param i
     * @return girilen pozisyondaki harf, yoksa HARF_YOK
     */
    public final TurkceHarf harf(int i) {
        if (i < 0)
            return Alfabe.HARF_YOK;
        if (i < boy)
            return dizi[i];
        return Alfabe.HARF_YOK;
    }

    /**
     * ilk sesliyi dondurur. eger sesli yoksa HARF_YOK doner.
     *
     * @param basla
     * @return varsa ilk sesli, yoksa HARF_YOK
     */
    public TurkceHarf ilkSesli(int basla) {
        for (int i = basla; i < boy; i++) {
            if (dizi[i].sesliMi())
                return dizi[i];
        }
        return Alfabe.HARF_YOK;
    }

    /**
     * Tam esitlik kiyaslamasi. kiyaslama nesne tipi, ardindan da TurkceHarf dizisi icindeki
     * harflerin char iceriklerine gore yapilir.
     *
     * @param o
     * @return true eger esitse.
     */
    public boolean equals(Object o) {
        if (o == null) return false;
        if (this == o) return true;
        if (!(o instanceof HarfDizisi)) return false;

        final HarfDizisi harfDizisi = (HarfDizisi) o;
        if (boy != harfDizisi.boy) return false;
        for (int i = 0; i < boy; i++) {
            if (dizi[i].charDeger() != harfDizisi.dizi[i].charDeger())
                return false;
        }
        return true;
    }

    public int hashCode() {
        return toString().hashCode();
    }

    /**
     * ascii benzer harf toleransli esitlik kiyaslamasi.
     *
     * @param harfDizisi
     * @return true eger esitse.
     */
    public final boolean asciiToleransliKiyasla(HarfDizisi harfDizisi) {
        if (harfDizisi == null) return false;
        if (this == harfDizisi) return true;
        if (boy != harfDizisi.boy) return false;
        for (int i = 0; i < boy; i++) {
            if (!dizi[i].asciiToleransliKiyasla(harfDizisi.dizi[i]))
                return false;
        }
        return true;
    }

    public final boolean asciiToleransliAradanKiyasla(int baslangic, HarfDizisi kelime) {
        if (kelime == null) return false;
        if (boy < baslangic + kelime.length())
            return false;
        for (int i = 0; i < kelime.length(); i++)
            if (!dizi[baslangic + i].asciiToleransliKiyasla(kelime.harf(i)))
                return false;
        return true;
    }

    public final boolean asciiToleransliBastanKiyasla(HarfDizisi giris) {
        if (giris == null) return false;
        if (giris.length() > this.boy)
            return false;
        for (int i = 0; i < giris.length(); i++)
            if (!dizi[i].asciiToleransliKiyasla(giris.harf(i)))
                return false;
        return true;
    }

    public final boolean aradanKiyasla(int baslangic, HarfDizisi kelime) {
        if (kelime == null) return false;
        if (boy < baslangic + kelime.length())
            return false;
        for (int i = 0; i < kelime.length(); i++)
            if (dizi[baslangic + i].charDeger() != kelime.harf(i).charDeger())
                return false;
        return true;
    }

    public final boolean bastanKiyasla(HarfDizisi giris) {
        if (giris == null) return false;
        if (giris.length() > this.boy)
            return false;
        for (int i = 0; i < giris.length(); i++)
            if (dizi[i].charDeger() != giris.harf(i).charDeger())
                return false;
        return true;
    }

    /**
     * istenen noktadaki harfi giris parametresi olan TurkceHarf ile degistirir.
     *
     * @param index
     * @param harf
     */
    public final void harfDegistir(int index, TurkceHarf harf) {
        if (index < 0 || index >= boy)
            throw new StringIndexOutOfBoundsException(index);
        dizi[index] = harf;
    }

    /**
     * son harfi yumusatir. Eger harfin yumusamis formu yoksa harf degismez.
     */
    public void sonHarfYumusat() {
        if (boy == 0)
            return;
        TurkceHarf yum = dizi[boy - 1].getYumusama();
        if (yum != null)
            dizi[boy - 1] = dizi[boy - 1].getYumusama();
    }

    /**
     * son harfi siler. eger harf yoksa hicbir etki yapmaz.
     */
    public void sonHarfSil() {
        if (boy > 0)
            boy--;
    }

    /**
     * verilen pozisyondaki harfi siler. kelimenin kalan kismi otelenir.
     * eger verilen pozisyon yanlis ise  StringIndexOutOfBoundsException firlatir.
     *
     * @param index
     * @return dizinin kendisi.
     */
    public HarfDizisi harfSil(int index) {
        if (index < 0 || index >= boy)
            throw new StringIndexOutOfBoundsException(index);
        if (index == boy - 1) {
            boy--;
        } else {
            for (int i = index; i < boy - 1; i++)
                dizi[i] = dizi[i + 1];
            boy--;
        }
        return this;
    }

    public HarfDizisi harfSil(int index, int harfSayisi) {
        if (index < 0 || index >= boy)
            throw new StringIndexOutOfBoundsException(index);
        if (index + harfSayisi > boy)
            harfSayisi = boy - index;
        for (int i = index + harfSayisi; i < boy; i++)
            dizi[i - harfSayisi] = dizi[i];
        boy -= harfSayisi;
        return this;
    }

    /**
     * ilk harfi dondurur. eger harf yoksa HARF_YOK doner.
     *
     * @return ilk TurkceHarf.
     */
    public final TurkceHarf ilkHarf() {
        if (boy == 0) return Alfabe.HARF_YOK;
        else
            return dizi[0];
    }

    /**
     * "index" numarali harften itibaren siler.
     *
     * @param index
     */
    public final void kirp(int index) {
        if (index <= boy && index >= 0)
            boy = index;
    }

    /**
     * sadece belirli bir bolumunu String'e donusturur.
     * @param index String'e donusum baslangic noktasi.
     * @return olusan String.
     */
    public String toString(int index) {
        if (index < 0 || index >= boy) return "";
        StringBuilder s = new StringBuilder(boy - index);
        for (int i = index; i < boy; i++)
            s.append(charAt(i));
        return s.toString();
    }

    public String toString() {
        return new StringBuilder(this).toString();
    }

    /* ------------------------- ozel metodlar ------------------------------- */

    /**
     * Genellikle kelimedeki hece sayisini bulmak icin kullanilir.
     *
     * @return inte, sesli harf sayisi.
     */
    public int sesliSayisi() {
        int sonuc = 0;
        for (int i = 0; i < boy; i++) {
            if (dizi[i].sesliMi())
                sonuc++;
        }
        return sonuc;
    }

    /**
     * @return hepsi buyuk harf ise true, boy=0 dahil.
     */
    public boolean hepsiBuyukHarfmi() {
        for (int i = 0; i < boy; i++) {
            if (!dizi[i].buyukHarfMi())
                return false;
        }
        return true;
    }

    //--------- asagidaki metodlar CharSequence arayuzu icin hazirlandi. -----

    public final int length() {
        return boy;
    }

    public final char charAt(int index) {
        if (index < 0 || index >= boy)
            throw new StringIndexOutOfBoundsException(index);
        return dizi[index].charDeger();
    }

    public CharSequence subSequence(int start, int end) {
        if (end < start) return null;
        TurkceHarf[] yeniHarfler = new TurkceHarf[end - start];
        System.arraycopy(dizi, start, yeniHarfler, 0, end - start);
        return new HarfDizisi(yeniHarfler);
    }

}
