Paket Gözden Geçirme Süreci
===========================

Paket gözden geçirme süreci, Pardus deposuna yeni girecek olan paketlerin
depo politikasına uygun olmalarını amaçlar.

Gözden geçirme süreci, `Pardus Hata Takip Sistemi <http://hata.pardus.org.tr>`_
aracılığıyla aşağıdaki adımlar uygulanarak gerçekleşmektedir.

#. Hata takip sisteminde, gözden geçirme sürecine girecek paket için daha önce
   bildirilmiş bir yeni paket isteği varsa sürece bu hata raporu üzerinden
   başlanır.

#. Paketi hazırlamak isteyen geliştirici, hata raporunu kendisine atar ve hata
   durumunu ATANDI şeklinde değiştirir. Bu işlemi sadece "editbugs" grubuna
   dahil bir Bugzilla kullanıcısı yapabilir.

#. Girilmiş olan hatada, 'Özet' bölümünde paketin adı, 'Ayrıntılar' bölümünde
   paketin pspec.xml dosyasında yazan Açıklama (description) alanı yer almalıdır.
   Paketin depoya alınmasında özel bir neden varsa (depoda var olan bir paket
   için gerekli olması, gözden geçirme sürecindeki başka bir paketin bağımlılığı
   olması vb.) hatanın 'Ayrıntılar' kısmına yazılmalıdır.

#. Paketin katkı depolarına alınması gerekiyor ise, hatanın "Ayrıntılar" bölümünde
   bu durumun açıklanması gerekmektedir.

#. Hata raporunda ürün olarak "Review", bileşen olarak paketin gireceği depo
   bileşeni seçilir. İlgili bileşen sorumluları otomatik olarak CC'ye
   eklenecektir.

#. Paket, gözden geçirme sürecinde bulunan başka bir pakete bağlı ise o paket
   için açılan hataya bağımlı olarak işaretlenir.

#. Paket hazır duruma geldiğinde depoda playground/review dizini altında
   girmesi düşünülen bileşene kopyalanır.

#. Paket üzerinde sonradan yapılacak değişikliklerin SVN açıklamalarına

     BUG:COMMENT:<Hata Numarası>

   şeklinde bir satır eklenerek ilgili hataya yorum olarak iletilmesi sağlanır.

#. Paketin uygun olduğuna karar verilebilmesi için yeterli sayıda ACK alması
   gerekmektedir. ACK'ler, başta ilgili bileşen sorumluları olmak üzere diğer
   geliştiriciler tarafından hata takip sisteminde yorum olarak verilir.

   Süreçin tamamlanması için en az 2 (iki) ACK alınması gerekir. Bu ACK'lerden
   en az biri, ilgili bileşenlerin sorumlularından olmalıdır. Paket sahibinden
   başka bileşen sorumlusu olmadığı durumda herhangi bir geliştirici ACK
   verebilir.

#. Paketi gözden geçirmek isteyen geliştirici, herhangi bir hata bulursa ACK
   vermek için hatanın düzeltilmesini beklemelidir. Şartlı ACK verilmemelidir.

   Örneğin: YANLIŞ: Dosya izinlerini değiştirdikten sonra ACK.
            DOĞRU : Dosya izinlerinin düzenlenmesi gerek.

   Paketçi, ACK için ön koşul olan kriteri yerine getirdikten sonra inceleme
   yapan kişi değişikliğin doğruluğunu kontrol eder ve yorum olarak "ACK"
   yazar.

#. Yeterli sayıda ACK alan paket, sahibi tarafından depoya alınır, review
   dizininden silinir ve hata raporunun durumu KARAR VERİLDİ/ÇÖZÜLDÜ olarak
   değiştirilir.
