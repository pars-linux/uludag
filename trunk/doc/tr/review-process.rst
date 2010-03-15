Paket Gözden Geçirme Süreci
==================================================

Bugzilla destekli paket gözden geçirme (review) süreci:

BUG:COMMENT ile yorum girilen yere aynı zamanda hangi dosyalarını değiştiğini gösteren bir
websvn bağlantısı koymaya karar verdik.

   1 Hata raporu "Paketler/00-Yeni Paket" bileşenine herhangi bir kullanıcı tarafından açılır.
       Bu hata raporu packages@pardus.org.tr adresine atanır ve doğal olarak listeye düşer.

   2 Herhangi bir geliştirici paketle ilgilenmeye karar verir, hatayı kendine atar ve ASSIGNED
       olarak işaretler. Bugzilla'da sadece 'editbugs' grubunda olanlar bu işlemi gerçekleştirebilir.

   3 Eğer paket "Paketler/00-Yeni Paket" bileşeninden gelmiyor ise (Paket geliştiricinin kendi isteği 
        ile ilgilenmeye başladığı bir paket ise): İşlem aşağıda bulunan aşmadan itibaren devam eder.

   4 Geliştirici paketi hazırlar ve kendi playground alanına commit eder.
       BUG:COMMENT aracılığıyla bu bilgi hataya yorum olarak girilir.

   5 Geliştirici paketin hazır olduğunu düşündüğünde playground/review dizininin altına
       kopyalar. Tüm bu değişiklikler BUG:COMMENT aracılığıyla hataya yansıtılır.

   6 Yeni paket ile ilgili olan hata, sahibi tarafından "Review" ürününe alınır. Bu ürüne
       sadece 'editbugs' grubundaki hesaplar atama yapabilecektir.

   7 "Review" ürünü seçildikten sonra bileşen bilgisi girilecektir. Bileşen bilgisi depo bileşenlerini
       yansıtacaktır. Örn: desktop.kde, kernel.default.drivers, vb. İlgili bileşenin ve üst bileşenlerinin
       sorumluları otomatik olarak CC'ye eklenecektir.

   8 Oylama süreci

       8.1 Eğer paketin sahibi, paketin ait olduğu bileşenin ve tüm üst
             bileşenlerinin sorumlusuyla aynı kişiyse, herhangi 2 adet ACK,

       8.2 Eğer paketin sahibi, paketin ait olduğu bileşen ağacında
             herhangi bir sorumluluğa sahip değilse, en az 1 adet bileşen ağacı
             sorumluları tarafından olmak üzere 2 ACK

       olacak şekilde düşünülmüştür.

   9 ACK bilgileri hatalarda yorum olarak bildirilecektir. Yorumlarda "Şu
       sorunlar düzeltildikten sonra OK" gibi ifadeler kullanmaktan
       kaçınılacaktır çünkü bu ifadeler ilgili düzeltmelerin düzgünce yapılıp
       yapılmadığının denetimini zorlaştırmaktadır. Geliştirici, sorunlar
       gerçekten düzeltildikten sonra "ACK" ifadesini yorumuna katacaktır.

   10 Yeterli ACK sayısı elde edildiğinde, paket sahibi paketini ilgili depo
       veya depolara taşıyacak ve hatayı FIXED olarak kapatacakdır.