package net.zemberek.yapi.kok;

import net.zemberek.yapi.HarfDizisi;

/**
 * Basitce harf dizisinin sondan bir onceki harfini siler.
 * User: ahmet
 * Date: Aug 28, 2005
 */
public class AraSesliDusmesi extends KokOzelDurumu {

    public AraSesliDusmesi(Uretici uretici) {
        super(uretici);
        yapiBozucu = true;
    }

    public void uygula(HarfDizisi dizi) {
        if (dizi.length() >= 2)
            dizi.harfSil(dizi.length() - 2);
    }
}
