package net.zemberek.islemler.cozumleme;

import net.zemberek.yapi.Kelime;

import java.util.LinkedList;


public class BasitKelimeYigini {

    private LinkedList<YiginKelime> yigin = new LinkedList<YiginKelime>();

    public void push(YiginKelime kel) {
        yigin.addFirst(kel);
    }

    public YiginKelime al() {
        return yigin.removeFirst();
    }

    public boolean bosMu() {
        return yigin.isEmpty();
    }

    public void clear() {
        yigin.clear();
    }

    public void koy(Kelime kelime, int ardisilEkSirasi) {
        push(new YiginKelime(kelime, ardisilEkSirasi));
    }

    public static final class YiginKelime {

        private final Kelime kelime;
        private final int ekSirasi;

        public YiginKelime(Kelime kel, int index) {
            this.kelime = kel;
            this.ekSirasi = index;
        }

        public Kelime getKelime() {
            return kelime;
        }

        public int getEkSirasi() {
            return ekSirasi;
        }

        public String toString() {
            return " olusan: " + kelime.icerik().toString()
                    + " sonEk: " + kelime.sonEk().toString()
                    + " ekSira: " + ekSirasi;
        }
    }
}
