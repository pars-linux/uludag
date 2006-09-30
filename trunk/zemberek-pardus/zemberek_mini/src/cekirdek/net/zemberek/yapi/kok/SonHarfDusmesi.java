package net.zemberek.yapi.kok;

import net.zemberek.yapi.HarfDizisi;

/**
 * Basitce harf dizisinin son harfini siler.
 */
public class SonHarfDusmesi extends KokOzelDurumu {

    public SonHarfDusmesi(Uretici uretici) {
        super(uretici);
        yapiBozucu = true;
    }

    public void uygula(HarfDizisi dizi) {
        if (dizi.length() > 0)
            dizi.harfSil(dizi.length() - 1);
    }
}
