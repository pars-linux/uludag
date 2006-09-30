package net.zemberek.tr.yapi.kok;

import static net.zemberek.tr.yapi.kok.TurkceKokOzelDurumTipleri.*;
import net.zemberek.yapi.Alfabe;
import net.zemberek.yapi.HarfDizisi;
import net.zemberek.yapi.KelimeTipi;
import net.zemberek.yapi.Kok;
import net.zemberek.yapi.ek.EkYonetici;
import net.zemberek.yapi.kok.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


/**
 * User: ahmet
 * Date: Aug 31, 2006
 */
public class TurkceKokOzelDurumBilgisi extends TemelKokOzelDurumBilgisi implements KokOzelDurumBilgisi {

    private void uret() {
        ekle(SESSIZ_YUMUSAMASI,  new Yumusama(uretici(SESSIZ_YUMUSAMASI)));
        ekle(SESSIZ_YUMUSAMASI_NK,  new YumusamaNk(uretici(SESSIZ_YUMUSAMASI_NK), alfabe));
        ekle(ISIM_SESLI_DUSMESI,  new AraSesliDusmesi(uretici(ISIM_SESLI_DUSMESI)));
        ekle(CIFTLEME, new Ciftleme(uretici(CIFTLEME)));
        ekle(FIIL_ARA_SESLI_DUSMESI, new AraSesliDusmesi(uretici(FIIL_ARA_SESLI_DUSMESI)));
        ekle(KUCULTME, new SonHarfDusmesi(uretici(KUCULTME)));

        Map<String, String> benSenDonusum = new HashMap();
        benSenDonusum.put("ben", "ban");
        benSenDonusum.put("sen", "san");
        ekle(TEKIL_KISI_BOZULMASI,
                new KuralsizKokBozulmasi(uretici(TEKIL_KISI_BOZULMASI), alfabe, benSenDonusum));

        Map<String, String> deYeDonusum = new HashMap();
        deYeDonusum.put("de", "di");
        deYeDonusum.put("ye", "yi");
        ekle(FIIL_KOK_BOZULMASI,
                new KuralsizKokBozulmasi(uretici(FIIL_KOK_BOZULMASI), alfabe, deYeDonusum));

        ekle(TERS_SESLI_EK, new TersSesliEk(uretici(TERS_SESLI_EK),alfabe));

        ekle(SIMDIKI_ZAMAN, new SonHarfDusmesi(uretici(SIMDIKI_ZAMAN)));

        ekle(ISIM_SON_SESLI_DUSMESI, new SonHarfDusmesi(uretici(ISIM_SON_SESLI_DUSMESI).secimlik(true)));

        ekle(SU_OZEL_DURUMU, new UlamaOzelDurumu(uretici(SU_OZEL_DURUMU), new HarfDizisi("yu", alfabe)));

        ekle(ZAMIR_SESLI_OZEL, new UlamaOzelDurumu(uretici(ZAMIR_SESLI_OZEL), new HarfDizisi("n", alfabe)));

        ekle(ISIM_TAMLAMASI, new BosKokOzelDurumu(uretici(ISIM_TAMLAMASI).ekKisitlayici(true)));

        ekle(YALIN, bosOzelDurum(YALIN));
        ekle(EK_OZEL_DURUMU, bosOzelDurum(EK_OZEL_DURUMU));
        ekle(GENIS_ZAMAN, bosOzelDurum(GENIS_ZAMAN));
        ekle(FIIL_GECISSIZ, bosOzelDurum(FIIL_GECISSIZ));
        ekle(KAYNASTIRMA_N, bosOzelDurum(KAYNASTIRMA_N));
        ekle(KESMESIZ, bosOzelDurum(KESMESIZ));
        ekle(TIRE, bosOzelDurum(TIRE));
        ekle(KESME, bosOzelDurum(KESME));
        ekle(OZEL_IC_KARAKTER, bosOzelDurum(OZEL_IC_KARAKTER));
        ekle(ZAMIR_IM, bosOzelDurum(ZAMIR_IM));
        ekle(ZAMIR_IN, bosOzelDurum(ZAMIR_IN));
        ekle(KISALTMA_SON_SESLI, bosOzelDurum(KISALTMA_SON_SESLI));
        ekle(KISALTMA_SON_SESSIZ, bosOzelDurum(KISALTMA_SON_SESSIZ));
    }

    public TurkceKokOzelDurumBilgisi(EkYonetici ekler, Alfabe alfabe) {
        super(ekler, alfabe);
        uret();
    }

