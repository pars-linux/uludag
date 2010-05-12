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

Süreç:
======
#. Başvuran kişi bugs.pardus.org.tr'ye üye olur.
#. Başvuran kişi "Gel Katıl Bize" ürününde istediği bileşen için hata açar.
#. Hatanın başlığı "Test/Geliştirme Adaylık Ad Soyad" şeklinde olmalıdır.
#. Hatanın "Ayrıntılar" kısmı aşağıda bulunan bilgilerin cevaplarını içermelidir:

    #. Başvuran kişinin Adı Soyadı
    #. Hiç bir özgür yazılım projesine katkı verdiniz mi?
    #. Daha önce kullandığınız dağıtımlar nelerdir?
    #. Ne zamandır ve hangi seviyede Pardus'u kullanıyorsunuz?
    #. Bir özgür yazılım projesine katkıda bulunmak sizin için ne ifade ediyor?
    #. Daha önce herhangi bir özgür yazılım projesine katkıda bulundunuz mu? Evetse, hangi projeye, ne şekilde, ne kadar zamandır?
    #. Pardus'a neden katkı vermek istiyorsunuz?
    #. Pardus'a haftada ne kadar vakit ayırabilirsiniz?
    #. Kısa özgeçmişin eke eklenmesi
    #. Başvuru geliştirici olmak için ise:
        #. Hazırlamış olduğu paket(ler)i veya harhangi bir uygulama ile yaptığı değişikliği,
        #. Pardus hata takip sisteminde çözmüş olduğu hata var ise bu Hataların bağlantılarını,
        #. Diğer özgür yazılım projelerinde yapmış olduğu yazılım katkılarının (patch, hata çözme, paket yapımı, uygulama geliştirme) bilgilerini ve bağlantılarını vermelidir.
#. Başvuru sahibi başvuru sırasında sorulan soruları özensiz bir şekilde cevaplamış ise hatası "GEÇERSİZ" olarak işaretlenir.

    ::

        Başvuru red stok yorum:
            Başvurunuz olumsuz sonuçlanmıştır. Pardus'a katkı vermeye başladığınız ve kendinizi geliştirdiğiniz takdirde yaklaşık x ay sonra tekrar başvuruda bulunabilirsiniz.
            --
            Pardus Mentor Ekibi

#. Başvuru sahibine ilgili quiz sorularının gönderilmesi:
    #. Başvuru sahibine quiz soruları gönderilirken hatası mentor listesinde bulunan kişiler ve başvuru sahibi hariç tüm kullanıcılara görünmez hale getirilir.

    ::

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

