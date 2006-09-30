package net.zemberek.yapi.kok;

import net.zemberek.yapi.HarfDizisi;
import net.zemberek.yapi.Alfabe;
import net.zemberek.yapi.ek.EkYonetici;
import net.zemberek.yapi.kok.KokOzelDurumu;
import net.zemberek.tr.yapi.ek.TurkceEkYonetici;
import net.zemberek.tr.HarfDizisiUretici;

import java.util.HashMap;
import java.util.Map;

/**
 * kuralsiz kok bozulmalarini temsil eder.
 * uretim parametresi olarak gelen Map icerisinde hangi kelimenin hangi kelimeye
 * donusecegi belirtilir.
 * ornegin
 * demek->diyen icin de->ye donusumu, ben->bana icin ben->ban donusumu.
 */
public class KuralsizKokBozulmasi extends KokOzelDurumu {

    private Map<String, String> kokDonusum;
    private Alfabe alfabe;

    public KuralsizKokBozulmasi(Uretici uretici, Alfabe alfabe, Map<String, String>kokDonusum) {
        super(uretici);
        this.kokDonusum = kokDonusum;
        this.alfabe = alfabe;
        yapiBozucu = true;

    }

    public void uygula(HarfDizisi dizi) {
        String kelime = (String) kokDonusum.get(dizi.toString());
        if (kelime != null) {
            dizi.sil();
            dizi.ekle(new HarfDizisi(kelime, alfabe));
        }
    }
}
