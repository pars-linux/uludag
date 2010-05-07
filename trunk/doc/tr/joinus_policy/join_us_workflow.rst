Gel Katıl Bize Serüveni
=======================

Bugzilla üzerinden Pardus gönüllü takibi
----------------------------------------
- "Gel Katıl Bize/ Join us" ürünü açılması
- Bu ürün için "Geliştirme", "Test" bileşenlerinin açılması
- Çeviri başvuruları transifex.pardus.org.tr üzerinden yapılmaktadır.
- Bileşenlerin öntanımlı cc'leri mentor@pardus.org.tr listesi olacak.
- mentor@pardus.org.tr listesindeki mesajlara dışarıdan erişim bulunmayacak
- Bugzilla izinleri:
    - Bugzilla'da bulunan "Gel Katıl Bize/ Join us" ürünü için bir mentor grubu oluşturulacak. İzinleri Shown/Default, CANEDIT olarak verilecektir.
    - Bu grubun dışında bulunan kişiler hata açabilecek fakat hata durumunda bir değişiklik yapamayacak, sadece yorum yazabilecek.

    ..  image:: mentoring.png

#. Aday bugs.pardus.org.tr'ye üye olur.
#. Aday "Gel Katıl Bize" ürününde istediği bileşen için hata açar.
#. Hatanın başlığı "Test/Geliştirme Adaylık Ad Soyad" şeklinde olmalıdır.
#. Hatanın "Ayrıntılar" kısmı aşağıda bulunan bilgilerin cevaplarını içermelidir:

    #. Adayın Adı Soyadı
    #. Hiç bir özgür yazılım projesine katkı verdiniz mi?
    #. Daha önce kullandığınız dağıtımlar nelerdir?
    #. Ne zamandır ve hangi seviyede Pardus'u kullanıyorsunuz?
    #. Bir özgür yazılım projesine katkıda bulunmak sizin için ne ifade ediyor?
    #. Daha önce herhangi bir özgür yazılım projesine katkıda bulundunuz mu? Evetse, hangi projeye, ne şekilde, ne kadar zamandır?
    #. Pardus'a neden katkı vermek istiyorsunuz?
    #. Pardus'a haftada ne kadar vakit ayırabilirsiniz?
    #. Kısa özgeçmişin eke eklenmesi
    #. Aday, geliştirici olmak için başvuruyor ise:
        #. Hazırlamış olduğu paket(ler)i veya harhangi bir uygulama ile yaptığı değişikliği,
        #. Pardus hata takip sisteminde çözmüş olduğu hata var ise bu Hataların bağlantılarını,
        #. Diğer özgür yazılım projelerinde yapmış olduğu yazılım katkılarının (patch, hata çözme, paket yapımı, uygulama geliştirme) bilgilerini ve bağlantılarını vermelidir.
#. Aday başvuru sırasında sorulan soruları özensiz bir şekilde cevaplamış ise hatası "GEÇERSİZ" olarak işaretlenir.

    Başvuru red stok yorum:
        Başvurunuz olumsuz sonuçlanmıştır. Pardus'a katkı vermeye başladığınız ve kendinizi geliştirdiğiniz takdirde yaklaşık x ay sonra tekrar başvuruda bulunabilirsiniz.
        --
        Pardus Mentor Ekibi

#. Adaya ilgili quiz sorularının gönderilmesi:

    Quiz sorusu stok yorum:
        Merhabalar,
        Öncelikle x üyesi adaylığınızı kutlar ve Pardus'a katkıda bulunmak istediğiniz için teşekkür ederiz.
        x ekibi üyeliği sürecinin ilk aşaması olan ve Pardus Linux Dağıtımı alt yapısı ve x süreçleri ile ilgili bilgilendirici nitelikte sorulara sahip olan sınavımızı ekte bulabilirsiniz.

        Kaynaklar,
        x
        y
        z

        Kolay Gelsin,
        --
        Pardus Mentor Ekibi

   #. Adaya quiz soruları gönderilirken hatası kullanıcılara görünmez hale getirilir.
    #. Aday kabul veya reddedilene kadar hatası gizli olarak kalır.
