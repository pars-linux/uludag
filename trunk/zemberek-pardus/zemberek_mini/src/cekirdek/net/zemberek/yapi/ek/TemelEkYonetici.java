package net.zemberek.yapi.ek;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import net.zemberek.yapi.Alfabe;
import net.zemberek.yapi.KelimeTipi;
import net.zemberek.yapi.Kok;

/**
 * Bu sinif dile ozel ek yonetici siniflar icin taban olarak kullanilir.
 * icerisinde cesitli ek bilgileri yer alir.
 * User: ahmet
 * Date: Sep 21, 2006
 */
public abstract class TemelEkYonetici implements EkYonetici{

    public static final Ek BOS_EK = new Ek("BOS_EK");

    protected Alfabe alfabe;
    protected Map<String, Ek> ekler;

    protected Set<Ek> iyelikEkleri = new HashSet();

    protected Set<Ek> halEkleri = new HashSet();

    protected Map<KelimeTipi, Ek> baslangicEkleri = new HashMap();


    protected abstract void ozelEkleriBelirle();

   /**
     * adi verilen Ek nesnesini bulur. Eger ek yok ise null doner.
     *
     * @param ekId - ek adi
     * @return istenen Ek nesnesi.
     */
    public Ek ek(String ekId) {
        Ek ek = ekler.get(ekId);
        if (ek == null)
            System.out.println("Ek bulunamiyor!" + ekId);
        return ekler.get(ekId);
    }

    /**
     * Kok nesnesinin tipine gore gelebilecek ilk ek'i dondurur.
     * Baslangic ekleri bilgisi dil tarafindan belirlenir.
     * @param kok
     * @return ilk Ek, eger kok tipi baslangic ekleri <baslangicEkleri>
     * haritasinda belirtilmemisse BOS_EK doner.
     */
    public Ek ilkEkBelirle(Kok kok) {
        Ek baslangicEki = baslangicEkleri.get(kok.tip());
        if (baslangicEki != null)
            return baslangicEki;
        else
            return BOS_EK;
    }

    public boolean iyelikEkiMi(Ek ek) {
        if (iyelikEkleri.contains(ek))
            return true;
        else
            return false;
    }

    public boolean halEkiMi(Ek ek) {
        if (halEkleri.contains(ek))
            return true;
        else
            return false;
    }
}
