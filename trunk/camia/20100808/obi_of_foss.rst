Açık Kaynak Topluluklarının Organizasyonel Davranışları ve  Güvenli ve Kaliteli Yazılımları
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Yazar:** Semen Cirit

Özet
====

Açık kaynak toplulukları ilginç bir şekilde güvenli ve kaliteli yazılımlar üretmektedir. Bu makalede, topluluklarının ve geliştirme ortamının tamamıyla açık olduğu bir yazılımın nasıl güvenli ve kaliteli bir şekilde üretilebileceğini açıklamaya çalışacağız. Bir özgür yazılım projesi olan Pardus Linux Dağıtımının organizasyonel davranışı ile yazılım kalitesi ve güvenilirliği arasındaki bağ anlatılacaktır. 

Şu ana kadar edindiğimiz topluluk geçmişi deneyimlerine dayanarak diyebiliriz ki; bir açık kaynak projesinde, yazılımı kullanan katkıcıların çokluğu, iletişim ve bilgi akışının tamamıyla açık olması güvenli ve kaliteli yazılım üretilmesini sağlamaktadır.

Giriş
=====

Açık kaynak toplulukları farklı ilgi, eğilim ve becerileri olan yüzlerce, bazen binlerce gönüllü kişinin oluşturduğu gruplardır. İlginç bir şekilde, bu gönüllü kişilerden oluşmuş toplulukların üyeleri, neredeyse hayatları boyunca sanal ortam dışında ve birbirleriyle hiç yüz yüze görüşmeden, bir ekip olarak; büyük, karmaşık ve güvenilir yazılım projeleri geliştirmekte ve iyileştirmektedirler. Üstelik bu projeler birçok bireysel, kurumsal ve devletsel alanda dünya çapında kullanılmaktadır.

Pardus depolarında yaklaşık olarak 4,500,000 satır kod bulunmasına karşın, Pardus'u kullanan tüm kullanıcılara açık olan hata takip sisteminde raporlanan hata sayısı yaklaşık 1500 civarındadır.  Bu raporlanan hataların yaklaşık 200 kadarı yeni özellik bildirimlerini oluşturmaktadır. Bu durumda 100 satır başına düşen hata yoğunluğu yaklaşık olarak 0,031 bulunmaktadır[1].
Bu iyi sonuç karşısında aklımıza bir takım sorular takılabilmektedir: Bu gibi bir davranış nasıl bir yazılım projesi olarak sonuçlanabilir? Kararları kim vermektedir? Yazılım projesi sürecinde karşılaşılan anlaşmazlıklar nasıl çözülmektedir? Ortaya çıkan projenin kalitesi ve güvenilirliği nasıl garantilenmektedir?
[2]Dünyanın diğer bir ucunda bulunan hiç tanımadığınız bir yabancı, bir yama gönderebilir ve bu sizin geliştirmekte olduğunuz yazılımda bulunan bir hatayı çözebilmektedir. Açık kaynak yazılımların hız aldığı nokta burasıdır, bir hata ortaya çıktığında, birçok kullanıcının elinde bulunan kaynak kod, birden bire birilerinin elinde bir cevhere dönüşmekte ve hata hemen çözülebilmektedir. Peki bu yapılan değişikliğin kabul edilme ve tüm kullanıcıların karşısına çıkma süreci nasıl işlemektedir?

Bu makale ile, bu süreci, Pardus Linux Dağıtımının  organizasyonel yapısı ile güvenli ve kaliteli yazılım üretmenin arasındaki ilişkiyi açıklayarak, anlatmaya   çalışacağız.

Organizasyonel Davranış
=======================

Bu bölümde sırası ile organizasyonel davranış ve yapı, topluluk, topluluk oluşumu ve büyümesi ve toplulukta etik kavramlarından bahsedilecektir.

Organizasyonel  Davranış
------------------------

Belirli bir organizasyonun etkili ve verimli çalışması için kişiler, gruplar ve organizasyon yapılarının birbirleri arasındaki etkileşimini inceleyen  çalışma alanıdır.

