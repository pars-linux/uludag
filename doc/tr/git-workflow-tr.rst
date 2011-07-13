Pardus için Git Kullanımı
=========================

Genel Kurallar
--------------

* Master branch bütün özelliklerin ve gelişmelerin olduğu ana hat olacak.
* Gelişme ve sürüm dalları bu hat üzerinden yapılacak.
* Master branch daki kodlar her zaman için tam, test edilmiş ve sürüm çıkarmaya
hazır halde bulunacaktır.
* Master branch hiç bir zaman, ister küçük ister büyük değişikliklere
kapatılamaz. Gelişime kapatma işlemi release branch da gerçekleşir.
* Release branch gelişmeye kapalı olduğu halde hata çözümü gerçekleş(ebil)ir.
Çözülen hatalar master branch a merge edilir.
* Geliştirme işlemi, feature branch da gerçekleşir.
* Geliştiriciler feature branch ı istedikleri sekilde kullanabilirler fakat
master breanch a birleştirme işlemi için kodun tam, test edilmiş ve review
edilmiş olması gerekir.
* Integration branch daha cok gelişmiş projeler için kullanılır. Birbirinden
bağımsız bir çok özelliği entegre etme, test etme ve gözden geçirme işlemi
için gerekebilir.
* Integration branch da bilinen kırıklıklar yer almaması gerekir.
* Integration branch, master branch a merge edilmez. Entegre ve test bitince
bu özellikler direk kendi dallarından master branch a merge edilir.
* Local çalışıldıktan sonra, sunucuya push etmeden önce, rebase edilmelidir.
Bu işlem, değişiklikleri bir patch gibi olmasını sağlar.
* Remote branch lar, çakışma olmaması için hiç bir zaman rebase
edilmemelidir.
* Bütün geliştiriciler kişisel dallarını kısa zaman aralıkları içinde
sunucuya push etmeliler ki herkes görsün.

Örnek Uygulama Geliştirme Aşamaları:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Leaf Uygulamaya Yeni Özellik Eklemek
------------------------------------

* Master branch dan clone ya da pull edilir.
* Yeni bir yerel veya uzak özellik dalı (tek veya çok geliştiriciye göre) 
yaratır. Checkout edilir.
* Bu feature branch a commit edilir.
    Tamamlanınca:
* Master branch a gore rebase edilir.
* Degisiklikleri Review aracına push edilir.
* İncelemesi gereken kisi inceler.
    Onaylanırsa:
* Master branch e merge edilir ve bu dal silinir.
    Reddedilirse:
Onaylanincaya kadar düzeltmeler yapılır ve tekrardan rebase edilir.

Core application a yeni bir özellik eklemek
-------------------------------------------

* Master branch dan clone ya da pull edilir.
* Yeni bir uzak özellik dalı yaratır.
* Checkout edilir.
    Tamamlaninca:
* Integration dalının bakıcısı uyarılır.
* Bu özellik integration a merge edilir.
* Bir cok geliştirici integration dalında test eder.
    Testlerden geçerse:
* Geliştirici degisiklikleri review aracına push eder.
* İncelemesi gereken kisi inceler.
    Onaylanırsa:
* Master branch e merge edilir.
    Küçük şeylerden dolayı reddedilirse:
* Onaylanincaya kadar düzeltmeler yapılır ve tekrardan rebase edilir.
    Büyük problemler varsa:
* Düzeltmeler yapılır, test edilir ve integration evresinden tekrar geçer.

Sosyal Git Akışı
----------------

Geliştiriciler kendilerine atanan olayları çözdükten sonra çözümü Pardus iş
takip sistemine (tracker.pardus.org.tr) çözümünü girerler. İlgili proje
sorumlusu ve yamayı gözden geçirebilme hakkına sahip olan geliştiriciler yamayı
gözden geçirdikten sonra onay alınırsa *proje sahibi* yamayı uygular.

Bir git projesini geliştirmek isteyen katkıcılar, var olan herhangi bir görevi
yapabilirler. Zamanı ve emeği verimli kullanmak adına, her projenin sahip
olması düşünüldüğü, elektronik posta listesine bildiri yapılması
önerilmektedir. Katkıcı tamamladığı bir işi, görev yönetim sisteminden ya da
ilgili posta listesine bildirerek gözden geçirme sürecini başlatmalıdır. Çözümü
geçerli bulunursa *proje sahibi* tarafından projeye dahil edilecektir.

Katkıcı bir projede var olmayan yeni bir özellik yapıp projeye dahil etmek
isteyebilir. Hatta bu isteği sadece projenin gereği olarak görüp, yapmak
istemeyebilir. Bu konuyla ilgili fikirlerini ilgili posta listelerinde
bildirip, fikir alış verişlerinden sonra yapılması gereken olarak kabul
edilirse tracker.pardus.org.tr de yeni bir görev açılır ve ilgili kişiye
atanır. Atanan kişi geliştirici ve ya katkıcı olmasına göre yukarıda belirtilen
yol izlenir.
