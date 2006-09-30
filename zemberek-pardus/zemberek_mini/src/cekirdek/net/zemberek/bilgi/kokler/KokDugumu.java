/*
 * Created on 24.Eki.2004
 */
package net.zemberek.bilgi.kokler;

import net.zemberek.yapi.Kok;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;

/**
 * Kök düğümü sınıfı Kök ağacının yapıtaşıdır. Her düğüm, kökler, eşseli kökler,
 * değişmiş halleri ifade eden bir string ve uygun �ekilde bellek kullanımı için 
 * hazırlanmış özel bir alt düğüm listesi nesnesi taşır.
 * <p/>
 * çeşitli nedenlerle değişikliğe uğrayabilecek olan kökler ağaca eklenirken
 * değişmiş halleri ile beraber eklenirler. Örneğin kitap kökü hem kitab hem de
 * kitap hali ile sözlüğe eklenir, ancak bu iki kelime için oluşan düğüm de
 * aynı kökü gösterirler. Böylece Kitabına gibi kelimeler için kök adayları
 * aranırken kitap köküne erişilmiş olur.
 * <p/>
 * Eş sesli olan kökler aynı düğüme bağlanırlar. Ağacın oluşumu sırasında ilk 
 * gelen kök düğümdeki kök değişkenne, sonradan gelenler de esSesliler listesine 
 * eklenirler. Arama sırasında bu kök te aday olarak döndürülür.
 *
 * @author MDA
 */
public final class KokDugumu {

    private AltDugumListesi altDugumler = null;
    // Her düğüm bir harfle ifade edilir.
    private char harf;
    // eş seslileri taşıyan liste (Kok nesneleri taşır)
    private List<Kok> esSesliler = null;
    // Düğümğn taşıdığı kök
    private Kok kok = null;
    // Kökün değişmiş halini tutan string
    private CharSequence kelime = null;

    public KokDugumu() {
    }

    public KokDugumu(char harf) {
        this.harf = harf;
    }

    public KokDugumu(char harf, CharSequence icerik, Kok kok) {
        this.harf = harf;
        this.kok = kok;
        if (!icerik.equals(kok.icerik())) this.kelime = icerik;
    }

    /**
     * Verilen karakteri taşıyan alt düğümü getirir.
     *
     * @param in
     * @return Eğer verilen karakteri taşıyan bir alt düğüm varsa
     * o düğümü, yoksa null.
     */
    public KokDugumu altDugumGetir(char in) {
        if (altDugumler == null)
            return null;
        else
            return altDugumler.altDugumGetir(in);
    }

    /**
     * Verilen düğümü bu düğüme alt düğüm olarak ekler.
     * Dönüş değeri eklenen düğümdür
     *
     * @param dugum
     * @return Eklenen düğüm
     */
    public KokDugumu addNode(KokDugumu dugum) {
        if (altDugumler == null) {
            altDugumler = new AltDugumListesi();
        }
        altDugumler.ekle(dugum);
        return dugum;
    }

    /**
     * @return tum alt dugumler. dizi olarak.
     */
    public KokDugumu[] altDugumDizisiGetir() {
        if (altDugumler == null) {
            return new KokDugumu[0];
        }
        return altDugumler.altDugumlerDizisiGetir();
    }

    public boolean altDugumVarMi(){
        if (altDugumler == null || altDugumler.size() == 0) return false;
        return true;
    }
    /**
     * Eğer Düğüme bağlı bir kök zaten varsa esSesli olarak ekle, 
     * yoksa sadece kok'e yaz.
     *
     * @param kok
     */
    public void kokEkle(Kok kok) {
        if (this.kok != null) {
            if (esSesliler == null) esSesliler = new ArrayList<Kok>(1);
            esSesliler.add(kok);
        } else {
            this.kok = kok;
        }
    }

    public Kok getKok() {
        return this.kok;
    }

    public List<Kok> getEsSesliler() {
        return esSesliler;
    }

    public CharSequence getKelime() {
        if (kelime != null) return kelime;
        if (kok != null) return kok.icerik();
        return null;
    }

