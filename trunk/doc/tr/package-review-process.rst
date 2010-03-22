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

#. Paketin uygun olduğuna karar verilebilmesi için yeterli sayıda oy alması
   gerekmektedir. Oylar, başta ilgili bileşen sorumluları olmak üzere diğer
   geliştiriciler tarafından hata takip sisteminde yorum olarak verilir.

   Süreçin tamamlanması için en az 2 (iki) oy alınması gerekir. Bu oylardan
   en az biri, ilgili bileşenlerin sorumlularından olmalıdır. Paket sahibinden
   başka bileşen sorumlusu olmadığı durumda herhangi bir geliştirici oy
   verebilir.

#. Paketi gözden geçirmek isteyen geliştirici, herhangi bir hata bulursa oy
   vermek için hatanın düzeltilmesini beklemelidir. Şartlı oy verilmemelidir.

#. Yeterli sayıda oy alan paket, sahibi tarafından depoya alınır ve hata
   raporunun durumu KARAR VERİLDİ/ÇÖZÜLDÜ olarak değiştirilir.
