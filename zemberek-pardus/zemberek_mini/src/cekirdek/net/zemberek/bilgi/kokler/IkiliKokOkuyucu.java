package net.zemberek.bilgi.kokler;

import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.EOFException;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

import net.zemberek.bilgi.KaynakYukleyici;
import net.zemberek.yapi.KelimeTipi;
import net.zemberek.yapi.Kok;
import net.zemberek.yapi.kok.KokOzelDurumBilgisi;
import net.zemberek.yapi.kok.KokOzelDurumu;

/**
 * User: ahmet
 * Date: Jan 15, 2006
 */
public class IkiliKokOkuyucu {

    private DataInputStream dis;
    private KokOzelDurumBilgisi ozelDurumlar;

    public IkiliKokOkuyucu(InputStream is, KokOzelDurumBilgisi ozelDurumlar) {
        dis = new DataInputStream(new BufferedInputStream(is));
        this.ozelDurumlar = ozelDurumlar;
    }

    public IkiliKokOkuyucu(String dosyaAdi, KokOzelDurumBilgisi ozelDurumlar) throws IOException {
        InputStream fis = new KaynakYukleyici("UTF-8").getStream(dosyaAdi);
        dis = new DataInputStream(new BufferedInputStream(fis));
        this.ozelDurumlar = ozelDurumlar;
    }

    /**
     * S�zl�kteki T�m k�kleri okur ve bir ArrayList olarak d�nd�r�r.
     */
    public List<Kok> hepsiniOku() throws IOException {
        ArrayList<Kok> list = new ArrayList<Kok>();
        Kok kok = null;
        while ((kok = oku()) != null) {
            list.add(kok);
        }
        dis.close();
        return list;
    }

    /**
     * �kili (Binary) s�zl�kten bir k�k okur. �a�r�ld�k�a bir sonraki k�k� al�r.
     *
     * @return bir sonraki k�k. E�er okunacak k�k kalmam��sa null
     */
    public Kok oku() throws IOException {

        String icerik = null;
        //kok icerigini oku. eger dosya sonuna gelinmisse (EOFException) null dondur.
        try {
            icerik = dis.readUTF();
        } catch (EOFException e) {
            dis.close();
            return null;
        }
        String asil = dis.readUTF();

        // Tip bilgisini oku (1 byte)
        KelimeTipi tip = KelimeTipi.getTip(dis.read());
        Kok kok = new Kok(icerik, tip);

        if (asil.length() != 0)
            kok.setAsil(asil);

        kok.setKisaltmaSonSeslisi(dis.readChar());

        // �zel durum say�s�n� (1 byte) ve ozel durumlari oku.
        int ozelDurumSayisi = dis.read();
        for (int i = 0; i < ozelDurumSayisi; i++) {
            int ozelDurum = dis.read();
            KokOzelDurumu oz = ozelDurumlar.ozelDurum(ozelDurum);
            kok.ozelDurumEkle(oz);
        }
        int frekans = dis.readInt();
        if (frekans != 0) {
            kok.setFrekans(frekans);
        }
        return kok;
    }
}
