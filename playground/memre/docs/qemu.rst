==============
QEMU ARM NASIL
==============

Giriş
-----
qemu, çeşitli platformlar için system ve linux-user mode olmak üzere iki
farklı emulasyon desteği sunmaktadır. Gerek alt sanallaştırılmış bir
sistemi rahat yönetmekte olsun gerek farklı bir mimarinin çalıştırılabilir
ikililerini çalıştırmakta olsun çok farklı alanlarda qemu kullanılabilir.

Birçok geliştirme ortamı için güzel bir emulator olan qemu Linaro projesi
ile birlikte ARM platformunda daha fazla aygıt desteği kazanmış durumda.

qemu ayrıca kvm desteği ile birlikte oldukça performanslı bir şekilde
sanallaştırma yapıp sistemimize farklı işletim sistemlerini yükleyip test
yapmamıza olanak sağlamaktadır. Bunların yanında kernel geliştiricileri için
de güzel bir debugger olarak kullanılır.

Bu belgede qemu-arm linux-user modu ve system emulation modlaru üzerinde
duracağız.

qemu modları
------------

qemu nun hali hazırda 2 adet modu bulunmakta. Bunlardan ilki, şeffaf çapraz
inşada kullandığımız linux-user modu, diğeri ise system modudur.

linux-user modunda, linux için derlediğiniz bir ikiliyi (binary)
çalıştırabilirsiniz. Bu ikilinin dinamik yükleyicisi ve bağımlı olduğu
kitaplıkları bir ``sysroot`` dizini içerisine yerleştirip ``qemu`` nun
bu kitaplıkları kullanabilmeleri sağlanabilir.

qemu'nun system modunda ise, bir sistemin tam bir emulasyonu yapılır.
Örneğin bir 8086 sistemde bütün giriş-çıkış aygıtları, hazırlanmış sanal
mikroişlemciye kesmeler yollayarak (IRQ) iletişim sağlar, bütün PCI kartları
emulasyonları gerçek bir 8086 sisteminde nasıl davranıyorsa aynı şekilde
davranış gösterir. Sistem ilk boot edildiğinde ``bios`` 'un belleğe yüklenip
sistemi ilklendirme durumuna kadar her şey birebir emule edilmiştir.

8086 sistemleri belirli standartlara sahiptirler. Bir 8086 sistemi ilk
açıldığında öncelikle bios belleğe yüklenir ve bir boot device arar. Bu boot
device'ı bulduğunda, bu device'ın ilk 512 byte'ını belleğe yükleyip bu
bellek bölgesine jump eder ve bundan sonraki işlem bu 512 byte'daki kodlar
sayesinde yürütülür. Bu kısım MBR (master boot record) olarak bilinir.

MBR'da bulunan uygulama standart olarak bir ``önyükleyici`` veya bootloader
olarak imlemente edilir (tabii ki kendiniz ufak bir kod parçası yazıp istediğiniz
işlemleri yaptırabilirsiniz). Önyükleyici olarak GRUB'ı örnek verecek olursak,
GRUB konfigurasyonuna göre bir linux çekirdeğini ve varsa bu çekirdeğe ait bir
ramdiski belleğe alır ve linux çekirdeğinin yüklendiği bellek bölgesinin
ilk sektörüne jump eder, bundan sonraki iş çekirdek tarafından yapılır. Veya
başka bir partisyonda bulunan ve desteklenmeyen bir çekirdek için, 
o kerneli yükleyecek olan önyükleyici belleğe yüklenip bu önyükleyicinin
bulunduğu ilk sektöre jump edilip görev devredilir.

qemu'nun yaptığı, kullandığı bellek bölgesine daha önceden oluşturulmuş
bios'u yükleyip, sanal bir işlemci üzerinde bu bellek bölgesindeki
uygulamaları çalıştırmaktır (virtualization destekli bir mikroişlemciniz
varsa ve çekirdeğiniz destekliyorsa, qemu emulation işlemlerini daha farklı
şekilde yönetir, konu dışı olduğundan üzerinde durmuyorum).

qemu'nun ARM için implemente edilen system modu 8086 sistemi kadar rahat
bir çalışma ortamı sağlamaz. Çünkü amaçları itibariyle bir ARM sistemleri
birbirlerinden oldukça farklı olabilirler.


-arm'ın system modunda da belirli platformlar implemente edilmiştir. ARM
sistemleri 8086 sistemlerine kıyasla biraz daha farklı çalışmaktadır.
İçerisinde ARM çekirdeği bulunduran birçok platformun implementasyonu ayrı ayrı
gerçeklenmektedir.

(will be continued..)
