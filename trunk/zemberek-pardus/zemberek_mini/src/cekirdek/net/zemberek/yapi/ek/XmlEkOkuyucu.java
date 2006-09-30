package net.zemberek.yapi.ek;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.logging.Logger;

import net.zemberek.araclar.XmlYardimcisi;

import org.w3c.dom.Attr;
import org.w3c.dom.Document;
import org.w3c.dom.Element;

/**
 * xml ek dosyasindan ek bilgilerini okur ve ekleri olusturur.
 * User: ahmet
 * Date: Aug 15, 2005
 */
public class XmlEkOkuyucu {

    private static Logger log = Logger.getLogger(XmlEkOkuyucu.class.getName());

    private Map<String, Set<Ek>> ekKumeleri = new HashMap();
    private Map<String, Ek> ekler = new HashMap();

    private final String xmlEkDosyasi;
    private final EkUretici ekUretici;
    private final EkKuralCozumleyici ekKuralCozumleyici;

    private final EkOzelDurumUretici ekOzelDurumUretici;

    public XmlEkOkuyucu(String xmlEkDosyasi,
                        EkUretici ekUretici,
                        EkOzelDurumUretici ekOzelDurumUretici,
                        EkKuralCozumleyici ekKuralCozumleyici) {
        this.xmlEkDosyasi = xmlEkDosyasi;
        this.ekUretici = ekUretici;
        this.ekOzelDurumUretici = ekOzelDurumUretici;
        this.ekKuralCozumleyici = ekKuralCozumleyici;
    }

    public Map<String, Ek> getEkler() {
        return ekler;
    }

    public void xmlOku() throws IOException {
        Document document = XmlYardimcisi.xmlDosyaCozumle(xmlEkDosyasi);

        // kok elemente ulas.
        Element kokElement = document.getDocumentElement();

        ilkEkleriOlustur(XmlYardimcisi.ilkEleman(kokElement, "ekler"));
        ekKumeleriniOlustur(XmlYardimcisi.ilkEleman(kokElement, "ek-kumeleri"));
        ekleriOlustur(XmlYardimcisi.ilkEleman(kokElement, "ekler"));
    }

    /**
     * xml dosyadan sadece eklerin adlarini okuyup Ek nesnelerin ilk hallerinin
     * olusturulmasini saglar.
     *
     * @param eklerElement
     */
    private void ilkEkleriOlustur(Element eklerElement) {
        List<Element> tumEkler = XmlYardimcisi.elemanlar(eklerElement, "ek");
        // tum ekleri bos haliyle uret.
        for (Element ekElement : tumEkler) {
            String ekadi = ekElement.getAttribute("ad");
            if (ekler.containsKey(ekadi))
                exit("Ek tekrari! " + ekadi);
            ekler.put(ekadi, new Ek(ekadi));
        }
    }

    /**
     * xml dosyadan ek kumelerini ayiklar. sonuclar ekKumeleri Map'ina atilir.
     *
     * @param ekKumeleriElement
     */
    private void ekKumeleriniOlustur(Element ekKumeleriElement) {
        List<Element> xmlKumeler = XmlYardimcisi.elemanlar(ekKumeleriElement, "ek-kumesi");
        for (Element ekKumeEl : xmlKumeler) {
            String kumeAdi = ekKumeEl.getAttribute("ad");
            Set<Ek> kumeEkleri = new HashSet();
            List<Element> xmlKumeEkleri = XmlYardimcisi.elemanlar(ekKumeEl, "ek");
            for (Element ekEl : xmlKumeEkleri) {
                String ekAdi = ekEl.getTextContent();
                Ek ek = this.ekler.get(ekAdi);
                if (ek == null) exit("kume eki bulunamiyor!" + ekAdi);
                kumeEkleri.add(ek);
            }
            ekKumeleri.put(kumeAdi, kumeEkleri);
        }
    }


    private void ekleriOlustur(Element eklerElement) {
        List<Element> tumEkler = XmlYardimcisi.elemanlar(eklerElement, "ek");
        for (Element ekElement : tumEkler) {
            String ekAdi = ekElement.getAttribute("ad");
            Ek ek = (Ek) this.ekler.get(ekAdi);
            // uretim kuralini oku ve ekleri uret.
            Attr uretimKurali = ekElement.getAttributeNode("uretim");
            if (uretimKurali == null)
                exit("ek uretim kural kelimesi yok!" + ekAdi);

            ek.setArdisilEkler(ardisilEkleriOlustur(ek, ekElement));
            ek.setEkKuralCozumleyici(ekUretici);
            List<EkUretimBileseni> bilesenler = ekKuralCozumleyici.kuralKelimesiAyristir(uretimKurali.getValue());
            ek.setUretimBilesenleri(bilesenler);
            ek.setOzelDurumlar(ozelDurumlariOku(ekElement));
            ekKuralCozumleyici.ekOzellikleriBelirle(ek, bilesenler);

        }
        log.fine("ek olusumu sonlandi.");
    }

