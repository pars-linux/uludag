Hangi program?
--------------
Masaüstünüzde hangi programların çalıştığını görebilmek için CTRL+ESC tuşlarına veya ALT+F2'den "System Activity" butonuna basmalısınız.

KDE üzerinde hangi uygulamanın  hangi komut ile çalıştığından emin olmak için aşağıda bulunan yolu izleyebiliriz.

    * KDE menü üzerinde ilgili uygulama üzerine sağ tıklayyıp "Add to Panel (Panele ekle)" seçin,
    * Panel üzerine yerleşen ikona sağ tıklayın ve "icon settings (ikon ayarları)" seçin,
    * Uygulama tab'ından komut alanında ne yazdığına bakın. Daha sonra pencereyi kapatın.
    * Tekrar menü üzerinde bulunan ikona sağ tıklayın ve "Bu ikonu sil" seçin, böylece yaptığınız işlemleri geri almış olacaksınız.

Hangi dosya?
------------

Eğer program için hangi komutun çalıştırıldığını biliyorsanız, fakat dosya isminden emin değil iseniz, aşağıda bulunan komutları komut satırından deneyebilirsiniz.

::

    which <komut-adı>

Sonucun ilk satırı aradığınız şey olacaktır.

::

    For example:

    $ which ssh
    /usr/bin/ssh

Hangi pisi paketi?
------------------

Dosya veya dizin adını öğrendikten sonra, bu dosyanın hangi hangi pisi paketine ait olduğunu bulabilirsiniz. Bunun için gerekli komut:

::

  pisi sf <dosya uzantısı>

  For example:

        $ pisi sf /usr/bin/ssh
            /usr/bin/ssh aranıyor
            openssh paketi içinde usr/bin/ssh dosyası var.

Böylece uygulamamnın ait olduğu paketi bulabilir ve hata raporunu bu şekilde düzenleyebilirsiniz.

Kurmadığınız paketler için, packages.pardus.org.tr arama bölümünden dosya uzantısını girip komuta ait doğru paketi bulabilirsiniz.

Bazen hata bir eklenti veya kütüphaneden kaynaklanıyor olabilir, bu durumda yapılması gereken geliştiricinin bu sorunu algılayıp yeniden atama yapmasıdır.
