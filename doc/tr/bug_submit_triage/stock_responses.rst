.. _stock-responses:

Bugzilla Hazır Cevapları
========================

Pardus'u daha iyi bir hale getirmek için Bugzilla isimli hata takip aracı
kullanılmaktadır. Pardus hata takip sisteminde bulunan pek çok hata kaydının,
geliştiriciler tarafından çözülebilmesi için ek bilgilere ihtiyaç duyulmaktadır.

Problemli hata kayıtlarına hızlı bir şekilde cevap verebilmek için, önceki
deneyimlerimizden yararlanarak hazır cevaplar oluşturduk. Bu cevaplar
hata ayıklayıcılara ve geliştiricilere eksik olan bilgileri hızlıca, açık,
kibar ve tutarlı bir şekilde istemelerini sağlayacaktır.


Yetersiz Rapor
--------------

Hata kaydının açıklaması eksikse lütfen "NEEDINFO" anahtar kelimesini ekleyin ve şu
cevabı verin:

::

    Hata bildiriminde bulunduğunuz için teşekkürler. Ne yazık ki, yaşadığınız problemi
    anlayamadık ve tekrarlayamıyoruz. Zamanınız varsa ve hala hatayı tekrarlayabiliyorsanız
    lütfen http://svn.pardus.org.tr/uludag/trunk/doc/tr/bug_submit_triage/bug_and_feature_requests.rst
    adresindekileri okuyun ve bu hata kaydına belgede anlatıldığına benzer şekilde bir
    açıklama ekleyin. Böylece biz de hata hakkında karara varabiliriz. Teşekkürler.

Raporlayıcıya yardımcı olabilecek hataya özgü daha belirgin bilgiler isteyebilirsiniz.


Benzer Raporlar
---------------

Hata kaydı başka bir kaydın aynısıysa, lütfen daha az bilgi içeren kaydı "AYNISI"
olarak işaretleyin ve şu mesajı verin:

::

    Hata bildiriminde bulunduğunuz için teşekkürler. Raporlamış olduğunuz
    hatanın benzeri raporlanmış durumda, fakat bulduğunuz diğer hataları
    lütfen bildirmekten çekinmeyiniz.


Tek hata kaydında birden fazla durum bildirimi
----------------------------------------------

