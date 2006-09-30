package net.zemberek.yapi;

import java.util.Map;

/**
 * Bir dilin gerceklenmesi sirasinda kullanilaca sinif ve cesitli bilgilere erisimi saglar.
 * User: ahmet
 * Date: Sep 20, 2006
 */
public interface DilAyarlari {

    Class alfabeSinifi();

    Class ekYoneticiSinifi();

    Class heceBulucuSinifi();

    Class kokOzelDurumBilgisiSinifi();

    Class cozumlemeYardimcisiSinifi();

    String[] duzYaziKokDosyalari();

    /**
     * Duz yazi ile belirtilen kok dosyalarinda kokun tipinin hangi kelime ile ifade
     * edilecegi bir Map icerisinde belirtilir.
     * @return ad-tip ikililerini tasiyan Map
     */
    Map<String, KelimeTipi> kelimeTipiAdlari();

    TurkDiliTuru tur();

}