    private List<EkOzelDurumu> ozelDurumlariOku(Element ekElement) {
        List<EkOzelDurumu> ozelDurumlar = new ArrayList();
        //xml ozel durumlarini al.
        List<Element> ozelDurumlarXml = XmlYardimcisi.elemanlar(ekElement, "ozel-durum");
        if (ozelDurumlarXml == null) return Collections.EMPTY_LIST;

        for (Element element : ozelDurumlarXml) {
            String ozelDurumAdi = element.getAttribute("ad");
            EkOzelDurumu oz = ekOzelDurumUretici.uret(ozelDurumAdi);
            Attr uretimKurali = element.getAttributeNode("uretim");

            if (uretimKurali != null) {
                oz.setEkKuralCozumleyici(ekUretici);
                oz.setUretimBilesenleri(ekKuralCozumleyici.kuralKelimesiAyristir(uretimKurali.getValue()));
            }

            List<Element> oneklerElements = XmlYardimcisi.elemanlar(element, "on-ek");
            if (oneklerElements != null) {
                Set<Ek> onekler = new HashSet();
                for (Element onekEl : oneklerElements) {
                    String onekAdi = onekEl.getAttribute("ad");
                    onekler.add(ekler.get(onekAdi));
                }
                oz.setOnEkler(onekler);
            }
            ozelDurumlar.add(oz);
        }
        return ozelDurumlar;
    }

    /**
     * Bir eke iliskin ardisil ekler belirlenir. ardisil ekler
     * a) ek kumelerinden
     * b) normal tek olarak
     * c) dogrudan baska bir ekin ardisil eklerinden kopyalanarak
     * elde edilir.
     * Ayrica eger oncelikli ekler belirtilmis ise bu ekler ardisil ek listeisnin en basina koyulur.
     *
     * @param ekElement :  ek xml bileseni..
     * @return Ek referans Listesi.
     */
    private List<Ek> ardisilEkleriOlustur(Ek anaEk, Element ekElement) {

        Set<Ek> ardisilEkSet = new HashSet();
        Element ardisilEklerEl = XmlYardimcisi.ilkEleman(ekElement, "ardisil-ekler");
        if (ardisilEklerEl == null) return Collections.EMPTY_LIST;

        // tek ekleri ekle.
        List<Element> tekArdisilEkler = XmlYardimcisi.elemanlar(ardisilEklerEl, "aek");
        for (Element element : tekArdisilEkler) {
            String ekAdi = element.getTextContent();
            Ek ek = this.ekler.get(ekAdi);
            if (ek == null) exit(anaEk.ad() + " icin ardisil ek bulunamiyor! " + ekAdi);
            ardisilEkSet.add(ek);
        }

        // kume eklerini ekle.
        List<Element> kumeEkler = XmlYardimcisi.elemanlar(ardisilEklerEl, "kume");
        for (Element element : kumeEkler) {
            String kumeAdi = element.getTextContent();
            Set<Ek> kumeEkleri = ekKumeleri.get(kumeAdi);
            if (kumeEkleri == null) exit("kume bulunamiyor..." + kumeAdi);
            ardisilEkSet.addAll(kumeEkleri);
        }

        //varsa baska bir ekin ardisil eklerini kopyala.
        Attr attr = ardisilEklerEl.getAttributeNode("kopya-ek");
        if (attr != null) {
            final String kopyaEkadi = attr.getValue();
            Ek ek = this.ekler.get(kopyaEkadi);
            if (ek == null) exit(anaEk.ad() + " icin kopyalanacak ek bulunamiyor! " + kopyaEkadi);
            ardisilEkSet.addAll(ek.ardisilEkler());
        }

        List<Ek> ardisilEkler = new ArrayList<Ek>(ardisilEkSet.size());

        //varsa oncelikli ekleri oku ve ardisil ekler listesinin ilk basina koy.
        // bu tamamen performans ile iliskili bir islemdir.
        Element oncelikliEklerEl = XmlYardimcisi.ilkEleman(ekElement, "oncelikli-ekler");
        if (oncelikliEklerEl != null) {
            List<Element> oncelikliEkler = XmlYardimcisi.elemanlar(oncelikliEklerEl, "oek");
            for (Element element : oncelikliEkler) {
                String ekAdi = element.getTextContent();
                Ek ek = this.ekler.get(ekAdi);
                if (ek == null) exit(anaEk.ad() + " icin oncelikli ek bulunamiyor! " + ekAdi);
                if (ardisilEkSet.contains(ek)) {
                    ardisilEkler.add(ek);
                    ardisilEkSet.remove(ek);
                } else log.warning(anaEk.ad() + "icin oncelikli ek:" + ekAdi + " bu ekin ardisil eki degil!");
            }
        }

        ardisilEkler.addAll(ardisilEkSet);
        return ardisilEkler;
    }

    /**
     * ciddi hata durumunda sistmein mesaj vererek yazilimdan cikmasi saglanir.
     *
     * @param mesaj
     */
    private void exit(String mesaj) {
        log.severe("Ek dosyasi okuma sorunu:" + mesaj);
        System.exit(1);
    }

}