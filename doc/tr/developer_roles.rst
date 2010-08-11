Geliştiriciler hangi alanlarda katkı sağlarlar?
===============================================

Pardus Linux Dağıtımının geliştiricileri proje içerisinde bir çok farlı rollere sahiptirler.
Bir geliştirici aşağıda bulunan rollerden herhangi birine dahil olabileceği gibi birden fazlasına
da dahil olabilmektedir. Ayrıca tecrübeleri doğrultusunda rolü değişebilir, veya yeni bir role
dahil olabilir.

Paket Bakıcısı
--------------

#. Paketlerin bileşenleri ile ilgili planlama ve koordinasyon çalışmalarına katkı sağlamak.
#. Diğer dağıtımların sürüm planlarını yakından takip etmek.
#. Paketler ile ilgili teknik yazıları ve listeleri okumak ve incelemek.
#. Paketlerin ana geliştiricileri ile iletişim kurmak.
#. Raporlanmış olan hataları araştırmak, analiz etmek, çözmek ve raporlamak.
#. Pardus paket ve depo politikalarına uygun şekilde paketleri yapmak ve güncellemek.
#.Paketi ilgili depolara aktarmadan önce gerekli testleri yapmak ve yaptırmak.
#.Güvenlik açıklarını takip etmek ve Güvenlik Sorumlusu ile koordinasyon içerisinde paketi güncellemek.

Bileşen Sorumlusu
-----------------

* Her ana ve alt bileşenin sorumlusu bulunmalıdır.
* Alt bileşenin sorumlusu bulunmadığı durumda bir üst bileşen sorumlusu bu bileşenin sorumlusu olarak kabul edilir.
* Bileşen ile ilgili en son karar ana bileşen sorumlusuna aittir.

Bileşen Sorumlularının Görev ve Sorumlulukları:
-----------------------------------------------

   #. Sorumlusu olduğu bileşenlerdeki paketlerin geliştiricilerini kontrol etmek:

        Aşağıda bulunan durumlar için kontrol söz konusu olmalıdır:

        - Paket güncellemeleri düzgün yapılıyor mu?
        - Paket hataları ile ilgileniliyor mu?
        - Paket zamanında depoya giriyor mu?

        Paket geliştiricisinden herhangi bir geri bildirim alınamamakta ise:

        #. Pakete gerektiği şekilde müdahale etmek. (Güncelleme, bakım, hata çözme, depoya taşıma)
        #. Paket geliştiricisinin durumunu tanımlamak. (Paketçi emekliye mi ayrılmak istiyor, askerlik durumu ve 
           diğer özel sebeplerden dolayı ara vermek mi istiyor?)

   #. Bileşen içinde paket taşıma işlemlerini yapmak ve paketin o bileşene ait olup olmadığına karar vermek,

   #. Bileşenindeki sahipsiz paketler için,

       #. Sahipsiz paketleri belirleyip işaretlemek,
       #. Sahipsiz paketlerin geçici olarak bakımını üstlenmek,
       #. Sahipsiz paketler için geçici olarak bakım yapma isteklerine izin vermek,
       #. Sahipsiz paketlere sahip bulmak.

   #. Bileşeni altında bulunan paketler için paket gözden geçirme politikasına uygun olarak sürece dahil olmak.
Yazılım Geliştirici:
--------------------

#. Yeni özellik isteklerini göz önünde bulundurarak, yazılım ana sorumlusuna danışarak gerekler listesi oluşturmak
#. Yazılım tasarımını yapmak. Yazılım tasarımı tarifinin belgelenmesine katkıda bulunmak.
#. Yazılımın kullanıcı kılavuzunu ve diğer teknik belgeleri yazmak.
#. Yazılımın kodlamasını yapmak, birim testlerini yürütmek ve belgelemek.
#. Yazılımın bakımını yapmak, hataları gidermek ve raporlamak.
#.  Yazılımın ve (gerekli durumlarda) bağımlısı olduğu diğer paketlerin bakıcılığını üstlenmek.

Yazılım Ana Geliştirici:
------------------------

#. Ana Geliştiricisi olduğu yazılımın tüm yaşam çevrimini planlamak, yürütmek ve yönetmek.
#. Yeni özellik isteklerini göz önünde bulundurarak, ilgili projeya bağlı bulunan tüm geliştiriciler ile birlikte gerekler listesi oluşturmak.
#. İlgili geliştiricileri organize ve koordine etmek.
#. Yazılımın geliştirme projesini planlamak, Sürüm Yöneticileri ile koordinasyon içerisinde yol haritasını ve takvimini oluşturmak.
#. Projeye bağlı hataları gözden geçirmek, gerekli önem ve öncelik durumlarını belirlemek.

