Çeviri Süreci
=============

Pardus, kendi yazdığı araçların ve paketlerin çevirilerini 
Transifex çeviri ortamı üzerinden yapmaktadır. Çevirmen olmak 
için gereken adımlar aşağıda açıklanmıştır:

#. İlk adım olarak Transifex'e üye olunur. Üye olan kişinin e-posta 
adresine onay e-postası gönderilir. E-posta adresini doğrulandıktan 
sonra kişi mutlaka kişisel bilgilerini doldurmalıdır. Kişisel bilgiler 
gönderim (commit) kaydında görünecektir.

#. Çevirmen hangi dilde çeviri yapmak istiyorsa o dil için çeviri takımı
üyesi başvurusu yapar. Çeviri takımı daha önceden oluşturulmamış ise 
çeviri takımının oluşturulması için istekte bulunur.

#. Daha önceden bir takım oluşturulmuş ve bu takıma bir koordinatör
atanmış ise çeviri takımı üyesi başvurusu yapılır.

#. Koordinatör veya çeviri takımı üyesi başvurusunda bulunan kişiye 
çeviri becerisini sınama amaçlı küçük bir sınav yapılır. (?)

#. Testi geçen kişinin başvurusu onaylanır ve kişinin Transifex 
arayüzünde yaptığı değişiklikleri, projelerin po dosyalarına doğrudan
yansıtabilme yetkisi verilmiş olur.

#. Çeviri üyelerine SVN hesabı verilmez. Transifex üzerinde yapılan 
değişiklikler "translator" SVN kullanıcısı tarafından depoya yansıtılır.

#. Koordinatörlere SVN hesabı verilebilir. (?)

#. Çeviri üyeleri ve koordinatörleri arasındaki iletişim e-posta listesi
üzerinden yapılır. Türkçe çeviri tartışmaları turkce@pardus.org.tr, 
diğer diller için pardus-translators@pardus.org.tr üzerinden yapılır.

#. Her projenin farklı koordinatörleri olabileceği gibi bir projenin 
birden fazla koordinatörü de olabilmektedir. Çevirmenlerin bir dosyayı 
çevirmeden önce koordinatörlerle e-posta listesi üzerinden iletişime 
geçmesi her zaman tercih edilmelidir.

#. Çevirmenin çevirmek istediği po dosyasının "kilitli" durumda 
olup olmadığını kontrol etmesi, bir başka çevirmenin ayağına basmaması 
açısından faydalıdır.

#. Çevirmenin çevirmek istediği dosya kilitli değilse, yani bir başka 
çevirmen bu dosya üzerinde çalışmıyorsa, dosya önce "kilitle" düğmesine 
basılarak kilitlenmeli ardından çeviriye başlanmalıdır.

#. Çevirisi tamamlanan dosyanın kilidi mutlaka kaldırmalıdır. Kilitli 
görünen dosya, üzerinde çalışılan dosya anlamına gelmektedir.

#. Her çevirmenin kendi diline ait çeviri dosyasını "izlemesi" yararına
olacaktır. Proje geliştiricileri çeviri dosyalarında değişiklik yaptığında 
çevirmenlerin bu değişikliklerden haberdar olması için bu özelliği 
kullanmaları gerekmektedir.

#. Projelerin genel çeviri durumu haftalık olarak proje koordinatörlerine 
gönderilecektir. (?)

