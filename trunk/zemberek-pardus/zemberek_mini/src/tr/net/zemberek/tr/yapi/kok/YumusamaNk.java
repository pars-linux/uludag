package net.zemberek.tr.yapi.kok;

import net.zemberek.yapi.Alfabe;
import net.zemberek.yapi.HarfDizisi;
import net.zemberek.yapi.kok.KokOzelDurumu;

/**
 * 'nk' ile biten baki koklere sert sesli eklendiginde sonraki k yumusak g'ye degil g harfine donusur.
 * 'cenk-cenge' 'denk-dengi' 'Celenk-celenge' gibi.
 */
public class YumusamaNk extends KokOzelDurumu {

    private final HarfDizisi NK;
    private Alfabe alfabe;


    public YumusamaNk(Uretici uretici, Alfabe alfabe) {
        super(uretici);
        this.alfabe = alfabe;
        NK = new HarfDizisi("nk", alfabe);
        yapiBozucu = true;
        sesliEkIleOlusur = true;
    }

    public void uygula(HarfDizisi dizi) {
        if (dizi.aradanKiyasla(dizi.length() - 2, NK))
            dizi.harfDegistir(dizi.length() - 1, alfabe.harf('g'));
    }
}