#. Başvuru sahibi soruları çözmeye başladıklarına dair onayı buzilla'ya yorum olarak gönderirler.
#. Onaydan yaklaşık 10 gün sonra başvuru sahibi cevaplarını bugzilla'ya yorum olarak gönderirler.
#. Eğer başvuru sahibi bu 10 gün içerisinde bugzilla üzerinden ulaşılamıyor ise hatası GEÇERSİZ olarak işaretlenir ve ilgili stok yorum Pardus mentor ekibi tarafından yazılır..
#. Başvuru sahibi ulaşılabilir durumda ve quiz sorularını ilgili gün içerisinde göndermiş ise, cevaplar mentorlar tarafından gözden geçirilip bugzilla üzerinde yorumları yapılarak onaylanır.
#. Gözden geçirme olumsuz sonuçlanır ise başvuru sahibi açmış olduğu hata GEÇERSİZ olarak işaretlenir ve ilgili stok yorum Pardus mentor ekibi tarafından yazılır.
#. Başvuru sahibi bu aşamada reddedildiğinde; eğer test için başvurmuş ise 3 ay sonrasında, geliştirme için başvurmuş ise 6 ay sonrasında kendini geliştirdiği takdirde tekrar başvuru yapabilecektir.
#. Gözden geçirme olumlu sonuçlanmış ise:
    #. Başvuru sahibi testçilik için başvurmuş ise test ekibi üyeliğine kabul edilir ve test listesine yazma onayı verilir.
    #. Başvuru sahibi geliştirici olmak için başvurmuş ise:
        #. Quiz'de bulunan sorular doğrultusunda başvuru sahibinin ilgili olduğu alana göre, başvuru sahibi ile daha yakından ilgilenecek bir mentor atanır.
            #. Her mentor'un üzerinde en fazla 3 başvuru yapan kişi bulunabilacektir.
            #. Eğer tüm mentor'lar üzerinde 3 başvuru var ise, yeni başvuru kuyrukta bekleyecek ve kuyrukta bekleyeceğine dair yorum hataya eklenecektir:

            ::

                Başvuru sahibinin kuyrukta beklemesi için gönderilen stok yorum:
                    Şu anda tüm mentor'larımızın slotları doludur, slot'ları uygun olan mentor'lar oluştuğunda size geri dönüş yapılacaktır.
                    Bu süre içerisinde Pardus'a yaptığınız katkılara devam edebilir ve kendinizi bu yönde daha fazla geliştirebilir ve mentor sürecinizi kısaltabilirsiniz.

                    İyi günler,
                    --
                    Pardus Mentor Ekibi

        #. Başvuru sahibine mentor tarafından küçük bir iş(ler) verilir. (not: Küçük iş çözülecek bir hata veya yapılacak bir paket olabilir.)
            #. Başvuru sahibi bu noktadan itibaren çırak olarak adlandırılacaktır.
            #. Çırağa mentor'un isteğine göre birden fazla iş verilebilir.
            #. Bu süreç içerisinde çırağa playground için svn izinleri verilir.
            #. Bu süre içerisinde yapmış olduğu paketlerin sahibi mentor'u olacaktır.
        #.  Mentorun belirtmiş olduğu sürede bu verilen küçük işi yerine getiremez ise hatası GEÇERSİZ olarak işaretlenir ve ilgili yorum mentoru arafından yazılır. Mentor çırağın ne kadar süre sonra tekrar başvurabileceğini de yoruma ekler. (playground svn izinleri de kapatılır)
        #. Çırak verilen küçük iş(ler)i mentor'un istediği süre içerisinde yerine getirebilmiş ise:
            #. Çırak "geliştirici adayı" olarak adlandırılacaktır:

            Geliştirici adaylığı süreci boyunca:
                #. Adaylık süresinin bitimi mentoruna bağlıdır.
                #. Adaylık döneminde yapılan paketlerin sahibi mentor'udur.
                #. Sürümlerin "stable" izinleri dışında izinleri adaya verilecektir.
                #. Mentor aday olgunluğa eriştiğine emin olana kadar çırağı takip eder:
                    #. Aday yaptığı paketlerin gözden geçirilme sürecine katılır.
                    #. Aday süreklilik, doğruluk, kararlılık, iletişim gibi katkıcıda bulunması gereken niteliklere sahip olup olmadığını kontrol eder.
        #. Başvuru sahibi adaylık sürecini geçemez ise hatası GEÇERSİZ olarak işaretlenir ve ilgili yorum mentor'u tarafından yazılır. (Verilmiş olan tüm izinler geri alınır.)
        #. Başvuru sahibi adaylık sürecini geçer ise:
            #. Mentor adaydan emin olduğunda, mentorluğu bıraktığını bugzilla üzerinden yorum olarak ilan eder ve hatasını ÇÖZÜLDÜ olarak işaretler.
            #. Geliştirici olarak kabul edilir
            #. stable dahil tüm svn izinleri verilir.
            #. Adaylık sürecinde yapmış olduğu paketler ve diğer işler mentor'undan adaya devredilir.

#. Başvuru sahibine bir mentor atanana kadar (bugzillla'yı gözden geçirip, quiz iletme, mentor atama uyarısı verme vb.) idare edecek iki kişi olacaktır.
#. Mentor atandıktan sonra başvuru sahibinin sorumluluğu mentorunda bulunmaktadır ve bugzilla'da gerekli yorumları mentoru yapacaktır.