#. Adaylar soruları çözmeye başladıklarına dair onayı buzilla'ya yorum olarak gönderirler.
#. Onaydan yaklaşık 10 gün sonra adaylar cevaplarını bugzilla'ya yorum olarak gönderirler.
#. Eğer adaylara bu 10 gün içerisinde bugzilla üzerinden ulaşılamıyor ise hatası GEÇERSİZ olarak işaretlenir ve ilgili stok yorum Pardus mentor ekibi tarafından yazılır..
#. Aday ulaşılabilir durumda ve quiz sorularını ilgili gün içerisinde göndermiş ise, cevaplar mentorlar tarafından gözden geçirilip bugzilla üzerinde yorumları yapılarak onaylanır.
#. Gözden geçirme olumsuz sonuçlanır ise adayın açmış olduğu hata GEÇERSİZ olarak işaretlenir ve ilgili stok yorum Pardus mentor ekibi tarafından yazılır.
#. Aday bu aşamada reddedildiğinde; eğer test için başvurmuş ise 3 ay sonrasında, geliştirme için başvurmuş ise 6 ay sonrasında kendini geliştirdiği takdirde tekrar başvuru yapabilecektir.
#. Gözden geçirme olumlu sonuçlanmış ise:
    #. Aday testçilik için başvurmuş ise test ekibi üyeliğine kabul edilir ve test listesine yazma onayı verilir.
    #. Aday geliştirici olmak için başvurmuş ise:
        #. Quiz'de bulunan sorular doğrultusunda adayın ilgili olduğu alana göre, aday ile daha yakından ilgilenecek bir mentor atanır.
            #. Her mentor'un üzerinde en fazla 3 aday bulunabilacektir.
            #. Eğer tüm mentor'lar üzerinde 3 aday var ise, yeni aday kuyrukta bekleyecek ve kuyrukta bekleyeceğine dair yorum hataya eklenecektir:

                Aday'ın kuyrukta beklemesi için gönderilen stok yorum:
                    Şu anda tüm mentor'larımızın slotları doludur, slot'ları uygun olan mentor'lar oluştuğunda size geri dönüş yapılacaktır.
                    Bu süre içerisinde Pardus'a yaptığınız katkılara devam edebilir ve kendinizi bu yönde daha fazla geliştirebilir ve mentor sürecinizi kısaltabilirsiniz.

                    İyi günler,
                    --
                    Pardus Mentor Ekibi

        #. Adaya mentor tarafından küçük bir iş(ler) verilir. (not: Küçük iş çözülecek bir hata veya yapılacak bir paket olabilir.)
            #. Adaya mentor'un isteğine göre birden fazla iş verilebilir.
            #. Bu süreç içerisinde adaya playground için svn izinleri verilir.
            #. Bu süre içerisinde yapmış olduğu paketlerin sahibi mentor'u olacaktır.
        #. Aday mentorun belirtmiş olduğu sürede bu verilen küçük işi yerine getiremez ise hatası GEÇERSİZ olarak işaretlenir ve ilgili yorum mentoru arafından yazılır. Mentor adayın ne kadar süre sonra tekrar bşvurabileceğini de yoruma ekler. (playground svn izinleri de kapatılır)
        #. Aday verilen küçük iş(ler)i mentor'un istediği süre içerisinde yerine getirebilmiş ise:
            #. Aday çırak olarak  adlandırılacaktır:
            Çıraklık süreci boyunca:
                #. Çıraklık süresinin bitimi mentoruna bağlıdır.
                #. Sürümlerin "stable" izinleri dışında izinleri çırağa verilecektir.
                #. Mentor çırağın olgunluğa eriştiğine emin olana kadar çırağı takip eder:
                    #. Çırağın paketlerinin gözden geçirilme sürecine katılır.
                    #. Çırağın süreklilik, doğruluk, kararlılık, iletişim gibi katkıcıda bulunması gereken niteliklere sahip olup olmadığını kontrol eder.
        #. Aday çıraklık sürecini geçemez ise hatası GEÇERSİZ olarak işaretlenir ve ilgili yorum mentor'u tarafından yazılır. (Verilmiş olan tüm izinler geri alınır.)
        #. Aday çıraklık sürecini geçer ise:
            #. Mentor çıraktan emin olduğunda, mentorluğu bıraktığını bugzilla üzerinden yorum olarak ilan eder ve hatasını ÇÖZÜLDÜ olarak işaretler.
            #. Geliştirici olarak kabul edilir
            #. stable dahil tüm svn izinleri verilir.
            #. Çıraklık sürecinde yapmış olduğu paketler ve diğer işler mentor'undan adaya devredilir.

#. Adaya bir mentor atanana kadar (bugzillla'yı gözden geçirip, quiz iletme, mentor atama uyarısı verme vb.) idare edecek iki kişi olacaktır.
#. Mentor atandıktan sonra adayın sorumluluğu mentorunda bulunmaktadır ve bugzilla'da gerekli yorumları mentoru yapacaktır.
