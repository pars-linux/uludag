package net.zemberek.yapi.ek;

import net.zemberek.islemler.cozumleme.HarfDizisiKiyaslayici;
import net.zemberek.yapi.HarfDizisi;
import net.zemberek.yapi.Kelime;

import java.util.ArrayList;
import java.util.List;

/**
 * Ek sinifi icerisinde eke ozel bilgiler, o ekten sonra gelebilecek eklerin listesi
 * ve o eke ozel ozel durumlar yer alir.
 * User: aakin
 * Date: Feb 15, 2004
 */
public class Ek {

    //bu ekten sonra elebilecek eklerin listesi.
    private List<Ek> ardisilEkler = new ArrayList<Ek>();

    private String ad;

    //ekin sesli ile baslayip baslayamayacagini belirler. bu bilgi otomatik olarak ek olusum kurallarina
    // gore baslangicta belirlenir.
    private boolean sesliIleBaslayabilir = false;

    //kurallara gore ek olusumunu beliler. dile gore farkli gerceklemeleri olabilir.
    private EkUretici ekUretici;

    //bu ekin uretim kullarinin listesi.
    private List<EkUretimBileseni> uretimBilesenleri;

    //bu eke iliskin ozel durumlar.
    private List<EkOzelDurumu> ozelDurumlar = new ArrayList<EkOzelDurumu>(1);

    private boolean sonEkOlamaz=false;


    public HarfDizisi cozumlemeIcinUret(
            Kelime kelime,
            HarfDizisi giris,
            HarfDizisiKiyaslayici kiyaslayici) {

        for (EkOzelDurumu ozelDurum : ozelDurumlar) {
            HarfDizisi ozelDurumSonucu = ozelDurum.cozumlemeIcinUret(kelime, giris, kiyaslayici);
            if (ozelDurumSonucu != null)
                return ozelDurumSonucu;
        }
        return ekUretici.cozumlemeIcinEkUret(kelime.icerik(), giris, uretimBilesenleri);
    }

    public HarfDizisi olusumIcinUret(
            Kelime kelime,
            Ek sonrakiEk) {
        for (EkOzelDurumu ozelDurum : ozelDurumlar) {
            HarfDizisi ozelDurumSonucu = ozelDurum.olusumIcinUret(kelime, sonrakiEk);
            if (ozelDurumSonucu != null)
                return ozelDurumSonucu;
        }
        return ekUretici.olusumIcinEkUret(kelime.icerik(), sonrakiEk, uretimBilesenleri);
    }

    public void setOzelDurumlar(List<EkOzelDurumu> ozelDurumlar) {
        this.ozelDurumlar = ozelDurumlar;
    }

    public boolean ardindanGelebilirMi(Ek ek) {
        return ardisilEkler.contains(ek);
    }

    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        final Ek ek = (Ek) o;

        if (ad != null ? !ad.equals(ek.ad) : ek.ad != null) return false;

        return true;
    }

    public int hashCode() {
        return (ad != null ? ad.hashCode() : 0);
    }

    public boolean sesliIleBaslayabilirMi() {
        return sesliIleBaslayabilir;
    }

    public String toString() {
        return ad;
    }

    public Ek(String name) {
        this.ad = name;
    }

    public String ad() {
        return ad;
    }

    public Ek getArdisilEk(int ardisilEkSirasi) {
        if (ardisilEkSirasi < ardisilEkler.size())
            return ardisilEkler.get(ardisilEkSirasi);
        return null;
    }

    public boolean OzelEkOlustur(Kelime ozelKelime) {
        return false;
    }

    public List<Ek> ardisilEkler() {
        return ardisilEkler;
    }

    public void setArdisilEkler(List ardisilEkler) {
        this.ardisilEkler = ardisilEkler;
    }

    public void setSesliIleBaslayabilir(boolean sesliIleBaslayabilir) {
        this.sesliIleBaslayabilir = sesliIleBaslayabilir;
    }

    public void setEkKuralCozumleyici(EkUretici ekUretici) {
        this.ekUretici = ekUretici;
    }

    public void setUretimBilesenleri(List<EkUretimBileseni> uretimBilesenleri) {
        this.uretimBilesenleri = uretimBilesenleri;
    }

    public boolean sonEkOlamazMi() {
        return sonEkOlamaz;
    }

    public void setSonEkOlamaz(boolean sonEkOlamaz) {
        this.sonEkOlamaz = sonEkOlamaz;
    }

}
