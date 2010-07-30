Hata Ayıklamaya Hazırlık
========================

Hata Seçimi
~~~~~~~~~~~

* Hata ayıklama ürün veya bileşen bazında yapılmaktadır. Pardus Hata sisteminde bulunan bileşenler ve üzerinde bulunan hatalar için bkz.
* Contribute/Katkıcılar sınıfı ve Pardus Services/Pardus Servisleri ürünü dışında bulunan hatalar hata ayıklama sürecine dahildir.
* Hazır hata yorumları hata ayıklayıcılar için çok önemlidir. (bkz. stock_responses.rst)

Bugzilla'yı Anlamak
~~~~~~~~~~~~~~~~~~~

    * Hata takip döngüsü bug_cycle.rst bkz.

Yeni Hataları Ayıklarken Kullanılan Ön Denetim Listesi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bu ön denetim listesi NEW/YENİ olarak işaretlenen hatalar için geçerlidir.

#. Raporlanan hata gerçekten bir hata mı?

    * Bazı durumlarda raporlayıcı yazılım kurulum veya kullanımı konusunda yardım almak amacı ile hata kaydı girmiş olabilir. Bu hata kayıtları hata veya yeni özellik isteği değildir. Bu gibi bir durum ile karşılaşıldığı zaman kibar bir şekilde kullanıcı listelerine ve forumlara yönlendirerek yorum yapılmalı ve hata CLOSED/KAPATILDI INVALID/GEÇERSİZ olarak işaretlenmelidir.
    * Yeni paket isteklerinin önem derecesi Küçük/Low olarak işaretlenmelidir.
    * Yeni özellik istekleri FutureFeature anahtarı ile işaretlenmelidir.

#. Hata doğru ürün ve bileşene atanmış durumda mı?

    * Teknik yardım almak için doğru bileşen bulma belgesini okuyunuz. (correct_component.rst)
    * Teknik yardımlar doğrultusunda hatanın yanlış üründe olduğu ortaya çıkar ise, hatanın ürün ve bileşenini değiştirilir.
    * Bazı durumlarda hatanın kaynak koduna bakmadan bileşenini seçebilmek mümkün olmamaktadır, bu gibi durumlarda hatanın atanmış olduğu geliştiriciden yardım alınmalıdır.
    * Genel bilşeni ilk sıralarda bulunduğu için üzerine bir çok hata atanmaktadır, bu bileşen üzerinde bulunan hatalar iyi bir şekilde ayıklanmalı ve mümkünse hata bu bileşen üzerinde bırakılmamalıdır.

#. Hatanın aynısı daha önce raporlanmış mı?

    * Öyle ise, en az açıklayıcı olan hata, en iyi açıklaması yapılmış olan hata numarası eklenerek, CLOSED/KAPATILDI DUPLICATE/AYNISI olarak işaretlenir ve ilgili stok yorum yapılır.
    * Eğer hatanın başka bir hatanın aynısı olduğu açık değil ise, raporlayıcı için açıklanmalıdır.
    * Yardım için finding_duplicates.rst, ya da kısaca:
          * `En sık raporlanan hataları <http://bugs.pardus.org.tr/duplicates.cgi>_`. gözden geçirin.
          * Aynı bileşen üzerine atanmış olan hataları inceleyin.
          * Farklı bileşenlerde bulunabilecek aynı hatalar için arama sayfası özet bölümünü kullanarak, benzerlikler bulmaya çalışın.
          * Eğer bu hata bir hataya bağlı veya bu hata başka hatalara bağımlı ise bu durumu da göz önünde bulundurunuz.

#. Birbirine bağlı olan hatalar mı var?

    * Bir hatanın çözümü diğer hatanın çözümüne yardımcı oluyor veya tam tersi ise, her iki hataya da açıklama yaparak durumu açıklayın.
    * Eğer bu durumdan kesin emin iseniz, diğer bir değişle bir hatanın çözümü diğer bir hatanın çözülmesine kesinlikle bağlı ise, hataya bağımlı olan diğer hatanın numarasını "Engellediği hatalar" kısmına girmelisiniz.

#. Bir hata raporunda birden fazla problemden mi bahsediliyor?

    * Bu durum ile ilgili stok yorumu göderiniz.

#. Geliştiricinin hatayı tekrarlaması, tanımlaması ve çözümlemesi için yeterli bilgi var mı?

    * Eğer yok ise,
          * Raporlayan kişiden geliştiricinin ihtiyacı olacak bilgileri isteyin, bunu isterken nazik ve kibar olmaya çalışın. Hatanın durumunu YENİ olarak bırakın ve anahtar kelime olarak "NEEDINFO" girin.
          * Hataya kendi yorumunuzu katın. Bu yorum genellikle hatayı verilen bilgiler doğrultusunda tekrar etmeye çalışılarak edinilebilir. Ayrıca hatada bir ek bulunuyor ise bu ek doğrultusunda da yorumda bulunablir.
    * Hangi tip hatalar için hangi bilgilerin gerekebileceğine Hata ve Özellik Bildirimleri belgesini incelenebilir:
          * Hatayı tekrarlamak için tüm adımlar doğru olarak açıklanmış mı?
          * Hata veya uyarıların çıktıları ek olarak eklenmiş mi?
          * Bileşen için gerekli olabilecek log, konfigürasyoni, sorun giderme dosyaları eklenmiş mi?
          * Eğer bir çökme söz konusu ise "stack trace" eklenmiş mi?

#. Özet hataya referans olabiliyor mu?

    * Özet eğer hatadan uzak, yetersiz veya kafa karıştırıcı ise hatanın başlığını değiştirebilirsiniz.
    * Bunu yaparken lütfen raporlayan kişinin amacını değiştirmeye çalışmayınız.
