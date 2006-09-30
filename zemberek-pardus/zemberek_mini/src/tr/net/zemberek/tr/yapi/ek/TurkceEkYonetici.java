package net.zemberek.tr.yapi.ek;

import net.zemberek.yapi.Alfabe;
import net.zemberek.yapi.KelimeTipi;
import net.zemberek.yapi.ek.EkKuralCozumleyici;
import net.zemberek.yapi.ek.TemelEkYonetici;
import net.zemberek.yapi.ek.XmlEkOkuyucu;

import java.io.IOException;

/**
 * Turkiye Turkcesi icin ek islemlerini kontrol eden sinif. Singleton yapisindadir.
 * <p/>
 * User: ahmet
 * Date: Aug 24, 2005
 */
public class TurkceEkYonetici extends TemelEkYonetici  {

    @Override
    protected void ozelEkleriBelirle() {

        iyelikEkleri.add(ek(TurkceEkAdlari.ISIM_SAHIPLIK_BEN_IM));
        iyelikEkleri.add(ek(TurkceEkAdlari.ISIM_SAHIPLIK_SEN_IN));
        iyelikEkleri.add(ek(TurkceEkAdlari.ISIM_SAHIPLIK_BIZ_IMIZ));
        iyelikEkleri.add(ek(TurkceEkAdlari.ISIM_SAHIPLIK_ONLAR_LERI));
        iyelikEkleri.add(ek(TurkceEkAdlari.ISIM_SAHIPLIK_O_I));
        iyelikEkleri.add(ek(TurkceEkAdlari.ISIM_SAHIPLIK_SIZ_INIZ));
        iyelikEkleri.add(ek(TurkceEkAdlari.ISIM_TAMLAMA_I));
        iyelikEkleri.add(ek(TurkceEkAdlari.ISIM_TAMLAMA_IN));

        halEkleri.add(ek(TurkceEkAdlari.ISIM_BELIRTME_I));
        halEkleri.add(ek(TurkceEkAdlari.ISIM_YONELME_E));
        halEkleri.add(ek(TurkceEkAdlari.ISIM_CIKMA_DEN));
        halEkleri.add(ek(TurkceEkAdlari.IMEK_RIVAYET_MIS));
        halEkleri.add(ek(TurkceEkAdlari.IMEK_SART_SE));
        halEkleri.add(ek(TurkceEkAdlari.IMEK_HIKAYE_DI));
        halEkleri.add(ek(TurkceEkAdlari.ISIM_BIRLIKTELIK_LE));

        baslangicEkleri.put(KelimeTipi.ISIM, ek(TurkceEkAdlari.ISIM_YALIN_BOS));
        baslangicEkleri.put(KelimeTipi.SIFAT, ek(TurkceEkAdlari.ISIM_YALIN_BOS));
        baslangicEkleri.put(KelimeTipi.FIIL, ek(TurkceEkAdlari.FIIL_YALIN_BOS));
        baslangicEkleri.put(KelimeTipi.ZAMAN, ek(TurkceEkAdlari.ZAMAN_YALIN_BOS));
        baslangicEkleri.put(KelimeTipi.ZAMIR, ek(TurkceEkAdlari.ZAMIR_YALIN_BOS));
        baslangicEkleri.put(KelimeTipi.SAYI, ek(TurkceEkAdlari.SAYI_YALIN_BOS));
        baslangicEkleri.put(KelimeTipi.SORU, ek(TurkceEkAdlari.SORU_YALIN_BOS));
        baslangicEkleri.put(KelimeTipi.UNLEM, ek(TurkceEkAdlari.UNLEM_YALIN_BOS));
        baslangicEkleri.put(KelimeTipi.EDAT, ek(TurkceEkAdlari.EDAT_YALIN_BOS));
        baslangicEkleri.put(KelimeTipi.BAGLAC, ek(TurkceEkAdlari.BAGLAC_YALIN_BOS));
        baslangicEkleri.put(KelimeTipi.OZEL, ek(TurkceEkAdlari.OZEL_YALIN_BOS));
        baslangicEkleri.put(KelimeTipi.IMEK, ek(TurkceEkAdlari.IMEK_YALIN_BOS));
        baslangicEkleri.put(KelimeTipi.YANKI, ek(TurkceEkAdlari.YANKI_YALIN_BOS));
        baslangicEkleri.put(KelimeTipi.KISALTMA, ek(TurkceEkAdlari.ISIM_YALIN_BOS));
    }

    public TurkceEkYonetici(Alfabe alfabe, String dosya) throws IOException {
        this.alfabe = alfabe;
        XmlEkOkuyucu okuyucu = new XmlEkOkuyucu(
                dosya,
                new EkUreticiTr(alfabe),
                new TurkceEkOzelDurumUretici(alfabe),
                new EkKuralCozumleyici(alfabe));
        okuyucu.xmlOku();
        ekler = okuyucu.getEkler();
        ozelEkleriBelirle();
    }

}
