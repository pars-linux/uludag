package net.zemberek.yapi.kok;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import net.zemberek.yapi.Alfabe;
import net.zemberek.yapi.ek.Ek;
import net.zemberek.yapi.ek.EkYonetici;

/**
 * User: ahmet
 * Date: Aug 29, 2006
 */
public class TemelKokOzelDurumBilgisi {


    protected EkYonetici ekYonetici;
    protected Alfabe alfabe;
    protected Map<KokOzelDurumTipi, KokOzelDurumu> ozelDurumlar = new HashMap();
    protected Map<String, KokOzelDurumu> kisaAdOzelDurumlar = new HashMap();

    public static final int MAX_OZEL_DURUM_SAYISI = 30;
    protected KokOzelDurumu[] ozelDurumDizisi = new KokOzelDurumu[MAX_OZEL_DURUM_SAYISI];

    public TemelKokOzelDurumBilgisi(EkYonetici ekYonetici, Alfabe alfabe) {
        this.ekYonetici = ekYonetici;
        this.alfabe = alfabe;
    }

    public KokOzelDurumu ozelDurum(int indeks) {
        if (indeks < 0 || indeks >= ozelDurumDizisi.length)
            throw new IndexOutOfBoundsException("istenilen indekksli ozel durum mevcut degil:" + indeks);
        return ozelDurumDizisi[indeks];
    }

    public KokOzelDurumu kisaAdIleOzelDurum(String ozelDurumKisaAdi) {
        return kisaAdOzelDurumlar.get(ozelDurumKisaAdi);
    }

    protected KokOzelDurumu.Uretici uretici(KokOzelDurumTipi tip) {

        // bir adet kok ozel durumu uretici olustur.
        KokOzelDurumu.Uretici uretici = new KokOzelDurumu.Uretici(tip);

        // eger varsa kok adlarini kullanarak iliskili ekleri bul ve bir Set'e ata.
        String[] ekAdlari = tip.ekAdlari();
        if (ekAdlari.length > 0) {
            Set set = new HashSet(ekAdlari.length);
            for (String s : ekAdlari) {
                Ek ek = ekYonetici.ek(s);
                if (ek != null) {
                    set.add(ek);
                } else {
                    System.out.println(s + " eki bulunamadigindan kok ozel durumuna eklenemedi!");
                }
            }
            // ureticiye seti ata.
            uretici.gelebilecekEkler(set);
        }
        return uretici;
    }

    protected void ekle(KokOzelDurumTipi tip, KokOzelDurumu ozelDurum) {
        ozelDurumlar.put(tip, ozelDurum);
        ozelDurumDizisi[tip.indeks()] = ozelDurum;
        kisaAdOzelDurumlar.put(tip.kisaAd(), ozelDurum);
    }

    protected KokOzelDurumu bosOzelDurum(KokOzelDurumTipi tip) {
        return new BosKokOzelDurumu(new KokOzelDurumu.Uretici(tip));
    }

    public KokOzelDurumu ozelDurum(String kisaAd) {
        return kisaAdOzelDurumlar.get(kisaAd);
    }

    public KokOzelDurumu ozelDurum(KokOzelDurumTipi tip) {
        return ozelDurumlar.get(tip);
    }
}
