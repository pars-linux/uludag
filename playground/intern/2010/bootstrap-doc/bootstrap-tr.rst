
================================================
Temel Derleme Sistemi Oluşturulması (Bootstrap)
================================================



Bu belge, Pardus 2011 sürümü için 32/64-bit işlemci mimarisi üzerinde yapılan temel derleme sistemi oluşturma (bootstrap) adımlarını ve yöntemlerini içermektedir. Derleyiciler ve programların derlenmesi/çalışması için gereken kitaplıklar da derlenecek programlama dilinde yazılmaktadırlar. Bu araçlar bir üst düzeye çıkarılmak istenildiğinde önce çalışan eski sürüm üzerinde işe başlanır. Bu işlemde eski sürüm bir iç derleyici oluşturup kendini bu iç derleyici ile derleyerek yeni sürüme yükseltilir. Temel derleme sistemi oluşturma işlemi gcc ve glibc için yapılmak istenildiğinde, bu araçların birbirlerine olan bağımlılıkları oldukça fazla olduğu için her bir aracın derlenmesi için bir diğerinin derlenmesi gerekmektedir. Bir anlamda bir çember haline gelen bu temel araçların derlenmesi işlemine temel derleme sistemi oluşturulması denilir.  

Temel Derleme Sistemi Oluşturma Adımları
--------------------------------------------------------------------------------------------------------------
                                                                                                                                
- Temel derleme sistemi oluşturma işlemi için bilinmesi gereken temel kavramlar ve kullanılacak araçlara dair bilgi edinilmesi  
- Temel derleme sisteminin esas kısmı olan binutils, glibc ve gcc yazılımlarının derlenmesi                                     
- Yeni oluşturulmuş olan sistemin kullanılabilmesi için gereken başlıca yazılımların yeni sisteme kurulması                     
                                                                                                                                




Ön Hazırlık - Temel Kavramlar ve Kullanılan Araçlar
----------------------------------------------------
Temel derleme sistemi oluşturmaya geçmeden önce temel kavramlara göz atmak gerekmektedir. İlk olarak C dili derleme modeli ile başlanabilir.

