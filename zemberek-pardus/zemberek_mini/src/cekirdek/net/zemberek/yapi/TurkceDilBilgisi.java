package net.zemberek.yapi;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Constructor;
import java.util.logging.Logger;

import net.zemberek.bilgi.KaynakYukleyici;
import net.zemberek.bilgi.kokler.AgacSozluk;
import net.zemberek.bilgi.kokler.IkiliKokOkuyucu;
import net.zemberek.bilgi.kokler.Sozluk;
import net.zemberek.islemler.BasitDenetlemeCebi;
import net.zemberek.islemler.DenetlemeCebi;
import net.zemberek.islemler.cozumleme.CozumlemeYardimcisi;
import net.zemberek.yapi.ek.EkYonetici;
import net.zemberek.yapi.kok.KokOzelDurumBilgisi;

/**
 * Bir dil icin gerekli parametrelerin kolay uretimi icin kullanilan fabrika sinifi.
 * Dile ozel siniflara iliskin nesneler reflection ile uretilir. Hangi dilin hangi sinifa
 * sahip oldgusu gibi bilgiler ilklendirme sirasindaki giris parametresi olan DilAyarlari
 * nesnesinden edinilir.
 * <p/>
 * User: ahmet
 * Date: Sep 17, 2006
 */
public class TurkceDilBilgisi implements DilBilgisi {

    private TurkDiliTuru dilTuru;
    private DilAyarlari dilAyarlari;

    private Alfabe alfabe;
    private Sozluk sozluk;
    private DenetlemeCebi cep;
    private CozumlemeYardimcisi yardimci;
    private EkYonetici ekYonetici;
    private KokOzelDurumBilgisi ozelDurumBilgisi;
    private HeceBulucu heceleyici;

    private static Logger logger = Logger.getLogger(TurkceDilBilgisi.class.getName());

    private final String bilgiDizini;

    private final String alfabeDosyaAdi;
    private final String ekDosyaAdi;
    private final String kokDosyaAdi;
    private final String cepDosyaAdi;
    private final String kokIstatistikDosyaAdi;

    /**
     * istenilen dilayarlari nesnesine gore cesitli parametreleri (bilgi dizin adi, kaynak dosyalarin locale
     * uyumlu adlari gibi) olusturur. bilgi dosyalari
     * kaynaklar/<locale>/bilgi/ ana dizini altinda yer almak zorundadir.
     *
     * @param dilAyarlari
     */
    public TurkceDilBilgisi(DilAyarlari dilAyarlari) {

        this.dilAyarlari = dilAyarlari;
        this.dilTuru = dilAyarlari.tur();
        char c = File.separatorChar;
        bilgiDizini = "kaynaklar" + c + dilTuru.iso3Ad() + c + "bilgi" + c;
        alfabeDosyaAdi = dosyaAdiUret("harf", "txt");
        ekDosyaAdi = dosyaAdiUret("ek", "xml");
        kokDosyaAdi = dosyaAdiUret("kokler", "bin");
        cepDosyaAdi = dosyaAdiUret("kelime_cebi", "txt");
        kokIstatistikDosyaAdi = dosyaAdiUret("kok_istatistik", "bin");
    }

    /**
     * kok_<locale>.uzanti dosya adini uretir.
     *
     * @param kok
     * @param uzanti
     * @return olusan kaynak dosyasi adi.
     */
    private String dosyaAdiUret(String kok, String uzanti) {
        return bilgiDizini + kok + '_' + dilTuru.iso3Ad() + '.' + uzanti;
    }

    public Alfabe alfabe() {
        if (alfabe != null) {
            return alfabe;
        } else
            try {
                logger.fine("Alfabe uretiliyor:" + dilTuru);
                Class clazz = dilAyarlari.alfabeSinifi();
                Constructor c = clazz.getConstructor(String.class, TurkDiliTuru.class);
                alfabe = (Alfabe) c.newInstance(alfabeDosyaAdi, dilTuru);
            } catch (Exception e) {
                logger.severe("Alfabe uretilemiyor. muhtemel dosya erisim hatasi.");
                e.printStackTrace();
            }
        return alfabe;
    }

