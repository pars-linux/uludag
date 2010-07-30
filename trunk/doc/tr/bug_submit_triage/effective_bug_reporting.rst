Nasıl daha etkili hata raporlarım?
==================================

Bu yazı iyi bir hata raporunun nasıl olması gerektiğini açıklamaktadır.

Kısaca anlamı ile hata raporu geliştiricinin uygulamadaki hatanın tekrarlayabilmesi için önemlidir. Geliştirici raporu kullanarak uygulamanın hatasını anlayabilene kadar hatayı tekrarlayan kullanıcıdan bilgi istemektedir.

Hata raporlarında gerçek sorunun ne olduğu açıkça anlatılmalıdır, histerik danranılmamalıdır ("Bilgisayarın başındaydım ve herşey o anda oldu") ve gereksiz kurgulara yer verilmemelidir ("Sanırım sorun buradan kaynaklanıyor"). Düşüncelerinizi aktarabilirsiniz, fakat bunları efsaneleştirmeye çalışmayınız.

Hata raporlamanızın amacı hatayı çözüme kavuşturma isteğinizdir. Geliştiriciye karşı kötü sözler söylemenin veya kasten hatanın çözülmesine engel olmanın hiç bir anlamlı ifadesi bulunmamaktadır: yazılan programda hata almış olabilirsiniz, bu yüzden problem yaşıyor ve sinirlenmiş olabilirsiniz fakat hatanın çabucak çözüme kavuşması için yapmanız gereken en iyi şey hata için gerekli olabilcek tüm bilgiyi açık bir dil ile rapora aktarmaktır. Unutulmamalıdır ki geliştiricilerimizin büyük bir kısmı gönüllü olarak çalışmaktadır ve raporlayıcı görgü kurallarını aştığında ve kötü sözler sarf etmeye başladığında, geliştiricilerimizde kibar davranmayı bırakabilmektedir.

Çalışmıyor!
-----------

Geliştiriciye biraz akıl yürütebilmesi için fırsat tanıyın: hatanın özet ve açıklamalarında olabildiğince açık bir dil kullanmaya ve bilgi vermeye çalışın. Eğer gerçekten uygulama tamamıyla çalışmıyorsa,büyük bir ihtimal geliştiricisi bunu farketmiş ve mutlaka bunun üzerinde çalışıyordur. Bu yüzden uygulamanın tamamıyla çalışmamasının kullanıcı kaynaklı olup olmadığını anlamaya çalışın. Daha önce değiştirmiş olduğunuz bir ayar dosyası, update sırasında bilgisayarın ani bir şekilde kapatılması gibi bir durum söz konusu olabilir.

Hata takip sisteminde birçok hata bulunmaktadır, eğer hata aldığınız uygulama daha önce raporlanmış ise, bu hatayı tekrar raporlamamalısınız. Fakat daha önce raporlanmış hatayı daha iyi açıklayan bir yorum yazabilirsiniz. Bu hatanın geliştiricidinin işine yarabilecek bir durumdur.

Uygulamayı kullanma yardımı almak için hata girilmemelidir, gerekli yardım kullanıcı listeleri ve forumlardan alınmalıdır?


Kendi kendine hatayı nasıl gösteriyorsan, öyle göster bana?
-----------------------------------------------------------

Geliştiricinin sizin uyguladığınız yöntemin aynısını izleyerek hatayla karşılaşmasını sağlayın, amaç burada sadece hatayı tekrarlatmaya çalışmaktır. Eğer gözleri önünde programın çalışmadığını görürlerse, bununla ilgilenmek için heyecan duyarlar.

Bu yüzden açık bir şekilde ne yaptığınız anlatın. Eğer grafiksel bir uygulama ise, hangi butonlara bastığınızı, hangi bildirimlerde bulunduğunuzu belirtin. Eğer komut satırından çalışan bir uygulama ise hangi komutları sırası ile kullandığınızı sırası ile yazınız, eğer mümkünse komutları yazdığınız ve sonuçları aldığınız alanı kopyalayınız ve rapora ekleyiniz.

Geliştiriciye uygulama ile ilgili aklınıza gelen her bilgiyi verin. Eğer uygulama bir dosya okurken hata aldıysanız mutlaka bu dosyayı ek olarak ekleyin. Gerekli log dosyalarını da eklemeyi unutmayın.


Bende çalışıyor, o zaman sorun ne?
----------------------------------

Geliştiriciye gerekli bilgileri ve bildirimleri gönderdiniz, geliştirici hatayı tekrarlamaya çalıştı ve her şeyin yolunda olduğunu gözlemledi. Büyük bir olasılıkla tüm bilgileri geliştiriciye göndermediniz, belkide bu hata tüm bilgisayarlarda tekrarlanayamayan bir hataydı. Aynı zamanda geliştiricinin bir sorunla karşılaşmamasının nedeni anlayış biçimi farklılığından da kaynaklanıyor olabilmektedir. Sizin için yanlış olan bir durumun geliştiricisi için uygulamaya eklediği yeni bir özellik veya davranış olabilmektedir.

Bu yüzden hatayı aldığınızda ne olduğunu anlatın, ne gördüğünüzü açıklayın. Gördüğünüz şeyin size neden yanlış geldiğini anlatın; diğer bir değişle uygulamadan ne beklediğinizi açıklayın.

