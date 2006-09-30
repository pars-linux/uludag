package net.zemberek.tr.yapi;

import net.zemberek.tr.islemler.TurkceCozumlemeYardimcisi;
import net.zemberek.tr.yapi.ek.TurkceEkYonetici;
import net.zemberek.tr.yapi.kok.TurkceKokOzelDurumBilgisi;
import net.zemberek.yapi.Alfabe;
import net.zemberek.yapi.DilAyarlari;
import net.zemberek.yapi.KelimeTipi;
import net.zemberek.yapi.TurkDiliTuru;

import java.util.HashMap;
import java.util.Map;

/**
 * User: ahmet
 * Date: Sep 20, 2006
 */
public class TurkiyeTurkcesi implements DilAyarlari {

   public TurkDiliTuru tur() {
       return TurkDiliTuru.TURKIYE;
   }

    public Class alfabeSinifi() {
        return Alfabe.class;
    }

    public Class ekYoneticiSinifi() {
        return TurkceEkYonetici.class;
    }

    public Class heceBulucuSinifi() {
        return TurkceHeceBulucu.class;
    }

    public Class kokOzelDurumBilgisiSinifi() {
        return TurkceKokOzelDurumBilgisi.class;
    }

    public Class cozumlemeYardimcisiSinifi() {
        return TurkceCozumlemeYardimcisi.class;
    }

    public String[] duzYaziKokDosyalari() {
        return new String[]{
                "kaynaklar/tr/bilgi/duzyazi-kilavuz.txt",
                "kaynaklar/tr/bilgi/kisaltmalar.txt",
                "kaynaklar/tr/bilgi/bilisim.txt",
                "kaynaklar/tr/bilgi/kisi-adlari.txt"};
    }

    public Map<String, KelimeTipi> kelimeTipiAdlari() {
        Map<String, KelimeTipi> tipMap = new HashMap();
        tipMap.put("IS", KelimeTipi.ISIM);
        tipMap.put("FI", KelimeTipi.FIIL);
        tipMap.put("SI", KelimeTipi.SIFAT);
        tipMap.put("SA", KelimeTipi.SAYI);
        tipMap.put("YA", KelimeTipi.YANKI);
        tipMap.put("ZA", KelimeTipi.ZAMIR);
        tipMap.put("SO", KelimeTipi.SORU);
        tipMap.put("IM", KelimeTipi.IMEK);
        tipMap.put("ZAMAN", KelimeTipi.ZAMAN);
        tipMap.put("HATALI", KelimeTipi.HATALI);
        tipMap.put("EDAT", KelimeTipi.EDAT);
        tipMap.put("BAGLAC", KelimeTipi.BAGLAC);
        tipMap.put("OZ", KelimeTipi.OZEL);
        tipMap.put("UN", KelimeTipi.UNLEM);
        tipMap.put("KI", KelimeTipi.KISALTMA);
        return tipMap;
    }
}