Derleme işlemi ilk olarak önişlemci ile başlar. Önişlemci, oluşturduğu çıktı verilerinin başka bir programa girdi olarak üreten programa denir. Bu aşamada, kaynak kod dahil etme (#include), makro tanımı (#define) ve şartlı dahil etme (#if,#ifdef vb) işlemleri çözümlenir. 
Daha sonra derleyicinin oluşturduğu makine dili kodları makine dili derleyicisine iletilir, makine dili derleyicisinin oluşturduğu obje kodlar ve programın çalışması için kullanılacak kitaplıklar bağlayıcıya verilir. Bağlama işlemi sonucunda da çalıştırılabilir biçimdeki kod elde edilmiş olur. 

Bahsi geçen derleme modelini gerçekleyebilmek için kullanılan araçlardan kısa kısa bahsedilirse;

**binutils**
-------------
  makine dili derleme ve bağlama aracıdır. İçerdiği başlıca araçlar.

**ar**
  arşiv dosyası oluşturmak, değiştirmek ve arşivden bir şey açmak için kullanılır.
**as**
  taşınabilir bir GNU makine dili derleyicisi.
**ld**
  obje ve arşiv dosyalarını birleştirir, bu dosyaların içerdiği verileri konulması gereken yerlere koyar (relocate) ve sembol referanslarını bağlar. Genelde derlemenin son adımında ld çalışır.
**nm**
  obje dosyasındaki sembolleri listeler.
**objdump**
  obje dosyalarındaki bilgileri gösterir.
**ranlib**
  arşiv dosyasındaki içerik için bir index oluşturur ve arşivde tutar.


**pax-utils**
  ELF32/64 (executable and linkable format) dosyaları üzerinde güvenlik de dahil çeşitli denetimler yapabilen araçtır.


**strace**
  çalışan bir süreç ile ilşkili sistem çağrılarını gösteren araçtır. Bu süreç tarafından alınan veya çağrılan sistem çağrılarını, bu çağrılara verilen parametreleri ve dönüş değerlerini gösteren bir hata ayıklama aracıdır.


**C Bayrakları (CFLAGS)**
--------------------------
  GCC ve GNU Library C'nin derleme sırasında sistemin bazı özelliklerini yönetmek için kullandığı bayraklardır.

**-D_FORTIFY_SOURCE=2**
  özellikle string kullanılan yerlerde güvenlik açığına karşın kullanılır. 
**-O2**
  yazılımın boyutunu çok fazla büyütmeyen ve hata ayıklamayı engellemeyen eniyileştirmeleri açar. -O2 -O'dan daha iyidir ve çoğunlukla onun kadar güvenlidir. Pardus 2009 paketleri için de öntanımlı eniyileştirme seviyesi -O2'dir.
**-fomit-frame-pointer**
  gcc'nin üretilen kodun çerçeve gösterici onarımını (frame pointer maintenance) atlamasını sağlar, bu da kodun daha küçük ve hızlı olmasını sağlar.ayrıca bir yazmacı sonraki kullanımlar için boşaltır.
**-fstack-protector**
  yığın üzerindeki değişkenlerin yerini değiştirerek tampon bellek olarak kullanılan değişkenlerin taşma durumunda diğer değişkenleri etkilemesini önler. Fonksiyon dönüş adresinden önce rastgele bir değer atanmış koruma değişkeni yerleştirir. Fonksiyon bittiğinde bu değişken kontrol edilerek taşma olup olmadığı anlaşılır. Eğer değişiklik varsa programın çalışması durdurulur. Bu sayede fonksiyon dönüş adresini değiştiren hafıza taşma hatalarının kötüye kullanılması engellenir. 
**-march=<mimari>**
  gcc'nin belli bir mimari için eniyileştirme yapmasını sağlar. Yazılımları sadece kendiniz için derliyorsanız yazılımın üzerinde çalışacağı mimariyi belirterek bu mimarinin tüm özelliklerini kullanabilirsiniz.
**-mtune=<mimari>**
  gcc'nin eski sürümlerindeki -mcpu, -march bayrağına benzer ve aynı seçeneklere sahiptir. Bununla birlikte -mtune eski mimarilerle uyumu bozmaz. -mtune ve -march bayrakları bir arada kullanılarak istenilen sonuçlar elde edilebilir.
**-pipe**
  gcc'nin derleme yaparken geçici dosyalar üretmemesini sağlar. Bunun yerine veriler doğrudan bir sonraki fonksiyona aktarılarak derleme zamanında iyileştirme gerçekleştirilir.

**Bağlayıcı Bayrakları (LDFLAGS)**
-----------------------------------
  Bağlayıcının sistemin bazı özelliklerini yönetmek için kullandığı bayraklardır.

**-Bsymbolic-functions**
  dinamik bir kitaplık oluşturulurken, eğer kütüphane içerisinde global fonksiyon simgeleri varsa  referansları bunlara bağlamaya yarar.
**-Wl,--hash-style=gnu**
  bağlayıcının hash tablosunun tipini belirler, burada gnu seçilmiştir.
**--as-needed**
  bağlayıcıya üretilmiş olan çalıştırılabilir sonuç dosyası ya da başka kitaplıklardan, kitaplıkta bire bir kullanılmış olanları bağlamasını söyler.
**--sort-common**
  bağlayıcıya uygun çıkış bölümlerine yerleştirilmiş simgeleri boyutuna göre sıralamasını söyler. Bu bayrak simgeler ile sıralanma kısıtları arasındaki uçurumu önler.
**-Wl,-z,relro**
  en son oluşturulan ELF için salt-oku bir yeniden yerleştirme (relocation) tablosu ayırır.  -z parametresi tüm bu yeniden yerleştirmelerin çalışma zamanında çözümlenmesini sağlar (çalışma zamanında çözümlenme başlangıç yüklemelerinin gecikmesine neden olabilir). 
**-no-unneeded**
  bu bayrak kullanılarak inşa (build) sırasında tüm durumlar ele alınır.


Derleme sistemi için gereken ortamın hazırlanması
--------------------------------------------------
Bu aşamada, var olan sistem üzerinde yeni bir sistemin derlenmesi istenildiği için temel derleme sistemi oluşturma işleminin var olan sistem üzerinde kalıcı hasara sebep olması gibi olası tehlikeleri göz önünde bulundurulmalı ve uygun  bir yöntem seçilmelidir. Söz konusu yöntemlerden en uygunu -biraz uzun bir yol olsa da- var olan sistemde yalıtılmış bir bölüm yapılarak işlemlerin bu ortamda yapılmasıdır. Bunun için ilk olarak yeni bir kullanıcı oluşturulur. Bu uygulamada yeni kullanıcıya *bootstrap* adı verilmiştir, bundan sonraki işlemlerin neredeyse tamamı bootstrap kullanıcı alanında yapılacaktır. İlk olarak bootstrap alanında işlemlerin yapılacağı ve yeni sistemin kök dizin olarak kullanacağı dizinler oluşturulur.
::

    bootstrap@pardus ~ $ mkdir -p newroot/sysroot

Derlenecek programların kaynak kodlarının yer alacağı bootstrap alanında bir sources dizini, bir de programların derleneceği newroot altında src dizini oluşturulur.
::

    bootstrap@pardus ~ $ mkdir sources
    bootstrap@pardus ~/newroot $ mkdir src

Daha sonra sıklıkla kullanılacak olan altdizin, yol gibi değişkenleri *.bashrc* dosyasına kaydedip, artık o kabukta geçerli olan kısa yolları kullanabiliriz.
::

    bootstrap@pardus ~ $ vi .bashrc
    
.bashrc dosyası içerisine
::

    export TARGET=x86_64-pc-linux-gnu
    export CROSS_COMPILE=${TARGET}-
    export PREFIX=/home/bootstrap/newroot
    export SYSROOT=${PREFIX}/sysroot
    export PATH=${PREFIX}/bin:${PREFIX}/sysroot/bin:${PATH}
    export MYDESTDIR=/home/bootstrap/newroot/installdir
    export CC=${CROSS_COMPILE}gcc
    export AR=${CROSS_COMPILE}ar
    export RANLIB=${CROSS_COMPILE}ranlib
    export AS=${CROSS_COMPILE}as
    export LD=${CROSS_COMPILE}ld

yukarıdaki satırlar eklenir. Sırasıyla TARGET derlenilecek yeni sistemin mimarisini, CROSS_COMPILE derlenecek hedef sistem araçlarını, PREFIX işlemlerin yapılacağı yolu, SYSROOT yeni sistemin kök dizinini, PATH yeni sisteme dair yolları, MYDESTDIR temel araçlar derlendikten sonra derlenmesi gereken programların yer alacağı dizini, CC, AR, RANLIB, AS ve LD ise iç derleme sırasında kullanılması istenen sistemin araçlarını göstermektedir.

Binutils, GCC ve GlibC'nin Derlenmesi
--------------------------------------


GNU binutils
-------------
Yeni sistem için kullanılacak binutils programının kaynak kodu sources dizini içerisine indirilir ve newroot altındaki src dizini içine açılır.
::

    cd ${PREFIX}/src
    tar xvf binutils-xxx
    mkdir -p build/binutils-stage1
    cd build/binutils-stage1

buraya kadar kaynak kodlar src içerisinde açılıp, derleme için kullanılacak build dizini ve onun altında binutils'in olacağı binutils-stage1 dizini oluşturulmuş oldu. Bir sonraki adım artık binutils'in derleneceği adımdır.

::
  
    ../../binutils-xxx/configure --prefix=${PREFIX} --target=${TARGET} --with-sysroot=${SYSROOT}
    make
    make install

yukarıdaki adımlarda sırasıyla, src içerisne açılmış olan binutils kaynak kodları, programın yapılandırma ayarlarıyla yapılandırıldı burada verilen ek parametrelere bakılırsa daha önce .bashrc dosyasına eklediğimiz değişkenlerden yararlanılmıştır. Böylece binutils, verilen yol içerisinde hedef mimari ile yeni sistemin kök dizini altına kurulmuştur. 

**Binutils derlendikten sonra gcc derlemek gerekmektedir ama bu işlem sırasında kullanılan eski gcc/glibc ve derlenilecek olan yeni gcc/glibc arasında sürüm farkı bulunmaktadır. Oysa temel programlar arasında paralelliğin sağlanması gerekmektedir. Ortaya çıkacak sürüm farkı kaynaklı, iki program arası bağımlılıkların sorun oluşturacağı görülmüştür. Bu soruna çözüm olarak önce bir ara adım olarak glibc derlenmiştir.** 

GNU Library C
--------------
Yeni sistem için derlenecek glibc için kernel-headers (glibc ve diğer kullanıcı uzayı uygulamaları tarafından kullanılan başlık dosyaları) bağımlılığı söz konusudur. Bu yüzden öncelikle 
::

    pisi fetch kernel-headers

komutuyla alınan pisi paketi newroot/sysroot içerisine 
::

    unpisi kernel-headers-xxx.pisi

komutuyla açılır.
Daha sonra glibc derlemek için yapılacak adımlara geçilebilir. Yeni sistem için kullanılacak glibc'nin kaynak kodu sources dizini içerisine indirilir ve newroot altındaki src dizini içine açılır. 
::

    cd ${PREFIX}/src
    tar xvf glibc-xxx
    mkdir -p build/glibc-stage1
    cd build/glibc-stage1

kaynak kodlar src içerisine açılıp derleme için kullanılacak build altında glibc-stage1 dizini oluşturulmuştur.
::

    ../../glibc-xxx/configure --prefix=usr  --target=${TARGET} --without-__thread --enable-add-ons=linuxthreads --with-headers=${SYSROOT}/usr/include
    make
    make install_root=${SYSROOT} install

yukarıdaki komutlarla glibc yapılandırılıp kurulur.

*Burada dikkat edilecek bir nokta olarak, bu işlemde var olan mimari ile hedef mimari aynı olduğu için sadece yukarıdaki parametreler yeterli olmuştur. Var olan mimariden başka bir mimari hedeflenseydi yapılandırma komutu aşağıdaki gibi olacaktı.* 
::

    BUILD_CC=gcc CC=${CROSS_COMPILE}gcc AR=${CROSS_COMPILE}ar RANLIB=${CROSS_COMPILE}ranlib AS=${CROSS_COMPILE}as LD=${CROSS_COMPILE}ld ../../glibc-xxx/configure --prefix=usr  --target=${TARGET} --without-__thread --enable-add-ons=linuxthreads --with-headers=${SYSROOT}/usr/include


GCC
------
Yeni sistem için kullanılacak gcc'nin kaynak kodu sources dizini içerisine indirilir ve newroot altındaki src dizini içine açılır. (gcc-4.5 sürümü için derleme öncesi libmpc paketi kurulması gerekmektedir.)
::

    cd ${PREFIX}/src
    tar xvf gcc-xxx
    mkdir -p build/gcc-stage1
    cd build/gcc-stage1

kaynak kodlar src içerisine açılıp derleme için kullanılacak build altında gcc-stage1 dizini oluşturulmuştur.
::

    ../../gcc-xxx/configure --prefix=${PREFIX} --target=${TARGET} --enable-languages=c  --with-build-sysroot=/ --with-sysroot=${SYSROOT} --with-headers=${SYSROOT}
    make
    make install

yukarıdaki komutlarla gcc yapılandırılıp kurulur.  

Binutils, glibc ve gcc'nin derlenmesiyle temel derleme sistemi oluşturma işleminin büyük çoğunluğu tamamlanmış oldu. 

zlib, ncurses ve bash'in Derlenmesi
-------------------------------------
Son adım, glibc, gcc temel yazılımların derlenmesiyle oluşturulan yeni sistemi başlatabilmek ve bu sistem üzerinde temel işlemleri gerçekleyebilmek için gereken zlib, ncurses ve bash araçlarının kurulmasından meydana gelmektedir. Bu adım için .bashrc dosyasına ekleme yapılabilir.
::

    alias autotools.configure="./configure --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info"
    alias autotools.install="make prefix=$MYDESTDIR/usr infodir=$MYDESTDIR/usr/share/info mandir=$MYDESTDIR/usr/share/man install"

ilerleyen işlemlerde yapılandırma ve kurma işlemleri için varsayılan parametreleri içeren tanımlamalar yapılmış oldu.

**zlib**
  Birçok uygulamanın kullandığı kayıpsız veri sıkıştırma algoritması içeren kitaplıktır.

Pardus paket depolarında bulunan zlib paketi
::

    pisi build --unpack http://svn.pardus.org.tr/pardus/2009/devel/system/base/zlib/pspec.xml

komutuyla inidirilir ve /var/pisi/zlib-xxx/work/ altındaki zlib* dizini newroot/src/ altına kopyalanır. Daha sonra bu dizin içerisine geçilir ve zlib paketinin actions.py dosyası içerisindeki işlemler adım adım yapılır.
::

    mkdir m4
    autoreconf -fi
    autotools.configure --disable-static
    make
    autotools.install

bu işlemlerden sonra pisitools kullanılarak devam etmek gerekiyor fakat yeni sistem pisitools içermediği için devam eden adımları newroot/installdir altında gerçeklemek gerekiyor. newroot/installdir içine gidilir. (xxx versiyon numarasını temsil etmektedir.)
::

    mv usr/lib/libz* lib
    ln -s lib/libz.so.xxx  usr/lib/libz.so.xxx
    ln -s libz.so.xxx  usr/lib/libz.so.1
    ln -s libz.so.1  usr/lib/libz.so
    cp zconf.h  usr/include
    cp zlib.h  usr/include
    cp zutil.h  usr/include

bu komutlardan sonra oluşan ".la" uzantılı dosyalar silinir ve yukarıdaki komutlar sonucunda oluşan installdir dizini içerisinde oluşan tüm içeriği newroot/sysroot'a kopyalayınca zlib yeni sisteme kurulmuş olur.

**ncurses**
  Konsol tabanlı uygulamalar için grafik arayüz sağlayan kitaplıktır.

Pardus paket depolarında bulunan ncurses paketi
::

    pisi build --unpack http://svn.pardus.org.tr/pardus/2009/devel/system/base/ncurses/pspec.xml

komutuyla indirilir ve /var/pisi/ncurses-xxx/work/ altındaki ncurses* dizini newroot/src/ altına kopyalanır. Daha sonra bu dizin içerisine geçilir ve ncurses paketinin actions.py dosyası içerisindeki işlemler adım adım yapılır.
::

    autotools.configure --without-debug --without-profile --disable-rpath --enable-const \
                        --enable-largefile --enable-widec --with-terminfo-dirs='/etc/terminfo:/usr/share/terminfo'\
                        --disable-termcap --with-shared --with-rcs-ids --with-chtype='long'\
                        --with-mmask-t='long'  --without-ada --enable-symlinks  

    make
    make DESTDIR=$MYDESTDIR install

devam eden adımlar için newroot/installdir içine gidilir.
::

    rm -rf usr/lib/*.a
    ln -s usr/lib/*w.* usr/lib/*.*

son komutta /*w.*/ dosyaları w olmayan hallerine sembolik linklenir. Oluşan ".la" uzantılı dosyalar silinir ve daha sonra paket deposunda bulunan ncurses paketi başka bir dizinde unpisi komutuyla açılır ve çıkan etc/ dizini newroot/sysroot içine kopyalanır. Böylece ncurses da kurulmuş olur.

**bash**
  Komut satırı kabuğu ve bu kabuğun betik dilidir.

Pardus paket depolarında bulunan bash paketi
::

    pisi build --unpack http://svn.pardus.org.tr/pardus/2009/devel/system/base/bash/pspec.xml

komutuyla indirilir ve /var/pisi/bash-xxx/work/ altındaki bash* dizini newroot/src/ altına kopyalanır. Daha sonra bu dizin içerisine geçilir ve bash paketinin actions.py dosyası içerisindeki işlemler adım adım yapılır.
::

    autoconf
    autotools.configure --without-installed-readline --disable-profiling --without-gnu-malloc --with-curses
    make
    autotools.install

devam eden adımlar için newroot/installdir içine gidilir.
::

    mv usr/bin/bash  bin/
    ln -s bin/bash  bin/sh
    ln -s bin/bash  bin/rbash

yukarıdaki komutlar sonunda bash de kurulmuş olur.


Böylece derlenen yeni sisteme temel araçlar da kurulduktan sonra temel derleme sistemi tamamen oluşturulmuş olur.



Kaynaklar
----------
- Linux man sayfaları
- `Building a GNU/Linux ARM Toolchain <http://frank.harvard.edu/~coldwell/toolchain/>`_
- `NASIL:Bayraklar donanmış cafcaflı <http://tr.pardus-wiki.org/NASIL:Bayraklar_donanm%C4%B1%C5%9F_cafcafl%C4%B1>`_























