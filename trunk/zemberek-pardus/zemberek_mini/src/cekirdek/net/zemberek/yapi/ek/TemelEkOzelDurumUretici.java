package net.zemberek.yapi.ek;

import net.zemberek.yapi.Alfabe;

/**
 * User: ahmet
 * Date: Sep 16, 2006
 */
public abstract class TemelEkOzelDurumUretici implements EkOzelDurumUretici {

    protected Alfabe alfabe;

    public enum TemelEkOzelDurumuTipi implements EkOzelDurumTipi {

        SON_HARF_YUMUSAMA,
        OLDURGAN,
        ON_EK,
        ZAMAN_KI;

        public String ad() {
            return name();
        }
    }

    public EkOzelDurumu uret(String ad) {
        if (!mevcut(TemelEkOzelDurumuTipi.values(), ad))
            return null;
        else
            switch (TemelEkOzelDurumuTipi.valueOf(ad)) {
                case SON_HARF_YUMUSAMA:
                    return new SonHarfYumusamaOzelDurumu();
                case OLDURGAN:
                    return new OldurganEkOzelDurumu(alfabe);
                case ON_EK:
                    return new OnEkOzelDurumu();
                case ZAMAN_KI:
                    return new ZamanKiOzelDurumu();
                default:
                    return null;
            }
    }

    /**
     * efektif olmayan bir tip denetimi.
     *
     * @param tipler
     * @param ad
     * @return eger ad ile belirtilen tip var ise true.
     */
    protected boolean mevcut(EkOzelDurumTipi[] tipler, String ad) {
        for (EkOzelDurumTipi tip : tipler) {
            if (tip.ad().equals(ad))
                return true;
        }
        return false;
    }


}
