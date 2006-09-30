package net.zemberek.yapi.ek;

import net.zemberek.islemler.cozumleme.HarfDizisiKiyaslayici;
import net.zemberek.yapi.HarfDizisi;
import net.zemberek.yapi.Kelime;

/**
 * User: ahmet
 * Date: Aug 26, 2005
 */
public class SonHarfYumusamaOzelDurumu extends EkOzelDurumu {

    public HarfDizisi cozumlemeIcinUret(Kelime kelime, HarfDizisi giris, HarfDizisiKiyaslayici kiyaslayici) {
        HarfDizisi ek = ekUretici.cozumlemeIcinEkUret(kelime.icerik(), giris, uretimBilesenleri);
        // XXXX gibi t�rk�e harf ta��mayan stringler i�in koruma.
        // TODO: Daha do�ru bir y�ntem bulunmal�.
        if(ek == null){
            return null;
        }
        int harfPozisyonu = kelime.icerik().length() + ek.length();
        if (giris.harf(harfPozisyonu).sesliMi())
            return ek;
        return null;
    }

    public HarfDizisi olusumIcinUret(Kelime kelime, Ek sonrakiEk){
        return null;
    }

}