::

    Hata bildiriminde bulunduğunuz için teşekkürler. Hata kaydının uygun olarak takip
    edilebilmesi için, hata kaydı yazım kılavuzunda (https://bugs.pardus.org.tr/page.cgi?id=bug-writing.html)
    söylendiği gibi raporlayıcılar her hata kaydında bir durum bildirmelidir. Görünüşe
    göre bu hata kaydı birden çok durum içeriyor. Zamanınız varsa ve hala hatayı
    (hataları) tekrarlayabiliyorsanız lütfen karşılaştığınız her durum için ayrı birer
    hata kaydı açın. Bu kayıtta tek bir hata kalabilir, bunun için basitçe özeti
    bunu yansıtacak şekilde düzenleyiniz. Yeni hata kayıtlarının numaralarını bu hata
    kaydına yorum olarak ekleyebilirsiniz. Teşekkürler.

Kullanıcılar genellikle hata kayıtlarını ayırmak hakkında daha fazla bilgiye ihtiyaç
duyar, lütfen onlara daha belirli bilgiler verin ve nazik olun.


Yanlış Bileşen
--------------

Hata kaydı yanlış bileşene bildirilmişse, uygun bileşen isimlerini ekleyerek şu mesajı
kullanabilirsiniz:

::

    Hata bildiriminde bulunduğunuz için teşekkürler. Hata kaydı yanlış bileşene
    bildirilmiş görünüyor. Bunun için rapor, <eskibileşen>'den <yenibileşen>'e
    atandı. Bulduğunuz diğer hataları, hata takip sistemimize bildirmekten lütfen
    çekinmeyiniz. Doğru bileşenleri bulmak için şu belgeye bakabilirsiniz:
    http://svn.pardus.org.tr/uludag/trunk/doc/tr/bug_submit_triage/correct_component.rst


Halihazırda düzeltilmiş hatalar
--------------------------------

Hata artık tekrarlanamıyor ise, lütfen hata kaydını "ÇÖZÜLDÜ" olarak işaretleyin ve
şu cevabı verin:

::

    Hata bildiriminde bulunduğunuz için teşekkürler. Ne yazık ki hatayı tekrarlayamıyoruz,
    hata halihazırda çözülmüş olabilir. Paketi güncellemeye ve tekrar test etmeye
    zamanınız varsa, lütfen bunu yapıp sonuçları buraya bildiriniz.


Sonraki kararlı güncelleme ile çözülecek hatalar
------------------------------------------------

Hata, test deposunda çözüldü ve sonraki güncellemeyle kararlı depoya aktarılacaksa,
lütfen kaydı "ÇÖZÜLDÜ" olarak işaretleyin ve şu cevabı verin:

::

    Hata bildiriminde bulunduğunuz için teşekkürler. Bu hata, test deposunda düzeltildi ve
    sonraki kararlı güncellemeyle yayınlanacak. Bulduğunuz diğer hataları bildirmekten veya
    güncellemeden sonra bu hata çözülmediyse bu hatayı tekrar açmaktan çekinmeyiniz.


Üst geliştirici Hataları
------------------------

Hatalar paketlemeyle ilgili değilse, bakıcı hata üzerinde yakın gelecekte çalışmayı
planlamıyorsa ve hatalı ürün kendi hata takip sistemine sahipse, lütfen hata kaydını
"DÜZELTİLMEYECEK" olarak işaretleyin ve şu cevabı verin:

::

    Hata bildiriminde bulunduğunuz için teşekkürler. Bu hata paketlemeyle ilgili bir
    sorundan kaynaklanmıyor. Şu an Pardus geliştiricileri diğer problemleri gidermekle
    meşguller ve üst geliştirici hataları ilgilenmek için zamanları olmayabilir. Hatayı
    uygulamanın yazarlarına (üst geliştiriciye) bildirebilirsiniz.

    Hata takip sistemleri, çoğu üst geliştirici tarafından kullanılmaktadır ve buralara
    bildirilmiş hata kayıtlarına kodu bilen daha çok kişi bakacaktır.

    Hata raporlayacağınız üst geliştirici hata takip sistemi:
    <bağlantı>

    Üst geliştirici hata takip sisteminde açtığınız kaydın bağlantısını buraya
    ekleyebilirsiniz. Lütfen bildirmeyi düşündüğünüz hatanın halihazırda
    üstgeliştirici hata takip sisteminde bildirilmiş olmadığından emin olun.

En Çok Kullanılan Üst Geliştirici Hata Takip Sistemi Listesi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------+-------------------------------------------------------------+
| Gnome       | http://bugzilla.gnome.org/                                  |
+-------------+-------------------------------------------------------------+
| KDE         | http://bugs.kde.org/                                        |
+-------------+-------------------------------------------------------------+
| Mozilla     | https://bugzilla.mozilla.org/                               |
+-------------+-------------------------------------------------------------+
| Freedesktop | http://bugs.freedesktop.org/                                |
+-------------+-------------------------------------------------------------+
| OpenOffice  | http://qa.openoffice.org/issue_handling/project_issues.html |
+-------------+-------------------------------------------------------------+


Benzer Üst Geliştirici Hataları
-------------------------------

Hata, paketlemeyle ilgili bir problemden kaynaklanmıyor ve bu hatanın benzeri üst
geliştirici hata takip sisteminde bildirilmiş ise, lütfen kaydı "DÜZELTİLMEYECEK"
olarak işaretleyin ve şu cevabı verin:

::

    Hata bildiriminde bulunduğunuz için teşekkürler. Bu hatanın benzeri uygulamanın
    yazarlarına bildirilmiş durumda.

    Üst geliştirici hata takip sistemindeki kayda aşağıdaki adresten ek bilgi
    verebilirsiniz:
    <bağlantı>

    Hata kaydındaki gelişmeleri takip etmek için kendinizi hata kaydının haber
    verilecekler kısmına ekleyebilirsiniz.


Sürüm Döngüsünü Tamamlamış Ürünler
----------------------------------

Bir sürüm döngüsünü tamamlamış ise, ona ait hataları aşağıda bulunan cevapla
"DÜZELTİLMEYECEK" olarak işaretleyin:

::

    Hata bildiriminde bulunduğunuz için teşekkürler. Ne yazık ki, önümüzdeki
    Pardus <yeni sürüm ismi> ile Pardus <yolun sonuna gelmiş sürüm ismi> güvenli
    duruma, bir süre sonra da sürüm döngüsünün sonuna gelecek ve şu anki Pardus
    <yolun sonuna gelmiş sürüm ismi> ile ilişkin hata kayıtları geçersiz olacaktır.
    Bu hatayı Pardus <yeni sürüm ismi> ile tekrarlayabiliyorsanız, hata raporunu
    tekrar açıp sürüm bilgilerini güncelleyebilirsiniz. Teşekkürler.


Üst Geliştirici Bakımı Yapılmayan Paketler
-------------------------------------------

Üst geliştirici tarafından uygulamanın bakımı artık yapılmıyor ise, kaydın
çözümü olarak "DÜZELTİLMEYECEK" seçerek şu cevabı verin:

::

    Hata bildiriminde bulunduğunuz için teşekkürler. Üst geliştirici artık bu yazılımın
    bakımını sürdürmüyor. Pardus da destek sağlayamıyor. <üst geliştirici bağlantısı>
    adresinden yazılımın <son tarih> itibariyle güncellenmediğini görebilirsiniz.
    Ne yazık ki, hatanın çözümü için Pardus projesinin yapabileceği hiçbir şey yoktur.


Uygulama Çökmeleri
------------------

Hata bir çöküş nedeniyle oluşuyor ama hata kaydında yığın izi yoksa, şu cevabı verin:

::

    Hata bildiriminde bulunduğunuz için teşekkürler. Fakat çöküşe ait yığın izine
    ihtiyacımız var. Hatanın nedenlerini bir yığın izi olmadan analiz etmek imkansızdır.
    Hata ayıklama sembolleriyle yararlı yığın izi elde etmek hakkında daha fazla bilgi
    için lütfen http://svn.pardus.org.tr/uludag/trunk/doc/tr/bug_submit_triage/stack_traces.rst
    adresine bakın.


Bazı Hatalar İçin Ek Bilgiler
-----------------------------

X Server Hataları
^^^^^^^^^^^^^^^^^

X11 server hataları için bazı dosyalara ihtiyaç duyulabilir, bunları istemek için
şu cevabı kullanın:

::

    Hata bildiriminde bulunduğunuz için teşekkürler. Hata kaydınız kontrol edildi,
    konuyu analiz etmede yardımcı olacak bazı ek bilgilere ihtiyacımız var.

    Lütfen X server yapılandırma dosyasını (/etc/X11/xorg.conf), X server kayıt dosyasını
    (/var/log/Xorg.*.log) ve "dmesg" komutunun çıktısını, hata kaydına üst bölümde yer alan
    "Eklenti gönder" isimli bağlantıyı kullanarak ayrı ayrı ve düz metin (text/plain)
    olarak ekleyin. Teşekkürler.

.. ATI/AMD ve Nvidia Sürücü Hataları
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. KMS/Radeon Hataları
.. ^^^^^^^^^^^^^^^^^^^

**Last Modified Date:** |today|

:Author: Semen Cirit

