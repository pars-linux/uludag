package net.zemberek.yapi.ek;

import net.zemberek.yapi.Alfabe;
import net.zemberek.yapi.TurkceHarf;

import java.util.*;
import java.util.logging.Logger;

/**
 * Konfigurasyon dosyasindan okunan ek uretim kurallairnin cozumlenmsi islemi bu sinif ile
 * gerceklestirilir. Farkli turk dilleri icn yeni bir uretim kurali gerekirse bu sinifin ona
 * gore degisitirlmesi gerekir.
 * User: ahmet
 * Date: Jun 18, 2006
 */
public class EkKuralCozumleyici {

    private static Logger log = Logger.getLogger(EkKuralCozumleyici.class.getName());
    private Alfabe alfabe;

    // ek uretim kural kelimesinde kullanilan parcalarin dilbilgisi kurali karsiliklarini tutan tablo.
    private static final Map<String, EkUretimBileseni.UretimKurali> kuralTablosu = new HashMap();

    static {
        kuralTablosu.put("(A)", EkUretimBileseni.UretimKurali.SESLI_AE);
        kuralTablosu.put("(I)", EkUretimBileseni.UretimKurali.SESLI_IU);
        kuralTablosu.put("(E)", EkUretimBileseni.UretimKurali.SESLI_AA);
        kuralTablosu.put("(Y)", EkUretimBileseni.UretimKurali.SESSIZ_Y);
        kuralTablosu.put("?", EkUretimBileseni.UretimKurali.KAYNASTIR);
        kuralTablosu.put("^", EkUretimBileseni.UretimKurali.SERTLESTIR);
    }

    private final Set<String> sesliKurallari =
            new HashSet(Arrays.asList(new String[]{"(A)", "(I)", "(E)", "(Y)"}));


    public EkKuralCozumleyici(Alfabe alfabe) {
        this.alfabe = alfabe;
    }

    /**
     * bazi ek ozellikleri konfigurasyon dosyasinda yer almaz, ekler okunduktan sonra
     * wk vw bilesenlere gore otomatik olarak belirlenir.
     * @param ek
     * @param bilesenler
     */
    public void ekOzellikleriBelirle(Ek ek, List<EkUretimBileseni> bilesenler) {
        for (int i = 0; i < bilesenler.size(); i++) {
            EkUretimBileseni uretimBileseni = bilesenler.get(i);
            TurkceHarf harf = uretimBileseni.harf();
            if (i == 0 || (i == 1 && bilesenler.get(0).kural() == EkUretimBileseni.UretimKurali.KAYNASTIR)) {

                if (harf.sesliMi())
                    ek.setSesliIleBaslayabilir(true);
                switch (uretimBileseni.kural()) {
                    case SESLI_AA:
                    case SESLI_AE:
                    case SESLI_IU:
                        ek.setSesliIleBaslayabilir(true);
                        break;
                }
            } else {
                break;
            }
        }
    }


    /**
     * Xml dosyadan okunan ek olusum kural kelimesi cozumlenerek
     * EkUretimBileseni listesine donusturulur. Bu bilgi bir ekin nasil uretilecegini ifade eder.
     *
     * @param uretimKuralStr
     * @return ek uretim bilesenleri listesi.
     */
    public List<EkUretimBileseni> kuralKelimesiAyristir(String uretimKuralStr) {
        if (uretimKuralStr == null || uretimKuralStr.length() == 0)
            return Collections.EMPTY_LIST;
        // temizle
        uretimKuralStr = uretimKuralStr.replaceAll("[ ]", "");
        List<EkUretimBileseni> uretimBilesenleri = new ArrayList();

        // gelen kurali + isaretini goz onune alarak parcalara ayir.
        String[] parcalar = uretimKuralStr.split("[+]");

        for (String parca : parcalar) {
            log.finer("parca = " + parca);

            //uretim kuralinin normal harf oldugunu varsayiyirouz basta.
            EkUretimBileseni token;
            TurkceHarf harf;

            // parcanin sesli uretim kurali olup olmadigina bak.
            if (sesliKurallari.contains(parca)) {
                token = new EkUretimBileseni(kuralTablosu.get(parca), Alfabe.HARF_YOK);
            } else if (parca.length() > 1) {
                String kural = parca.substring(0, 1);
                harf = alfabe.harf(parca.charAt(1));
                if (kuralTablosu.get(kural) == null)
                    log.severe("Hatali uretim kurali:" + kural);
                token = new EkUretimBileseni(kuralTablosu.get(kural), harf);
            } else {
                token = new EkUretimBileseni(EkUretimBileseni.UretimKurali.HARF, alfabe.harf(parca.charAt(0)));
            }
            log.finer("uretim bileseni:" + token);
            uretimBilesenleri.add(token);
        }
        return uretimBilesenleri;
    }
}