    public String[] ozelDurumUygula(Kok kok) {
        //kok icinde ozel durum yok ise cik..
        if (!kok.ozelDurumVarmi())
            return new String[0];

        HarfDizisi hdizi = new HarfDizisi(kok.icerik(), alfabe);

        List degismisIcerikler = new ArrayList(1);

        //ara sesli dusmesi nedeniyle bazen yapay oarak kok'e ters sesli etkisi ozel durumunun eklenmesi gerekir.
        // nakit -> nakde seklinde. normal kosullarda "nakda" olusmasi gerekirdi.
        boolean eskiSonsesliInce = false;
        if (kok.ozelDurumIceriyormu(ISIM_SESLI_DUSMESI))
            eskiSonsesliInce = hdizi.sonSesli().inceSesliMi();

        boolean yapiBozucuOzelDurumvar = false;
        // kok uzerindeki ozel durumlar basta sona taranip ozel durum koke uygulaniyor.
        for (KokOzelDurumu ozelDurum : kok.ozelDurumDizisi()) {
            // kucultme ozel durumunda problem var, cunku kok'te hem kucultme hem yumusama uygulaniyor.
            if (ozelDurum == null) {
                System.out.println("kok = " + kok);
                System.exit(-1);
            }
            if (!ozelDurum.equals(ozelDurum(KUCULTME)))
                ozelDurum.uygula(hdizi);
            if (ozelDurum.yapiBozucumu())
                yapiBozucuOzelDurumvar = true;
        }
        // ara sesli dusmesi durumunda dusen sesi ile dustukten sonra olusan seslinin farkli olmasi durumunda
        // kok'e bir de ters sesli ek ozel durumu ekleniyor.,
        if (kok.ozelDurumIceriyormu(ISIM_SESLI_DUSMESI)
                || kok.ozelDurumIceriyormu(FIIL_ARA_SESLI_DUSMESI)) {
            if (!hdizi.sonSesli().inceSesliMi() && eskiSonsesliInce)
                kok.ozelDurumEkle(ozelDurumlar.get(TERS_SESLI_EK));
        }

        if (yapiBozucuOzelDurumvar)
            degismisIcerikler.add(hdizi.toString());

        if (kok.ozelDurumVarmi() &&
                kok.ozelDurumIceriyormu(KUCULTME) &&
                kok.ozelDurumIceriyormu(SESSIZ_YUMUSAMASI)) {
            HarfDizisi tempDizi = new HarfDizisi(kok.icerik(), alfabe);
            ozelDurum(KUCULTME).uygula(tempDizi);
            degismisIcerikler.add(tempDizi.toString());
        }
        // yani ozel durumlar eklenmis olabileceginden koke ods'u tekrar koke esle.
        return (String[]) degismisIcerikler.toArray(new String[degismisIcerikler.size()]);
    }

    public void ozelDurumBelirle(Kok kok) {
        // eger bir fiilin son harfi sesli ise bu dogrudan simdiki zaman ozel durumu olarak ele alinir.
        // bu ozel durum bilgi tabaninda ayrica belirtilmedigi icin burada kok'e eklenir.  aramak -> ar(a)Iyor
        char sonChar = kok.icerik().charAt(kok.icerik().length() - 1);
        if (kok.tip() == KelimeTipi.FIIL && alfabe.harf(sonChar).sesliMi()) {
            //demek-yemek fiilleri icin bu uygulama yapilamaz.
            if (!kok.ozelDurumIceriyormu(FIIL_KOK_BOZULMASI)) {
                kok.ozelDurumEkle(ozelDurumlar.get(SIMDIKI_ZAMAN));
            }
        }
    }

    public void duzyaziOzelDurumOku(Kok kok, String okunanIcerik, String[] parcalar) {
        for (int i = 2; i < parcalar.length; i++) {

            String ozelDurum = parcalar[i];

            //kisaltma ozel durumunun analizi burada yapiliyor.
            if (ozelDurum.startsWith(KISALTMA_SON_SESLI.kisaAd())) {
                int loc = ozelDurum.indexOf(':');
                if (loc > 0) {
                    String parca = ozelDurum.substring(loc + 1);
                    char sonSesli = parca.charAt(0);
                    if (!alfabe.harf(sonSesli).sesliMi())
                        System.out.println("Hatali kisaltma harfi.. Sesli bekleniyordu." + ozelDurum);
                    kok.setKisaltmaSonSeslisi(sonSesli);
                    if (parca.length() > 1) {
                        kok.ozelDurumEkle(ozelDurumlar.get(KISALTMA_SON_SESSIZ));
                    } else
                        kok.ozelDurumCikar(KISALTMA_SON_SESLI);
                } else {
                    char sonHarf = kok.icerik().charAt(kok.icerik().length() - 1);
                    if (!alfabe.harf(sonHarf).sesliMi()) {
                        kok.setKisaltmaSonSeslisi('e');
                        kok.ozelDurumEkle(ozelDurumlar.get(KISALTMA_SON_SESLI));
                    }
                }
                continue;
            }

            //diger ozel durumlarin elde edilmesi..
            KokOzelDurumu oz = ozelDurum(ozelDurum);
            if (oz != null) {
                kok.ozelDurumEkle(oz);
            } else {
                System.out.println("Hatali kok bileseni" + kok.icerik() + " Token: " + ozelDurum);
            }
        }

        //kisaltmalari ve ozel karakter iceren kokleri asil icerik olarak ata.
        if (kok.tip() == KelimeTipi.KISALTMA || kok.ozelDurumIceriyormu(OZEL_IC_KARAKTER))
            kok.setAsil(okunanIcerik);
    }

    public void kokIcerikIsle(Kok kok, KelimeTipi tip, String icerik) {
        //tip kisaltma ise ya da icerik ozel karakterler iceriyorsa bunu kok'un asil haline ata.
        if (tip.equals(KelimeTipi.KISALTMA))
            kok.setAsil(icerik);
        if (tip.equals(KelimeTipi.FIIL) && (icerik.endsWith("mek") || icerik.endsWith("mak"))) {
            icerik = icerik.substring(0, icerik.length() - 3);
            kok.setIcerik(icerik);
        }
    }
}