Organizasyonel davranışın temelinde;

#. Organizasyon içerisinde bulunan üyeler arası iletişim ve etkileşim
#. Organizasyon içerisinde bulunan üyelerin var olma amacı
#. Organizasyon üyelerini motive eden unsurlar
#. Organizasyon içi etik kısıtlar
#. Organizasyon arası bilgi akışı ve organizasyonu etkili bir hale getirmek için bir bilgi birikimi oluşturmak yer almaktadır.

Organizasyonel davranış model olarak ilk önce bireyleri daha sonra grupları ve en son olarak da organizasyonların davranışlarını incelemekte; üretimi arttırmayı ve emek veren kitlenin motivasyonunu ve memnuniyetini ve bulunduğu organizasyona bağlılığını arttırmayı amaçlamaktadır.

Organizasyonel Yapı
-------------------

Bir organizasyonun yapısının oluşmasında çevresindeki ekosistem  büyük etkiye sahiptir. Çünkü organizasyonun güç bulacağı nokta ekosistemidir.
Ekosistemi ile etkileşim halinde olan organizasyonlar daha çabuk değişebilen ve gelişebilen bir yapıya sahiptir [4].

Bu ekosistemlere bağlı olarak farklı organizasyon yapıları oluşmuştur. Pardus'un bulunmuş olduğu ekosistem, bilgi paylaşımının ve iletişimin tamamıyla açık olduğu özgür bir sistemdir. Bu ekositem içerisinde oluşmuş bir organizasyonel yapı kendi kendine öğrenebilir ve gelişebilir bir yapı olarak ortaya çıkmıştır.

Kendi kendine öğrenen organizasyonlar, harekete geçmek için organizasyon üyelerinin gelişmesini amaçlar.  Bu nedenle öğrenen organizasyon  yaratıcılığı arttırma amacı güderek, devamlı olarak organizasyon içerisinde bulunan bireylerin tecrübelerini artırmaya çalışır.

Topluluk
--------
Kendi kendine öğrenen organizasyonlar bir topluluk etrafında toplanmıştır.  Bir organizasyon, hayat boyu öğrenici, değişikliklere karşı ilgili, karşıtlıklara karşı  yapıcı ve farklı birçok alternatif olguya karşı bilinçli olabildiği sürece topluluk olarak tanımlanabilmektedir.  Topluluk belirli bir unsur çerçevesinde sonsuz bir iletişim sağlayabilen insan topluluğudur [3].

Topluluğun Oluşması ve Büyümesi
-------------------------------
Belirli bir amaç için oluşturulan bir organizasyonun başlangıcında, heyecan, yenilikçilik, yaratıcılık ve sıkı sıkıya bir birliktelik ve anlaşma bulunmaktadır. Fakat zaman içerisinde organizasyon hem yaptığı iş hem de üyeleri bakımından büyümekte ve farklı düşüncelere sahip olan bireyler ortaya çıkmaktadır. Bu dönem içerisinde farklı fikirlerin ortaya çıkışı bir organizasyonun iyiye gitmesi ve gelişmesi için olumludur. Fakat bu farklı fikirlerin ortaya çıkışı sırasında gerçekleşen tartışmaların çeşidi ve türü çok önemlidir [5].

Bu türler genel olarak iki şekilde ifade edilmektedir:

**Fonksiyonel tartışma:** Organizasyonun amaçları doğrultusunda olan bir konu hakkında, bireylerin bilgi ve becerileri ile nesnel olarak fikirlerini belirttikleri tartışma türleridir. Bu tip tartışmalarda farklı bakış açıları, yapılacak olan işin tüm yönleri ile görülmesini ve  işin performansının artmasını sağlamaktadır.

**Duygulanımlı Tartışma:** Bu tip tartışmalar, bireyler arasında çeşitli nedenlerden dolayı ortaya çıkan ve öznel  bilgileri içeren ve duygusal bir bakış açısı ile yapılan tartışmadır. 

Bu iki tür tartışmanın organizasyon için yararları ve aynı zamanda zararları bulunabilmektedir. 

