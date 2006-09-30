package net.zemberek.yapi;

import net.zemberek.tr.yapi.ek.TurkceEkYonetici;
import net.zemberek.tr.yapi.kok.TurkceKokOzelDurumBilgisi;
import net.zemberek.tr.yapi.TurkceHeceBulucu;
import net.zemberek.tr.islemler.TurkceCozumlemeYardimcisi;

import java.util.Locale;
import java.util.Map;
import java.util.HashMap;

/**
 * User: ahmet
 * Date: Jun 23, 2006
 */
public enum TurkDiliTuru {


    TURKIYE("tr"),
    TURKMEN("tm");

    //AZERI("az");
    //KAZAK("kk"),
    //OZBEK("uz"),
    //TATAR("tt"),
    //UYGUR("ug");

    private Locale locale;
    private String iso3Ad;


    TurkDiliTuru(String iso3Ad) {
        this.iso3Ad = iso3Ad;
        this.locale = new Locale(iso3Ad);
    }

    public Locale locale() {
        return locale;
    }

    public String iso3Ad() {
        return iso3Ad;
    }


}
