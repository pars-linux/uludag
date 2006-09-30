package net.zemberek.yapi.kok;

import net.zemberek.yapi.HarfDizisi;

/**
 * son harfi yumusatir. normal sert harf yumusama kurali gecerlidir.
 */
public class Yumusama extends KokOzelDurumu {

    public Yumusama(Uretici uretici) {
        super(uretici);
        sesliEkIleOlusur = true;
        yapiBozucu = true;        
    }

    public void uygula(HarfDizisi dizi) {
        dizi.sonHarfYumusat();
    }

}