Avantajları:
^^^^^^^^^^^^

* Üretkenliği arttırır: Tartışma yaşayan gruplar yaşamayanlara göre daha hızlı bir büyüme çizgisine sahiptirler.
* Sürü psikolojisinin olmasını engeller: Fonksiyonel tartışmalar organizasyon üyelerini doğru düşünme, kritize etme ve alternatif yaratma gibi konularda tetikler.
* Yaratıcılığı arttırır: Fonksiyonel tartışmalar merak ve ilgiyi arttırmaktadır.
* Devamlılığı arttırır: Bir organizasyon içerisinde tartışma bir konu hakkında iyi ve kötü yönlerin iyi bir şekilde ortaya çıkmasını ve adil bir dengenin oluşmasını sağlar.

Dezavantajları:
^^^^^^^^^^^^^^^
* Duygulanımlı tartışmalar yıkıcı ve güçlü negatif etki yaratıcı,  körü körüne bir düşünceye bağlanma ve bu şekilde bir dayanışma oluşturma ve bu uğurda agresifleşmeye yol açmaktadır.
* Duygulanımlı tartışmalar isteksizliğe neden olabilmektedir: Herkes düşüncesini belirtmek için kendi değer yargıları ve ilgi alanlarına sahiptir.  Fakat nesnel olmayan tartışmaların yaşandığı organizasyonlarda bireysel değer yargıları incinmekte ve bu da isteksizliğe neden olmaktadır.
* Duygulanımlı tartışmalar toplulukların devamlılığını tehlikeye sokabilirler: Bir topluluğun başarısının tartışmaları çözme yönteminin kolaylığı ve  var olmasına bağlı olduğu söylenmektedir.

Bir topluluğun oluşma evresi dört aşamada gerçekleşmektedir. İlk evre farklı düşüncelerin ve karşı çıkışların ortaya çıkmasıdır. Bu evrede yukarıda da bahsetmiş olduğumuz tartışmalar yaşanmakta, farklılıklar oluşmakta ve topluluk kavramı organizasyon için oturmaya başlamaktadır. Bir sonraki evre ise bireylerin farklılıklarının tam anlamıyla ortaya çıktığı ve netleştiği evredir. Bu evrede topluluğu iyiye götürecek birçok farklı düşünce üretilmekte ve denenmektedir. Bu evre aynı zamanda topluluğun iletişimin geliştiği ve iletişim yapısının oluştuğu evredir. Üçüncü evre ise topluluğun iletişimi ve öğrenim yapısı ve farklılıkları düşünülüp, topluluğun ekosistem ile nasıl etkileşime geçeceğini ve kendi arasında yönetilebileceğini anlatan  kuralların oluşturulduğu ve standartlaştırıldığı dönemdir. Bu dönem içerisinde topluluk içerisinde yapılan iş ve nitelik farklılıkları oluşup alt gruplara ayrılabilmektedirler. Bu kurallar sayesinde kaotik olan süreç sona ermekte ve herkesin topluluk içerisinde mutlu bir şekilde var olduğu, kendini ve çevresindekileri geliştirebildiği bir ortam oluşmaktadır. En son evre, topluluk içi farklılıkların kucaklaştığı, topluluğun öğrenme, büyüme ve yaratma hızının devamlılığının sağlandığı ve  topluluk var olduğu sürece yeni durum ve risklerin oluşması ile tekrarlanarak devam edecek bir evredir.

Toplulukta Etik
---------------
Topluluk oluşumu ve büyümesi gerçekleşirken bir kurallar bütünü oluşumundan önceki bölümde bahsetmiştik. Topluluk ve içinde bulunduğu bireylerin yararına ve yapılan işin daha sağlıklı düşünceler ile oluşmasına olanak sağlayacak olan görünmez sisteme etik demekteyiz.

Etik kendi kendine öğrenen bir topluluğun sağlıklı büyümesi, devam etmesi ve kaliteli işler çıkarabilmesi için önemlidir. Topluluk bu kurallar doğrultusunda yeni bireyeler kazanır, yeni oluşumlar sağlar ve etkin ve etkili bir şekilde bilgisini paylaşıp, yaratıcılığını ortaya çıkarır, güvenilir ve kaliteli işler çıkarabilir.

