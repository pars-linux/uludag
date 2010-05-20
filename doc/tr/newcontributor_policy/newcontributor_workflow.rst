Yeni Katkıcı Kabul Politikası
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. contents:: :depth: 2

.. .. admonition:: Abstract

   bla bla bla bla bla


.. #. Bugzilla Katkıcı Adayı Takibi

Bugzilla Katkıcı Adayı Takibi
=============================

- Bu izleme süreci için "Yeni Katkıcı / New Contributor" ürünü bulunmaktadır.
- Bu ürün altında "Geliştirici / Developer", "Testçi / Tester" bileşenleri bulunmaktadır.
- Çeviri başvuruları transifex.pardus.org.tr üzerinden yapılmaktadır.
- Bugzilla izinleri:
    - Bugzilla'da bulunan "Yeni Katkıcı / New Contributor" ürünü için bir mentor grubu bulunmaktadır.
    - Bu grubun dışında bulunan kişiler hata açabilecek fakat hata durumunda bir değişiklik yapamayacaktır.

    ..  image:: mentoring.png

Süreç:
------
#. Başvuran kişi bugs.pardus.org.tr'ye üye olur.
#. Başvuran kişi "Yeni Katkıcı / New Contributor" ürününde istediği bileşen için hata açar.
#. Hatanın başlığı "Testçi veya Geliştirici Adaylık Ad Soyad" şeklinde olmalıdır.
#. Hatanın "Ayrıntılar" kısmı aşağıda bulunan bilgilerin cevaplarını içermelidir:

    #. Başvuran kişinin Adı Soyadı
    #. Daha önce kullandığınız dağıtımlar nelerdir?
    #. Ne zamandır ve hangi seviyede Pardus'u kullanıyorsunuz?
    #. Bir özgür yazılım projesine katkıda bulunmak sizin için ne ifade ediyor?
    #. Daha önce herhangi bir özgür yazılım projesine katkıda bulundunuz mu? Evetse, hangi projeye, ne şekilde, ne kadar zamandır?
    #. Pardus'a neden katkı vermek istiyorsunuz?
    #. Pardus'a haftada ne kadar vakit ayırabilirsiniz?
    #. Kısa özgeçmişin eke eklenmesi
    #. Başvuru geliştiriciolmak için ise:
        #. Hazırlamış olduğu paket(ler)i veya harhangi bir uygulama üzerinde yaptığı değişikliği,
        #. Pardus hata takip sisteminde çözmüş olduğu hata var ise bu hataların bağlantılarını veya numaralarını,
        #. Diğer özgür yazılım projelerinde yapmış olduğu yazılım katkılarının (patch, hata çözme, paket yapımı, uygulama geliştirme) bilgilerini ve bağlantılarını vermelidir.

#. Başvuru sahibi başvuru sırasında sorulan soruları özensiz bir şekilde cevaplamış ise mentor koordinatorleri tarafından hatası "KARAR VERİLDİ/GEÇERSİZ" olarak işaretlenir ve `Başvuru Red Hazır Yorumu`_ yapılır.
#. Başvuru sahibi bu aşamada reddedildiğinde; eğer test için başvurmuş ise 3 ay, geliştirme için başvurmuş ise 6 ay sonrasında kendini geliştirdiği takdirde tekrar başvuru yapabilecektir.
#. Başvuru sahibine ilgili quiz sorularının gönderilmesi:
    #. Başvuru sahibine quiz soruları gönderilirken hatası mentor listesinde bulunan kişiler ve başvuru sahibi hariç tüm kullanıcılara görünmez hale getirilir.
    #. Quiz soruları mentor koordinatörleri tarafından `Quiz Gönderme Hazır Yorumu`_ ile gönderilir.

