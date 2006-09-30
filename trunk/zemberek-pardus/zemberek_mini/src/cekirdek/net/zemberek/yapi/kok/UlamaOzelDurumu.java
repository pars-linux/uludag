package net.zemberek.yapi.kok;

import net.zemberek.yapi.HarfDizisi;

/**
 * Genel amacli ulama ozel durumunu temsil eder. olustugu durumda koke
 * ulancak olan harfdizisini ekler.
 */
public class UlamaOzelDurumu extends KokOzelDurumu {

    private final HarfDizisi ulanacak;

    public UlamaOzelDurumu(Uretici uretici, HarfDizisi ulanacak) {
        super(uretici);
        this.ulanacak = ulanacak;
        yapiBozucu = true;
    }

    public void uygula(HarfDizisi dizi) {
        dizi.ekle(ulanacak);
    }
}
