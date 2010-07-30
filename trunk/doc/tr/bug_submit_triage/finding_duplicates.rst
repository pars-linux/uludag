Aynı hataların yakalanması
==========================

Hataların özgün ve tekrarlanabilir olması en önemli konulardan biridir. Bu yüzden bir hata raporlanmadan önce hatanın aynısının bulunup bulunmadığı kontrol edilmelidir. Eğer hata birden fazla kez raporlanmış ise hatalar aynısı olarak işaretlenmelidir.

En çok karşılaşılan hatalar:

    * `En sık raporlanan hatalar listesinden <http://www.python.org/>`_.
    * Sürüm adı ile açılmış takip (tracker) hatalarından kolayca bulunabilir.

Bugzilla arama arayüzünü kullanarak hata bulmak
-----------------------------------------------
`Belirli hata bulma arayüzü <http://bugs.pardus.org.tr/query.cgi?format=specific>_` basit anahtar kelimelere göre arama yapmanızı sağlar.

`Ayrıntılı hata arama arayüzü <http://bugs.pardus.org.tr/query.cgi?format=advanced>_` ilk bakışta biraz karışık görünebilir. Fakat çok iyi bir arama arayüzüdür, sadece aramak istediğiniz kriterleri belirleyip diğer alanları boş bırakarak arama yapabilirsiniz. Boş bıraktığınız alanlar aramanızı kısıtlamayacak, sadece seçmiş olduğunuz kriterler doğrultusunda hataları listeleyebileceksiniz.

Durum bölümü için öntanımlı olarak YENİ, ATANDI, TEKRAR AÇILDI kısımları seçili gelmektedir. Bu hatalar çözümlenmemiş hataların tümünü kapsamaktadır.

Özet alanına hata ile ilgili bir kelime veya kısa bir cümle girebilirsiniz. Örnek: Examples: ekran ayarı, masaüstü. Eğer arama alanına birden fazla kelime giriyor iseniz ve eğer bu bir cümle değil ise, arama tipinizi dizgeyi içerir seçeneği yerine, dizgelerin tümümü içerir veya dizgelerin herhangi birini içererir olarak değiştirebilirsiniz.

Anahtarlar bağlantısının üzerine tıklayıp anahtarları görmeden, herhangi bir anahtar kelime girmeyiniz: Bu alanda sadece daha önce tanımlanmış olan anahtar kelimeler aratıldığında sonuç dönebilmektedir.
Eğer listede bulunmayan bir anahtar kelime ile arama yaparsanız sonucun boş döndüğünü göreceksiniz. Pardus'ta kullanılabilirlik, çeviri, görsellik ile ilgili sorunlar, yeni özellik istekleri, eksik raporlanmış hatalar için anahtar kelimeler bulunmaktadır.

Ayrıca arama sayfasının at bölümünde grafiksel olarak arama yapabileceğiniz "mantıksal ifade ile gelişmiş arama" bölümü de bulunmaktadır. 

Eğer hatanın aynısını yakaladıysak ne yapmalıyız?
-------------------------------------------------

Siz eğer Pardus hata yakalama ekibi üyesi veya geliştiricisi iseniz, hatayı en az derecede açıklayan raporu veya raporları KAPATILDI/AYNISI olarak işaretlemeli ve en iyi açıklamaya sahip olan hatanın numarasını hataya eklemelisiniz. 

Eğer raporlamadığınız hataları değiştirme yetkisine sahip değil iseniz, hataya yorum olarak aynısı olan hata numarasını ekleyebilirsiniz, biri bunu görecek ve gerekli işlemi yapacaktır.
