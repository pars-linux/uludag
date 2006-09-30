/*
 * Created on 07.Mar.2004
 */
package net.zemberek.bilgi.kokler;

import java.util.List;

import net.zemberek.yapi.KelimeTipi;
import net.zemberek.yapi.Kok;

/**
 * Birden fazla sozlukle calisabilmek icin Sozluk arayuzu. Kaynak s�zl�kteki k�saltmalar�n
 * anlamlar�:
 * <pre>
 * #       : Yorum. Bu sat�rlar okuyucular ihmal edilir.
 * IS      : �sim
 * FI      : Fiil
 * SI      : S�fat
 * SA      : Say�
 * OZ      : �zel isim
 * ZA      : Zamir
 * YUM     : Yumu�ama. �rnek: kitap � kitab� (kitap� de�il)
 * DUS     : Harf D��mesi nutuk � nutka (nutuka de�il)
 * TERS    : Ters d�n���m saat � saate (saata de�il)
 * YAL     : Kelime sadece yal�n olarak kullan�l�r
 * GEN     : Geni� zaman istisnas�
 * </pre>
 *
 * @author MDA & GBA
 */
public interface Sozluk {
    /**
     * str seklinde yazilan tum kelime koklerini dondurur. str kokun istisna hali de olabilir.
     *
     * @param str
     * @return kok listesi.
     */
    public List<Kok> kokBul(String str);


    public Kok kokBul(String str, KelimeTipi tip);

    /**
     * sozluge kok ekler.
     *
     * @param kok
     */
    public void ekle(Kok kok);

    /**
     * Bu metod k�kse�ici fabrikas� elde etmek i�in kullan�l�r. Ger�ekleyen s�zl�k s�n�flar� bu
     * metodda kendi K�k Se�ici fabrikas� ger�eklemelerinin bir instancesini geri d�nd�rmelidirler.
     *
     * @return S�zl�k
     * @see AgacSozluk
     */
    public KokBulucuUretici getKokBulucuFactory();

    public KokAgaci getAgac();
}

