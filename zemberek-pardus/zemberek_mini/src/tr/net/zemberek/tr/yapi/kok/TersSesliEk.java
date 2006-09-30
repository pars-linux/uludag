package net.zemberek.tr.yapi.kok;

import net.zemberek.yapi.HarfDizisi;
import net.zemberek.yapi.Alfabe;
import net.zemberek.yapi.ek.Ek;
import net.zemberek.yapi.kok.KokOzelDurumu;

/**
 */
public class TersSesliEk extends KokOzelDurumu {

    Alfabe alfabe;

    public TersSesliEk(Uretici uretici, Alfabe alfabe) {
        super(uretici);
        yapiBozucu = true;
        this.alfabe = alfabe;
    }

    /**
     * en son kalin sesli harfi bulup onu ince formu ile degistirir.
     * ornegin saat -> saAt haline donusur. ince a harfi icin TurkceAlfabe sinifini inceleyin
     *
     * @param dizi
     */
    public void uygula(HarfDizisi dizi) {
        for (int i = dizi.length() - 1; i >= 0; i--) {
            if (!dizi.harf(i).inceSesliMi())
                dizi.harfDegistir(i, alfabe.kalinSesliIncelt(dizi.harf(i)));
        }
    }

    public boolean olusabilirMi(Ek ek) {
        return true;
    }
}