Eğer hata mesajları gördüyseniz, bunları rapora mutlaka ekleyin. Hata measjını eksiksiz bir şekilde göndermeye özen gösterin. Örneğin hata mesajlarında bulunan sayılar, geliştiricinin gerekli bilgiyi elde edbilmesi için önemli olabilmektedir. Bu aşamada gerliştirici problemi çözmeyi değil, bulmayı düşünmektedir. Sizin göndermiş olduğunuz hata mesajları doğrultusunda neyin kötü gittiğini anlamaya çalışmaktadır.

Sakin Olun!
------------

Bir hata ile karşılaştığınızda bir çok farklı yapılacak şey aklınıza gelebilir. Fakat bunların bir çoğu problemi daha kötü duruma getirebilir.

Kullanıcılar genellikle tetikte av bekleyen bir aslan gibidir. Aslan avı gördüğünde hızlı bir hamle ile etkisiz hale getirir. Fakat bu durum bilgisayarda hata alındığında uygulanması uygun olmayan bir yöntemdir. Bu durum için, aslan olmak yerine geyik olmak daha iyidir. Geyik düşmanı gördüğünde hareketsiz olarak kalır ve dikkat çekmemek için hiç bir şey yapmaz.

Bilgisayarda problem ile karşılaştığınızda, ne yapıyorsanız bırakın. Hiç bir butona, tuşa basmayın. Ekrana bakın ve herşey normale dönene kadar bekleyin, bu sürede olan olayları bir yere kaydedin. Daha sonra dikkatli bir şekilde ekranda çıkan görüntüyü inceleyin ve sizin için en güvenli olduğunu düşündüğünüz yöntemi seçin. Bilgisayar karşısında istenmeyen bir durum ile karşılaştığınızda (donma, takılma çökme vb.) bir refleks geliştirin.

Hata ile başedebildiğiniz noktada (İlgili uygulamayı kapatmış olabilirsiniz, bilgisayarı yeniden başlatmış olabilirsiniz, vb.), hatayı yeniden tekrarlamayı deneyin. Geliştiriciler birden fazla kez tekrarlanabilen hataları severler. Ve mutlu geliştiriciler daha etkili ve hızlı hata çözerler :)

Bu çok garip, biraz önce çökmüştü!
----------------------------------

Basit hatalar, belirli bir sırada yapılan işlemler sonrasında ortaya çıkan hatalardır. Fakat bazı hatalar haftada bir, ayda bir veya herhangi bir zamanda ortaya çıkan hatalardır. 

Çoğu rastgele oluşan hata aslında rastgele olmayabilir. Çoğunun bazı mantıksal ifadesi bulunmaktadır. Bazıları makinenin hafızasının yetersiz kalmasından, bazıları kritik bir dosyaya yanlış zamanda yazmasından meydana gelebilir. Bu yüzden hatayı aldığınız anda açık olan tüm programları açıklamanız yararlı olabilmektedir. (Örneğin: Genellikle Gimp açık iken ekran donuyor.)

Ayrıca eğer geliştirici hatayı tekrar edemiyor ama siz edebiliyorsanız, bir şekilde sizin bilgisayarınızın geliştiricininkinden farklı olmasından kaynaklanıyor olabilir ve bu fark hataya neden oluyor olabilir. Bu hatalar genellikle donanıma bağlı olan hatalar olmaktadır, bu durumda hata aldığınız uygulamanını bağlı olduğu donanımların bilgisiniz hata raporuna eklemek çok yararlı olacaktır.


"Uygulamayı açtım, uyarı penceresi çıktı, sonra kapatmaya çalıştım, çöktü"
--------------------------------------------------------------------------

Hata raporunun açık ve temiz bir dil ile yazılmış olması önemlidir. Geliştirici sizin ne söylediğinizi anlamadığı sürece siz hiç bir şey söylememişsiniz demektir.

    * Spesifik olun: Eğer bir durum iki farklı şekilde anlatılabiliyorsa, hangisini kullanacağınıza karar verin ve raporunuzu bu doğrultuda yazın.
    * Herşey olsun: Hata ile ilgili olabildiğince fazla bilgi vermeye çalışın. Fazla bilgi verdiğinizi düşünüyorsanız düşünmeyin, geliştirici gereksiz olan bilgileri hata raporunu okurken eleyecektir. Eksik bilgi verdiğinizde, geliştirici size geri dönüp sorular soracak ve hatayı çözmek için zaman kaybedecektir.
    * Kapalı anlamlara dikkat: O, onlar, buraya, pencereyi gibi kelimeleri  kullanmamaya çalışın. Açık ve net olun. Örneğin: "X uygulamasını açtım, bir uyarı penceresi çıkardı ve sonra kapatmaya çalıştım, çöktü." Burada kapatılan uygula mıdır yoksa uyarı penceresi midir?  Bu örnek yerine: "X uygulamasını başlattım, bir uyarrı penceresi çıkardı. Daha sonra uyarı penceresini kapatmaya çalışırken, X uygulaması çöktü." Bu cümle biraz uzun ve tekrarlı olmasına rağmen, açık ve anlaşılır bir cümledir ve yanlış anlamaya mahal vermemek.
    * Yazdığınızı Okuyun: Hata raporunu göndermeden önce mutlaka okuyun ve açık olup olmadığını sorgulayın. Eğer hatayı gerçekleyen bir çok durum listelediyseniz, kendi kendinize bu yazmış olduğunuz sırada hatayı tekrar etmeye çalışın. Bu sayede herhangi bir adımı kaçırıp kaçırmadığınızı görebilirsiniz.