#. Başvuru sahibi soruları çözmeye başladıklarına dair onayı buzilla'ya yorum olarak gönderir.
#. Onaydan yaklaşık 10 gün içerisinde başvuru sahibi cevaplarını bugzilla'ya yorum olarak gönderir.
#. Eğer başvuru sahibi bu 10 gün içerisinde bugzilla üzerinden ulaşılamıyor ise hatası KARAR VERİLDİ/GEÇERSİZ olarak işaretlenir ve `Başvuru Red Hazır Yorumu`_ mentor koordinatörleri tarafından yazılır.
#. Başvuru sahibi ulaşılabilir durumda ve quiz sorularını ilgili gün içerisinde göndermiş ise, cevaplar mentorlar tarafından gözden geçirilip bugzilla üzerinde yorumları yapılarak onaylanır.
#. Gözden geçirme olumsuz sonuçlanır ise başvuru sahibinin açmış olduğu hata mentor koordinatörleri tarafından KARAR VERİLDİ/GEÇERSİZ olarak işaretlenir ve `Başvuru Red Hazır Yorumu`_ yapılır.
#. Başvuru sahibi bu aşamada reddedildiğinde; eğer test için başvurmuş ise 3 ay, geliştirme için başvurmuş ise 6 ay sonrasında kendini geliştirdiği takdirde tekrar başvuru yapabilecektir.
#. Gözden geçirme olumlu sonuçlanmış ise:
    #. Başvuru sahibi testçilik için başvurmuş ise test ekibi üyeliğine kabul edilir ve test listesine yazma onayı verilir. Mentor koordinatörleri tarafından `Testçi Başvuru Kabul Hazır Yorumu`_ yapılır ve hata KARAR VERİLDİ/ONAYLANDI olarak işaretlenir.
    #. Başvuru sahibi geliştirici olmak için başvurmuş ise:
        #. Quiz'de bulunan sorular doğrultusunda başvuru sahibinin ilgili olduğu alana göre, başvuru sahibi ile daha yakından ilgilenecek bir mentor atanır.
            #. Her mentor'un üzerinde en fazla 3 başvuru yapan kişi bulunabilacektir.
            #. Eğer tüm mentor'lar üzerinde 3 başvuru var ise, yeni başvuru kuyrukta bekleyecek ve kuyrukta bekleyeceğine dair stok yorum mentor koordinatörleri tarafından hataya eklenecektir.
            #. Menor'un atanma sürecini mentor koordinatörleri takip eder.
                #. Her mentor üzerinde bulunan başvuru sayısı takibi,
                #. Mentor atanması için mentor@pardus.org.tr üzerinden uyarı maili gönderilmesi,
            #. Başvuru sahibine bir mentor atandığında, hata üzerinden mentor koordinatörleri tarafından  `Mentor Atama Hazır Yorumu`_ yapılır, anahtar kelimeyi "mentor" olarak işaretler ve hatanın sahibini mentor@pardus.org.tr'den ilgili mentora atar.

        #. Başvuru sahibine mentor tarafından küçük bir iş(ler) verilir. (not: Küçük iş çözülecek bir hata veya yapılacak bir paket olabilir.)
            #. Başvuru sahibi bu noktadan itibaren çırak olarak adlandırılacaktır.
            #. Çırağa mentor'un isteğine göre birden fazla iş verilebilir.
            #. Bu süreç içerisinde çırağa playground için svn izinleri verilir. (playground svn izni verilmesi uyarı maili mentor'u tarafından Pardus Sys. Admin'e yapılacaktır.)
            #. Bu süre içerisinde yapmış olduğu paketlerin sahibi mentor'u olacaktır.
        #.  Mentorun belirtmiş olduğu sürede bu verilen küçük işi yerine getiremez ise hatası mentoru tarafından KARAR VERİLDİ/GEÇERSİZ olarak işaretlenir ve ilgili yorum yazılır. Mentor çırağın ne kadar süre sonra tekrar başvurabileceğini de yoruma ekler. (playground svn izni kaldırılması uyarı maili mentor'u tarafından Pardus Sys. Admin'e yapılacaktır.)
        #. Çırak verilen küçük iş(ler)i mentor'un istediği süre içerisinde yerine getirebilmiş ise:
            #. Çırak "geliştirici adayı" olarak adlandırılacaktır:

            Geliştirici adaylığı süreci boyunca:
                #. Adaylık süresinin bitimi mentoruna bağlıdır.
                #. Adaylık döneminde yapılan paketlerin sahibi mentor'udur.
                #. Sürümlerin "stable" izinleri dışında izinleri adaya verilecektir. (svn izni verilmesi uyarı maili mentor'u tarafından Pardus Sys. Admin'e yapılacaktır.)
                #. Mentor adayın olgunluğa eriştiğine emin olana kadar takip eder:
                    #. Adayın yaptığı paketlerin gözden geçirilme sürecine katılır.
                    #. Adayın süreklilik, doğruluk, kararlılık, iletişim gibi katkıcıda bulunması gereken niteliklere sahip olup olmadığını kontrol eder.
        #. Başvuru sahibi adaylık sürecini geçemez ise hatası mentoru tarafından KARAR VERİLDİ/GEÇERSİZ olarak işaretlenir ve ilgili yorum yazılır. (Verilmiş olan tüm izinler geri alınır.) (svn izni kaldırılması uyarı maili mentor'u tarafından Pardus Sys. Admin'e yapılacaktır.)
        #. Başvuru sahibi adaylık sürecini geçer ise:
            #. Mentor adaydan emin olduğunda, mentorluğu bıraktığını bugzilla üzerinden yorum olarak ilan eder ve hatasını KARAR VERİLDİ/ÇÖZÜLDÜ olarak işaretler.
            #. Geliştirici olarak kabul edilir
            #. stable dahil tüm svn izinleri verilir.(stable svn izni verilmesi uyarı maili mentor'u tarafından Pardus Sys. Admin'e yapılacaktır.)
            #. Adaylık sürecinde yapmış olduğu paketler ve diğer işler mentor'undan adaya devredilir.

