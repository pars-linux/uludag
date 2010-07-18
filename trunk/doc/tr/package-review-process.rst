Paket Gözden Geçirme Süreci
===========================

Paket gözden geçirme süreci, Pardus deposuna yeni girecek olan paketlerin
depo politikasına uygun olmalarını amaçlar.

Gözden geçirme süreci, `Pardus Hata Takip Sistemi <http://hata.pardus.org.tr>`_
aracılığıyla aşağıdaki adımlar uygulanarak gerçekleşmektedir.

#. Paket hazır duruma geldiğinde depoda playground/review dizini altında
   girmesi düşünülen bileşene kopyalanır.

#. Paketi hazırlamak isteyen geliştirici, hata kayıt sisteminde daha önceden
   açılmış yeni paket isteği olsa dahi inceleme için yeni hata kaydı açar, hata
   raporunu kendisine atar ve hata durumunu ATANDI şeklinde değiştirir. Bu
   işlemi sadece "editbugs" grubuna dahil bir Bugzilla kullanıcısı yapabilir.

#. Hata raporunda ürün olarak "Review", bileşen olarak paketin gireceği depo
   bileşeni seçilir. İlgili bileşen sorumluları otomatik olarak CC'ye
   eklenecektir.

#. Girilmiş olan hatada, 'Özet' bölümüne paketin tam yolu yazılmalı (ör:
   desktop/toolkit/gtk/gtkimageview), 'Ayrıntılar' bölümünde paketin pspec.xml
   dosyasında yazan Açıklama (description) alanı yer almalıdır.  Paketin depoya
   alınmasında özel bir neden varsa (depoda var olan bir paket için gerekli
   olması, gözden geçirme sürecindeki başka bir paketin bağımlılığı olması vb.)
   hatanın 'Ayrıntılar' kısmına yazılmalıdır.

#. Paket sorumlusunun paketin bakımını sürdürmek istediği depo (contrib, pardus vs.)
   adı tercihen sebebiyle birlikte, hatanın "Ayrıntılar" bölümüne yazılmalıdır.

#. Paket, gözden geçirme sürecinde bulunan başka bir pakete bağlı ise o paket
   için açılan hataya bağımlı olarak işaretlenir.

#. Paket üzerinde sonradan yapılacak değişikliklerin SVN açıklamalarına

     BUG:COMMENT:<Hata Numarası>

   şeklinde bir satır eklenerek ilgili hataya yorum olarak iletilmesi sağlanır.

#. Paketin uygun olduğuna karar verilebilmesi için yeterli sayıda onay alması
   gerekmektedir. Onaylar, başta ilgili bileşen sorumluları olmak üzere diğer
   geliştiriciler tarafından hata takip sisteminde yorum olarak verilir.

   Süreçin tamamlanması için en az 2 (iki) onay alınması gerekir. Bu onaylardan
   en az biri, ilgili bileşenlerin sorumlularından olmalıdır. Paket sahibinden
   başka bileşen sorumlusu olmadığı durumda herhangi bir geliştirici onay
   verebilir.

#. Paketi gözden geçirmek isteyen geliştirici, herhangi bir hata bulursa onay
   vermek için hatanın düzeltilmesini beklemelidir. Şartlı onay verilmemelidir.

   Örneğin: YANLIŞ: Dosya izinlerini değiştirdikten sonra ACK.
            DOĞRU : Dosya izinlerinin düzenlenmesi gerek.

   Paketçi, onay için ön koşul olan kriteri yerine getirdikten sonra inceleme
   yapan kişi değişikliğin doğruluğunu kontrol eder ve onay yorumu olarak "ACK"
   yazar.

#. Yeterli sayıda onay alan paket, sahibi tarafından depoya alınır, review
   dizininden silinir ve hata raporunun durumu KARAR VERİLDİ/ÇÖZÜLDÜ olarak
   değiştirilir.

#. Paket pardus depolarına katıldıktan sonra ve paket gözden geçirme(review) hatası
   kapatıldıktan sonra, paket isteği hatası da kapatılacaktır. KARAR VERİLDİ / ÇÖZÜLDÜ
   mekanizması bu aşamada kullanılabilir. Hem paket isteği hem de paket gözden geçirme
   hatalarını aynı commit mesajıyla kapatmak tercih edilmektedir.