    public EkYonetici ekler() {
        if (ekYonetici != null) {
            return ekYonetici;
        } else {
            alfabe();
            try {
                logger.fine("Ek yonetici uretiliyor:" + dilTuru);
                Class clazz = dilAyarlari.ekYoneticiSinifi();
                Constructor c = clazz.getConstructor(Alfabe.class, String.class);
                ekYonetici = (EkYonetici) c.newInstance(alfabe, ekDosyaAdi);
            } catch (Exception e) {
                logger.severe("ek yonetici sinif uretilemiyor.");
                e.printStackTrace();
            }
        }
        return ekYonetici;
    }

    /**
     * Sozluk, daha dogrusu Kokleri tasiyan agac ve iliskili kok secicileri tasiyan nesneyi uretir
     * Proje gelistirime asamasinda, eger ikili kok-sozluk dosyasi (kokler_xx.bin) dosyasi mevcut
     * degilse once onu uretmeye calisir, daha sonra asil sozluk uretim islemini yapar.
     * Normal kosullarda dagitim jar icerisinde bu dosya yer alacagindan bu islem (bin dosya uretimi) atlanir.
     *
     * @return Sozluk
     */
    public Sozluk kokler() {
    	if (sozluk != null) {
    		return sozluk;
    	} else {
    		if (!new KaynakYukleyici().kaynakMevcutmu(kokDosyaAdi)) {
    			logger.info("binary kok dosyasi bulunamadi.");
    			System.exit(-1);
    		}
    		alfabe();
    		kokOzelDurumlari();
    		logger.fine("Ikili okuyucu uretiliyor:");
    		try {
    			IkiliKokOkuyucu okuyucu = new IkiliKokOkuyucu(kokDosyaAdi, ozelDurumBilgisi);
    			logger.fine("Sozluk ve agac uretiliyor:" + dilTuru);
    			sozluk = new AgacSozluk(okuyucu, alfabe, ozelDurumBilgisi);
    		} catch (IOException e) {
    			e.printStackTrace();
    			logger.severe("sozluk uretilemiyor.");
    		}
    	}
    	return sozluk;
    }

    public KokOzelDurumBilgisi kokOzelDurumlari() {
        if (ozelDurumBilgisi != null) {
            return ozelDurumBilgisi;
        } else {
            alfabe();
            ekler();
            try {
                Class clazz = dilAyarlari.kokOzelDurumBilgisiSinifi();
                Constructor c = clazz.getConstructor(EkYonetici.class, Alfabe.class);
                ozelDurumBilgisi = (KokOzelDurumBilgisi) c.newInstance(ekYonetici, alfabe);
            } catch (Exception e) {
                logger.severe("kok ozel durum bilgi nesnesi uretilemiyor.");
                e.printStackTrace();
            }
        }
        return ozelDurumBilgisi;
    }


    public TurkDiliTuru tur() {
        return dilTuru;
    }

    public DenetlemeCebi cep() {
        if (cep != null) {
            return cep;
        } else {
            try {
                cep = new BasitDenetlemeCebi(cepDosyaAdi);
            } catch (IOException e) {
                logger.warning("cep dosyasina (" + cepDosyaAdi + ") erisilemiyor. sistem cep kullanmayacak.");
                cep = null;
            }
        }
        return cep;
    }

    public HeceBulucu heceBulucu() {
        if (heceleyici != null) {
            return heceleyici;
        } else {
            alfabe();
            try {
                Class clazz = dilAyarlari.heceBulucuSinifi();
                Constructor c = clazz.getConstructor(Alfabe.class);
                heceleyici = (HeceBulucu) c.newInstance(alfabe);
            } catch (Exception e) {
                logger.warning("heceleyici nesnesi uretilemiyor. heceleme islemi basarisi olacak.");
            }
        }
        return heceleyici;
    }

    public CozumlemeYardimcisi cozumlemeYardimcisi() {
        if (yardimci != null) {
            return yardimci;
        } else {
            alfabe();
            ekler();
            kokOzelDurumlari();
            cep();
            try {
                Class clazz = dilAyarlari.cozumlemeYardimcisiSinifi();
                Constructor c = clazz.getConstructor(
                        Alfabe.class,
                        KokOzelDurumBilgisi.class,
                        EkYonetici.class,
                        DenetlemeCebi.class);
                yardimci = (CozumlemeYardimcisi) c.newInstance(alfabe, ozelDurumBilgisi, ekYonetici, cep);
            } catch (Exception e) {
                logger.severe("cozumleme yardimcisi nesnesi uretilemiyor.");
                e.printStackTrace();
            }
        }
        return yardimci;
    }

}
