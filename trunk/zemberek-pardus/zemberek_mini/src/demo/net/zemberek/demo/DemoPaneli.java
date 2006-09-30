package net.zemberek.demo;

import net.zemberek.araclar.turkce.YaziIsleyici;
import net.zemberek.yapi.TurkDiliTuru;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.IOException;

/**
 */
public class DemoPaneli {

    private JPanel mainPanel;
    private GirisAlani girisAlani;
    private net.zemberek.demo.CikisAlani cikisAlani = new CikisAlani();
    private DemoYonetici dy;
    private File currentDir = null;
    public static final int MAX_LOAD_STRING_BOY = 32000;


    public DemoPaneli(DemoYonetici dy) {
        this.dy = dy;
        configure();
    }

    public void yaziEkle(String text) {
        girisAlani.setYazi(text);
    }

    public JPanel getMainPanel() {
        return mainPanel;
    }

    public void configure() {
        // ana paneli ve islem dugmelerinin yer alacagi paneli olustur
        mainPanel = new JPanel();
        JPanel buttonPanel = makeButtonPanel();
        // Islem dugmelerini kuzeye yerlestir
        mainPanel.setLayout(new BorderLayout());
        mainPanel.add(buttonPanel, BorderLayout.NORTH);

        //giris ve cikisin pencere buyudugunde ayni ende kalmasi icin onlari ayrica Grid Layout'a
        //sahip bir panele yerlestir. sonucta her ikisinide ana panelin merkezine koy.
        JPanel ioPanel = new JPanel(new GridLayout());
        girisAlani = new GirisAlani(dy.ozelKarakterDizisiGetir());
        ioPanel.add(girisAlani.getMainPanel());
        ioPanel.add(cikisAlani.getMainPanel());
        mainPanel.add(ioPanel, BorderLayout.CENTER);
    }


    public JPanel makeButtonPanel() {
        JPanel pt = new JPanel(new BorderLayout());

        JPanel topPanel = new JPanel(new FlowLayout());

        JPanel centerPanel = new JPanel(new FlowLayout());

        final JComboBox dilCombo = new JComboBox(TurkDiliTuru.values());
        dilCombo.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                TurkDiliTuru dilAdi = (TurkDiliTuru) dilCombo.getSelectedItem();
                dy.dilSec(dilAdi);
                girisAlani.setYazi("");
                cikisAlani.setYazi("");
                girisAlani.ozelKarakterDugmeAlaniOlustur(dy.ozelKarakterDizisiGetir());
            }
        });
        topPanel.add(dilCombo);

        JButton btnLoad = SwingFactory.getRegularButton("Y\u00fckle");
        btnLoad.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent evt) {
                JFileChooser c;
                if (currentDir == null)
                    c = new JFileChooser();
                else
                    c = new JFileChooser(currentDir);

                int rVal = c.showOpenDialog(mainPanel);
                if (rVal == JFileChooser.APPROVE_OPTION) {
                    try {
                        File f = c.getSelectedFile();
                        String yazi = YaziIsleyici.yaziOkuyucu(f.toString());
                        girisAlani.setYazi(yazi);
                        currentDir = f;
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        });

        topPanel.add(btnLoad);

        JButton btnClear;
        btnClear = SwingFactory.getRegularButton("Sil");
        btnClear.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent evt) {
                girisAlani.setYazi("");
                cikisAlani.setYazi("");
            }
        });
        topPanel.add(btnClear);


        JButton btnTurkceTest;
        btnTurkceTest = SwingFactory.getRegularButton("T\u00fcrk\u00e7e Test");
        btnTurkceTest.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent evt) {
                cikisAlani.setYazi(dy.turkceTest(girisAlani.getYazi()));
            }
        });
        topPanel.add(btnTurkceTest);

        pt.add(topPanel, BorderLayout.NORTH);



        JButton btnDenetle;
        btnDenetle = SwingFactory.getRegularButton("Denetle");
        btnDenetle.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent evt) {
                cikisAlani.setYazi(dy.yaziDenetle(girisAlani.getYazi()));
            }
        });
        centerPanel.add(btnDenetle);

        JButton btnCozumle;
        btnCozumle = SwingFactory.getRegularButton("\u00c7\u00f6z\u00fcmle");
        btnCozumle.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent evt) {
                cikisAlani.setYazi(dy.yaziCozumle(girisAlani.getYazi()));
            }
        });
        centerPanel.add(btnCozumle);

        JButton btnDeascii;
        btnDeascii = SwingFactory.getRegularButton("Ascii->Tr");
        btnDeascii.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent evt) {
                cikisAlani.setYazi(dy.asciiToTurkce(girisAlani.getYazi()));
            }
        });
        centerPanel.add(btnDeascii);

        JButton btnascii;
        btnascii = SwingFactory.getRegularButton("Tr->Ascii");
        btnascii.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent evt) {
                cikisAlani.setYazi(dy.turkceToAscii(girisAlani.getYazi()));
            }
        });
        centerPanel.add(btnascii);

        JButton btnHecele;
        btnHecele = SwingFactory.getRegularButton("Hecele");
        btnHecele.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent evt) {
                cikisAlani.setYazi(dy.hecele(girisAlani.getYazi()));
            }
        });
        centerPanel.add(btnHecele);

        JButton btnOner;
        btnOner = SwingFactory.getRegularButton("\u00d6ner");
        btnOner.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent evt) {
                cikisAlani.setYazi(dy.oner(girisAlani.getYazi()));
            }
        });
        centerPanel.add(btnOner);

        JButton btnTemizle;
        btnTemizle = SwingFactory.getRegularButton("Temizle");
        btnTemizle.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent evt) {
                cikisAlani.setYazi(dy.temizle(girisAlani.getYazi()));
            }
        });
        centerPanel.add(btnTemizle);
        pt.add(centerPanel, BorderLayout.CENTER);

        return pt;

    }

}
