Hata Raporlama Döngüsü
======================

 ..  image:: bugCycle.png

Bu süreç Pardus Hata takip sisteminde paket hatalarının kapatılma döngüsünü anlatmaktadır, bu sürecin içerisine Paket gözden geçirme süreci dahil değildir.

    #. (1)(2)Bir hata ilk kez biri tarafından raporlandığında "New" durumunu (status) almaktadır. Hata alınan uygulamanın sahibi ön tanımlı olarak atanan kısmına eklenmekte ve normal bir kullanıcı tarafından değiştirilememektedir.

    #. (1)(2)Hata alınan uygulamanın raporlanması için çeşitli ayrıntılar gerekmektedir:

        #. Hata alınan uygulamanın hangi bileşeninde hata alınmış olduğu belirlenmelidir.
        #. Hatanın alınmış olduğu mimari seçilmelidir.
        #. Hatanın alınmış olduğu Pardus sürümü seçilmelidir.
        #. Özet bölümüne olabildiğince ipucu kelime kullanarak karşılaşılan problemi özetleyen bir cümle girilmelidir.
        #. Hatayı daha ayrıntılı biçimde anlatan bir açıklama girilmelidir.
        #. Hatanın tekrarlanma sıklığı için dört farklı seçenekten biri seçilmelidir:

            #. Her zaman tekrarlanabiliyor
            #. Bazen tekrarlanabiliyor
            #. Hatayı tekrarlamayı denemedim
            #. Hatayı tekrarlayamıyorum

        #. Hatanın tekrarlanması için hangi adımların gerekli olduğu sırası ile açıklanmalıdır.
        #. Güncel ve beklenen sonuçlar girilmelidir.
        #. Hatanın önemi için dört farklı seçenek bulunmaktadır, bu kriterler hatanın dağıtım için ne kadar önemli olduğu göz önünde bulundurularak seçilmelidir:

            #. Acil/Urgent: Tüm sistemi kullanılmaz hale getiren hatalar
            #. Büyük/High: Uygulamayı kullanılmaz hale getiren hatalar
            #. Normal/Medium: Programın bir kısmını kullanılmaz hale getiren hatalar
            #. Küçük/Low: Yeni bir özellik isteği, çeviri eksikliği veya kozmetik bir problem
        #. Gerekli olan hata çıktıları, log dosyaları, hatayı çözen yamalar vb. eklenerek gönderilmelidir.

    #. (3)Bu aşamadan sonra geliştiricisi tarafından hata eğer "NEEDINFO" anahtarı ile işaretlenir ise raporlayıcısı tarafından bilgi bekliyor durumda demektir.

    #. Eğer raporlanan hata ek bilgiye ihtiyaç duymuyor ise:

        #. (4.a)Hatanın önem derecesi(severity) geliştiricisi tarafından tekrar belirlenecektir ve bu aşamadan sonra hatanın önem kriteri tekrar değiştirilmemelidir.

            #. Acil/Urgent: Tüm sistemi kullanılmaz hale getiren hatalar
            #. Büyük/High: Uygulamayı kullanılmaz hale getiren hatalar
            #. Normal/Medium: Programın bir kısmını kullanılmaz hale getiren hatalar
            #. Küçük/Low: Yeni bir özellik isteği, çeviri eksikliği veya kozmetik bir problem

        #. (4.b)Hata eğer çözümlenemeyecek bir hata ise, aşağıda bulunan durumlardan en uygunu seçilerek geliştiricileri tarafından hata durumu değiştirilmelidir.

            #. WONTFIX/DÜZELTİLMEYECEK: Hiç bir zaman düzeltilmeyecek hatalar.
            #. DUPLICATE/AYNISI: Daha önce aynısı raporlanmış hatalar
            #. INVALID/GEÇERSİZ: Gerçekte hata olmayan hatalar.
            #. WORKSFORME/BENDEÇALIŞIYOR: Tekrarlanamayan hatalar

        #. (4.c)Hatanın önceliği (priority) ana bileşen sorumlusu veya sürüm yöneticisi tarafından belirlenebilmektedir.

            #. High/1: İlgili sürümde düzeltilmesi gereken hatalar
            #. Medium/2: Bir sonraki sürümde düzeltilmesi gereken hatalar.
            #. Low/3,4,5: Düzelme zamanı çok önemli olmayan hatalar.

        #. (4.d)Sürüm engelleyici hatalar bileşen sorumlusu veya sürüm yöneticisi tarafından sürümün adı ile açılmış hataya bağlı bir hata haline getirilebilir.

    #. (5.a)(5.b)Eğer hata geliştiricisi tarafından çözülmüş ise,

        Geliştiricisi hatayı çözdüğüne emin olduğunda yaptığı değişiklikleri sürüm takip sistemi üzerinden göndermelidir.

        Hatayı kapatacak olan SVN açıklaması  BUG:FIXED:<Hata Numarası> bilgisini içermelidir.

        Bu işlem ile hata durumu otomatik olarak ÇÖZÜLDÜ olarak işaretlenmektedir.

    #. (6)Fixlenen hata diğer güncellenen paketler ile birlikte kararlı depo test sürecine girecek ve alınan geliştirici onayı (ACK/NACK) sonrasında, test sürecine dahil olacaktır.

    #. (7)Hata alınan paketlerin test sonuçları bugzilla üzerinden gönderilecektir. Eğer daha önce bugzilla'da aynı hata raporlanmış ise bu hataya yorum yapılacaktır.

    #  (8)Test sorumlusu daha önce REOLVED/FIXED olarak işaretlenip, test süreci sonrasında aynı hatayı almış paketlerin hatalarını tekrar açacak (REOPENED), ve paket tekrar hata döngüsü içerisine girecektir. Aynı şekilde hatayı raporlamış olan kişi de RESOLVED/FIXED olarak işaretlenmiş hatasını tekrarlayabildiği takdirde REOPENED olarak durumunu değiştirebilmektedir.

    # (9)Test süreci içerisine girmiş ve hata ile karşılaşılmamış fakat daha önce hata raporu bulunan paketler, test sorumlusu tarafından gözden geçirilecek ve eğer hataları tekrarlanamıyor ise VERIFIED (ONAYLANDI) olarak işaretlenecek ve hatanın döngüsü son bulacaktır.