Pardus Topluluğu
================
Pardus Topluluğu'nun bu gibi topluluk oluşumu süreçlerinin bir kısmından geçtiği ve bir kısmından geçeceği kuşkusuzdur.

Pardus 2010 yılı içerisinde beşinci yılını kutlamış genç bir projedir. Burada genç dememizin nedeni, topluluk oluşum safhasının ilk aşamasını geçiği ve ikinci aşamasından çıkmak üzere olduğu ve diğer kısımları için yola çıktığıdır.

Pardus Topluluğu son iki yıldır belirli değişikliklere sahne olmakta ve çeşitli geliştirme süreçlerinde yeniden yapılanma yoluna gitmektedir.

Bu yeniden yapılanmanın nedenleri[6]:

* Topluluğun gelişimi ve yeni bireylerin katılımı için öğrenme mekanizmasını daha aktif kullanmak.
* Topluluk içi bilgi birikimi oluşumunu sağlamak.
* Yapılan işin izlenebilirliğini ve kontrolünü arttırmak ve tüm bireyleri bu işten haberder etmek
* Topluluk bireylerinin motivasyonun bağlılığını arttırmak

Yukarıda anlatılan nedenlerin hepsi aynı zamanda işin güvenilirliğini ve kalitesini arttırmaktadır.

Bu yukarıda sıralamış olduğumuz tüm nedenler doğrultusunda  topluluk içerisinde uygulanmakta olan ve yeniden yapılanma içerisine girmiş olan kavramlardan ve yararlarından bahsedilecektir.

Katkıcı
-------

Pardus'un geliştirme süreçleri içerisinde yapmış olduğu işlerin zamanla belirli farklılıklar içerdiğinin gözlemlenmesi ve kendi arasında amaç farklılıkları oluşması nedeni ile daha önce genel olarak geliştirici kavramı içerisinde olan birçok kavram ayrıştırılma ve farklı gruplar oluşturulma yoluna gidilmiştir. Böylece Pardus topluluğu içerisinde katkı veren her bir bireye katkıcı denilmiş ve katkıcı kavramının alt bölümleri ise farklı amaçlara sahip gruplara ayrılmıştır. [7]

Bu gruplar şu hali ile geliştirme, test, çeviri, belgeleme, görsel tasarım, tanıtım şeklindedir.

Toplulukta bulunan her bir birey sadece bir gruba dahil olabileceği gibi aynı anda birden fazla gruba da dahil olabilmektedir. 

Sorumlulukları
^^^^^^^^^^^^^^

Pardus Projesi var olduğundan bu yana katkı sağlayan her bir bireyin yapılan işe ve topluluğa karşı sorumluluklarının bulunması gerektiği düşünülmüştür. Bu sorumluluklar bireyler arası ilişkiyi güçlendirici, iletişimi ve bilgi akışını arttırıcı niteliktedir.

**Devamlılık:**

Bir katkıcının üzerinde çalıştığı projelerde sürekli olarak çalışabilmeyi göze almasıdır. Burada süreklilik ile ifade edilen 7/24 bir çalışma değil, fakat üzerinde çalışılan konunun devamlılığının sağlanmasıdır.

**Doğruluk:**

Proje içerisinde birden fazla katkıcı aynı konu üzerinde çalışıyor olabilir. Bunun yanında bir katkıcının yaptığı işten bir diğerinin etkilendiği durumlar da olabilir. Bu yüzden yapılan çalışmaların yalnızca sürekliliği değil, diğer katkıcıları etkilediği oranda doğruluğu da önemlidir. 

**Kararlılık:**

Yapılan işte sık karar değişiklikleri yapılmamalıdır. Kararın sık bir şekilde değiştirilmesi, diğer katkıcıların gelişimi takip etmesini, fakat daha önemlisi o çalışmaya bağımlı olan katkıcıların çalışmalarını güçleştirecektir. Bu yüzden kararlar iyi düşünerek ve diğer katkıcıların de fikirleri alınarak verilmelidir.