#. Başvuru sahibine bir mentor atanana kadar (bugzillla'yı gözden geçirip, quiz iletme, mentor atama uyarısı verme vb.) mentor koordinatorleri süreci takip eder.
#. Mentor atandıktan sonra başvuru sahibinin sorumluluğu mentorunda bulunmaktadır ve bugzilla'da gerekli karar yorumlarını mentoru yapacaktır.

.. #. Hazır Yorumlar

Hazır Yorumlar
==============

Başvuru Red Hazır Yorumu
------------------------
    ::

        Başvuru red hazır yorum:
            Başvurunuz olumsuz sonuçlanmıştır. Pardus'a katkı vermeye başladığınız ve kendinizi geliştirdiğiniz takdirde yaklaşık x ay sonra tekrar başvuruda bulunabilirsiniz.
            --
            Pardus Mentor Koordinatörleri

Quiz Gönderme Hazır Yorumu
--------------------------
    ::

        Quiz gönderme hazır yorum:
            Merhabalar,
            Öncelikle x üyesi adaylığınızı kutlar ve Pardus'a katkıda bulunmak istediğiniz için teşekkür ederiz.
            x ekibi üyeliği sürecinin ilk aşaması olan ve Pardus Linux Dağıtımı alt yapısı ve x süreçleri ile ilgili bilgilendirici nitelikte sorulara sahip olan sınavımızı ekte bulabilirsiniz.

            Kaynaklar,
            x
            y
            z

            Kolay Gelsin,
            --
            Pardus Mentor Koordinatörleri

Testçi Başvuru Kabul Hazır Yorumu
---------------------------------

    ::

        Testçi Başvuru kabul hazır yorum:
            Başvurunuz olumlu sonuçlanmıştır,  testçi@pardus.org.tr için gerekli izinleriniz verilmiştir. Pardus'a yapacağınız katkılarda dolayı şimdiden size teşşekür ederiz.  
            --
            Pardus Mentor Koordinatörleri


Kuyrukta Bekleme Hazır Yorumu
-----------------------------
    ::

          Başvuru sahibinin kuyrukta beklemesi için gönderilen hazır yorum:
          Şu anda tüm mentor'larımızın slotları doludur, slot'ları uygun olan mentor'lar oluştuğunda size geri dönüş yapılacaktır.
          Bu süre içerisinde Pardus'a yaptığınız katkılara devam edebilir ve kendinizi bu yönde daha fazla geliştirebilir ve mentor sürecinizi kısaltabilirsiniz.

          İyi günler,
          --
          Pardus Mentor Koordinatörleri

Mentor Atama Hazır Yorumu
-------------------------

    ::

        Göndermiş olduğunuz cevaplar doğrultusunda size x kişisi mentor olarak atanmıştır. http://svn.pardus.org.tr/uludag/trunk/playground/ ve http://svn.pardus.org.tr/pardus/playground/ izinleriniz verilmiştir. Bu aşamada size mentor tarafından küçük iş(ler) verilecektir.

        Bu aşamada yapacağınız çalışmalar için şimdiden kolaylıklar dileriz.
        --
        Pardus Mentor Koordinatörleri