    public void setKelime(CharSequence kelime) {
        this.kelime = kelime;
    }

    /**
     * @return düğüme bağlı kök ve eş seslilerin hepsini bir listeye 
     * koyarak geri döndürür.
     */
    public List<Kok> tumKokleriGetir() {
        if (kok != null) {
            ArrayList<Kok> kokler = new ArrayList<Kok>();
            kokler.add(kok);
            if (esSesliler != null) {
                kokler.addAll(esSesliler);
            }
            return kokler;
        }
        return null;
    }

    /**
     * Verilen collectiona düğüme bağlı tüm kökleri ekler. 
     *
     * @param kokler
     */
    public void tumKokleriEkle(Collection<Kok> kokler) {
        if (kok != null) {
            kokler.add(kok);
            if (esSesliler != null) {
                kokler.addAll(esSesliler);
            }
        }
    }

    public void temizle() {
        this.kok = null;
        this.kelime = null;
        this.esSesliler = null;
    }

    public void kopyala(KokDugumu kaynak) {
        this.kok = kaynak.getKok();
        this.kelime = kaynak.getKelime();
        this.esSesliler = kaynak.getEsSesliler();
    }

    public char getHarf() {
        return harf;
    }

    public void setHarf(char harf) {
        this.harf = harf;
    }

    /**
     * Kök agacindaki düğümlerin alt düğümleri için bu sinifi kullanirlar.
     * Özellikle bellek kullaniminin önemli oldugu Zemberek-Pardus ve OOo 
     * eklentisi gibi uygulamalarda bu yapinin kullanilmasi bellek kazanci 
     * getirmektedir. 
     * Asagidaki sinifta alt dugum sayisi CEP_BUYUKLUGU degerinden
     * az ise sadece CEP_BUYUKLUGU elemanli bir dizi acar. Bu dizi üzerinde 
     * Arama yapmak biraz daha yavas olsa da ortalama CEP_BUYUKLUGU/2 aramada 
     * sonuca erişildiği için verilen ceza minimumda kalir. 
     *
     */
    private static final int CEP_BUYUKLUGU = 3;    
    private final class AltDugumListesi {
        KokDugumu[] dugumler = new KokDugumu[CEP_BUYUKLUGU];
        int index = 0;
        HashMap<Character, KokDugumu> tumDugumler = null;

        /**
         * Verilen düğümü alt düğüm olarak ekler. eger alt düğümlerinin sayisi
         * CEP_BUYUKLUGU degerini asmissa bir HashMap oluşturur
         * @param dugum
         */
        public void ekle(KokDugumu dugum) {
            if (index == CEP_BUYUKLUGU) {
                if (tumDugumler == null) {
                    tumDugumler = new HashMap<Character, KokDugumu>(CEP_BUYUKLUGU + 2);
                    for (int i = 0; i < CEP_BUYUKLUGU; i++) {
                        tumDugumler.put(dugumler[i].getHarf(), dugumler[i]);
                    }
                    dugumler = null;
                }
                tumDugumler.put(dugum.getHarf(), dugum);
            } else {
                dugumler[index++] = dugum;
            }
        }

        /**
         * Verilen karaktere sahip alt düğümü döndürür.
         * @param giris
         * @return ilgili KokDugumu
         */
        public KokDugumu altDugumGetir(char giris) {
            if (dugumler != null) {
                for (int i=0 ; i< index; i++) {
                    if (dugumler[i].getHarf() == giris) {
                        return dugumler[i];
                    }
                }
                return null;
            } else {
                return tumDugumler.get(giris);
            }
        }

        /**
         * Alt düğümleri dizi olarak döndürür.
         * @return KokDugumu[] cinsinden alt düğümler dizisi
         */
        public KokDugumu[] altDugumlerDizisiGetir() {
            if (dugumler != null){
                return dugumler;
            }
            else{
                return tumDugumler.values().toArray(new KokDugumu[tumDugumler.values().size()]);
            }
        }
        
        public int size(){
            if (dugumler != null){
                return index;
            } else {
                return tumDugumler.size();
            }
        }
    }
    
}