**İletişim:**

Alınan kararlardan, küçük de olsa yapılan değişikliklerden diğer katkıcıları haberdar etmek gerekmektedir. Böylece ortak iş yapan katkıcılar daha uyumlu ve hızlı bir şekilde çalışabilmekte ve yeni katkıcılar da yapılan işi izleme imkanı bularak çalışılan konuya daha kolay adapte olabilmektedirler.

Bu iletişim ve bilgi akışı sayesinde yapılan çalışmada sorun yaşanılan bir noktada daha fazla fikir beyan edilebilmekte ve daha hızlı çözüm üretilebilmektedir.

Katkıcı alma ve yetiştirme sürecinin önemi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pardus Projesine katılmak isteyen her bir birey belirli bir bilgilendirme sürecinden geçmektedir. Bu süreç bilgi akışını katkıcı adaylarına aktarabilmek adına oluşturulmuş bir süreçtir. Oluşturulmuş sistem sayesinde her bir adaya katılmak istediği alan doğrultusunda bir mentor atanmakta ve mentoru ile geçirdiği dönem boyunca gerekli tüm bilgiyi hızlı bir şekilde öğrenmesi sağlanmaktadır. Ayrıca mentorlar adayı bu dönem içerisinde izleyerek katkıcı sorumluluklarını yerine getirip getirmediğini de takip etmektedirler [8].

Pardus için katkı sağlayacak her bir bireyin topluluk içerisinde sorun yaşamadan çalışmalara katılması, verimli ve mutlu bir şekilde çalışması, sağlıklı iletişim kurması ve böylece kaliteli ve güvenilir iş çıkarabilmesi sağlanmaya çalışılmaktadır.

Hata Takip Sistemi
------------------

Hata takip sistemleri geliştirici ve kullanıcı arasında bir köprü oluşturarak, yaşanılan problem hakkında bilgi alışverişini ve çözüme kavuşması için yol göstericiliğini sağlamaktadır [9].

Bu bilgi alışverişinin iyileştirilmesi, hatanın hızlı çözümü ve dolayısı ile yapılan işin kalitesini arttırmaktadır.

Hata Raporlamak
^^^^^^^^^^^^^^^
Sistemin hızlı ve etkili kullanabilmesi, bilinçli hata raporlayan kullanıcıların çokluğuna bağlıdır. Hata takip sistemi deneyimlerimize dayanarak söyleyebiliriz ki, iyi raporlanmış ve kullanıcı, geliştirici bilgi alışverişinin hızlı olduğu hataların çözülme hızı diğerlerine göre fazladır[10].

Bu durumda, iyi hata raporlayan geniş bir kullanıcı kitlesi, yapılan işin kalitesini olumlu yönde etkileyen etmenlerden biridir denebilir.

Hata Kontrolü
^^^^^^^^^^^^^
Raporlanan hataların düzenli olarak gözden geçirilip, hangi tip hata olduğunun, öneminin ne olduğunun, eksik bilgiler içerip içermediğinin kontrol edilmesi, hata eğer kritik veya önemli bir hata ise,  hızlı bir şekilde çözüme  kavuşmasını sağlar [11].

Bilgi Kontrolü
---------------
Projenin her bir aşamasında birçok farklı gözün yer alması, yorumunu iletebilmesi ve bunların düzenli hale getirilmesi iş kalitesini ve güvenilirliğini arttırmaktadır. 

Pardus Projesi yaptığı işleri farklı süreçlerden geçirerek kalite ve güvenilirliğini daha iyiye götürmeyi amaçlamaktadır. 

Kod Gözden Geçirme
^^^^^^^^^^^^^^^^^^

Pardus'ta bulunan yazılımların (paketlerin) geliştirme deposuna alınmadan önce diğer geliştiriciler tarafından onay aldığı bir süreç bulunmaktadır. Bu onay sırasında paketin Pardus'un paket politikalarına uygun olup olmadığı tecrübeli geliştiriciler tarafından gözden geçirilmektedir. [12]

Bu süreç sayesinde Pardus paket depolarında, paket kalitesini arttırıcı nitelikte alınmış kararların dışına çıkılmamış olunmaktadır.

Güvenlik Süreci
^^^^^^^^^^^^^^^
Pardus depolarında bulunan özgür yazılımların güvenlik açıklarını takip etmek ve bu açıklıkların kapatılmasını sağlamak için bir güvenlik ekibi oluşturulmuştur. Bu ekip diğer dağıtımlar ile ortak çalışır ve vendor-sec, oss-security gibi e-posta listelerini takip ederek, güvenlik açıklarının takibini gerçekleştir. 

Bu süreç sayesinde hızlı bir şekilde güvenlik açıkları ortaya çıkarılmakta ve geliştiricileri tarafından kapatılmaktadır.

Test Süreci
^^^^^^^^^^^
Kararlı depoya aktarılacak ve kullanıcı karşısına çıkacak olan her paket test sürecinden geçmek zorundadır. 

Bu amaç doğrultusunda Pardus test ekibi oluşturulmuştur [13]. Bu ekip sayesinde güvenlik güncellemeleri testleri ve düzenli olarak takip edilen kararlı depo testleri gerçekleştirilmekte ve paketlerin sistem içerisinde düzgün çalışıp çalışmadığının testi yapılmaktadır.

Sonuç
=====
Pardus topluluğu ve oluşturmuş ve oluşturmakta olduğu süreçler; sağlıklı iletişimi, karşılıklı bilgi aktarımını ve birikimini iyileştirmeyi, etkili ve bilinçli büyümeyi amaçlamaktadır.  

Bu amaçlarının varacağı nokta dünyanın herhangi bir yerinden geliştirme süreçlerine katılmış ve farklılıkları olan birçok bireyin aynı çatı altında güvenli ve kaliteli işler çıkarmasıdır.

Teşekkür
========
Bu yazıyı yazarken yardımlarını esirgemeyen ve geçmiş deneyimlerini paylaşan Pardus topluluğu üyelerine teşekkürlerimi sunarım.

Kaynaklar
=========
- [1] Geek.net, “Pardus Linux”,  http://www.ohloh.net/p/pardus-linux/analyses/latestTrans. , 2010.
- [2] Con Zymaris,  “Linux security strong as ever”, http://www.zdnet.com/news/linux-security-strong-as-ever/298545. , 2010.
- [3] David S. Walonick,  “Organizational Theory and Behavior”, http://www.survey-software-solutions.com/walonick/organizational-theory.htm. , 2010.
- [4] Knowledge Jump Production,  “Leadership and Organizational Behavior”, http://www.nwlink.com/~donclark/leader/leadob.html. , 2010.
- [5] Ruben van Wendel de Joode,  “Managing Conflicts in Open Source Communities” , 2010.
- [6] Carla C.J.M. Millar, Chong Ju Choi and Edward T. Russell, Jai-Boem Kim,  “Open source communities: an integrally informed approach” , 2005.
- [7] Pardus Linux,  “New Contributors”, http://developer.pardus.org.tr/guides/newcontributor/index.html. , 2010.
- [8] Pardus Linux,  “How to be a Contirbutor?”, http://developer.pardus.org.tr/guides/newcontributor/how-to-be-contributor.html. , 2010.
- [9] Pardus Linux,  “Bug Tracking Guide”, http://developer.pardus.org.tr/guides/bugtracking/index.html. , 2010.
- [10] Pardus Linux,  “Bug Tracking System”, http://bugs.pardus.org.tr. , 2010.
- [11] Pardus Linux,  “Bug Tracking System”, http://developer.pardus.org.tr/guides/bugtracking/howto_bug_triage.html. , 2010.
- [12] Pardus Linux,  “Bug Tracking System”, http://developer.pardus.org.tr/guides/packaging/package-review-process.html. , 2010.
- [13] Pardus Linux,  “Bug Tracking System”, http://tr.pardus-wiki.org/Pardus:Test_Ekibi. , 2010.
