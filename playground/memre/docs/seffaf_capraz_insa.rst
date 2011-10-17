======================
TRANSPARENT CROSSBUILD
======================

Giriş
-----
Native ortamda derleme yapar gibi derleme yapmamıza olanak tanıyan şeffaf
çapraz inşa yöntemi, hedef platform için derlenmiş ikilileri bir emulator
veya ortamın direkt içerisinde çalıştırılması şeklinde gerçekleştirilir.

Derlenecek uygulama için öncelikle çapraz derleyiciler ve araçlar belirlenir.
Hedef platform için oluşturulmuş ikililerin nasıl çalıştırılacağına dair
kurallar ayarlandıktan sonra doğal derleme yapılıyormuş gibi inşa işlemi
başlatılır.

Doğal derlemede bir inşa sistemi kullandığımızda, inşa sistemi sistemde
bulunan kitaplıklar, başlık dosyaları, herhangi bir kitaplıkta bulunan
bir fonksiyonun davranışı vs. gibi testleri rahat bir şekilde yapar.
Ancak çapraz derleme esnasında bazı testlerin yapılması imkansızlaşır.
Bu durumda o testlerin sonuçları inşa sistemine bir şekilde bildirilip
testlerin atlanması sağlanarak inşa testleri başarılı sonuçlanmış olur.
Ancak bu geliştirme modelinde her bir uygulama için oldukça çok işgücü
harcamak zorunda kalınmaktadır.

Şeffaf derlemede, hedef platformda çalışacak uygulamalar veya test için
hazırlanmış ufak kod parçaları inşa esnasında kullanılacaksa bu uygulamalar
direkt bir emulator yardımıyla çalıştırılır. Böylelikle doğal derleme
yapar gibi çapraz derleme yapılabilir duruma geliriz.

Şimdi ``şeffaf çapraz inşa`` (transparent crossbuild) ayrıntılarına
geçebiliriz.

binfmt_misc modülü
------------------
``binfmt_misc``, belirli ikili çalıştırılabilir dosyaları veya bir betiği
bir uygulama ile çalıştırmaya olanak tanıyan bir kernel modülüdür.
İkili dosyaları ``magicnumber`` larına, betikleri ``hashbang`` lerine göre
değerlendirip ilgili uygulama yardımıyla, sanki herhangi bir programı
çalıştırır gibi çalıştırmaya yarar.

``binfmt_misc`` modülünün desteği öncelikle kernelde açılmış olmalıdır.
Bu destek açıldıktan sonra ``proc`` dosya sistemi altında registration
işlemlerini yapabilirsiniz::

    $ sudo modprobe binfmt_misc
    $ cd /proc/sys/fs/binfmt_misc
    $ ls
    register  status
    $ cat satus
    enabled

``binfmt_misc`` modülü şu anda kullanıma hazır. Registration için gerekli
dokümantasyonu `binfmt_misc HOWTO belgesinden 
<http://www.kernel.org/doc/Documentation/binfmt_misc.txt>`_ öğrenebilirsiniz.
Bu belgenin ayrıntılarına girmeden bizim ile ilgili kısmı anlatacağım.

binfmt_misc modülü kullanımı
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
binfmt_misc modülünü kullanırken ``:`` ile birbirlerinden ayrılmış değeri
echo ile register dosyasına basmak yeterli olacaktır::

    arm-register içeriği:
    8<------8<------8<------8<------8<------8<------8<------8<------8<------

    #!/bin/bash
    DEFAULT_PARM_ROOTFS=/var/cross/sysroots/armv7l
    PARM_ROOTFS=${DEFAULT_PARM_ROOTFS}
    REGISTER_NODE=arm
    EMULATOR="/qemu-arm-debug"
    ARM_ELF_MAGIC="\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x28\x00"
    MASK="\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfb\xff\xff\xff"

    # Register magic of the ARM ELF binaries to the binfmt_misc
    #
    # binfmt_misc format:
    #   :<name>:<type>:<offset>:<magic>:<mask>:<interpretter>:<flags>
    #
    #                 -> Name of the registration.
    #                /
    #               /                -> Say binfmt_misc that "we are
    #              /                /     using **magic file** of this registration".
    #             /                /
    #            /                / -> No offset
    #           /                / /-> Magic number of the ARM binaries
    #          /                / //
    #         /                / //                -> Mask
    #        /                / //                /
    #       /                / //                /       -> Emulator of the binaries
    #      /                / //                /       /
    #      ----------------:-::----------------:-------:-----------
    echo ":${REGISTER_NODE}:M::${ARM_ELF_MAGIC}:${MASK}:${EMULATOR}:" > /proc/sys/fs/binfmt_misc/register

    8<------8<------8<------8<------8<------8<------8<------8<------8<------

Bu ufak betiği kullanarak binfmt_misc modülünü ayarlayacağız. Ancak öncelikle
ARM için dinamik yükleyicinin kullanımı ile ilgili bir trick yapmamız gerekiyor.
Bildiğiniz gibi çalıştırılabilir uygulamalarda paylaşımlı kitaplıklar kullanıldığında
dinamik yükleyici bu paylaşımlı kitaplıkları belleğe yükler ve uygulama bu
şekilde çalıştırılır. qemu-arm'ın linux-user modunda bu dinamik yükleyiciyi
doğal bir şekilde çalıştırabilmesi için bir trick kullanacağız. Önceklikle
dinamik yükleyici için trick yapmadan nasıl çalışmadığını görelim

Pardus-ARM için hazırladığımız çapraz derleyicinin ``sysroot`` dizini içerisinde
dinamik yükleyici bulunmakta. Ayrıca bu ``sysroot`` içerisinde ``libc``, ``libgcc``
ve diğer temel kitaplıkların tamamı bulunmakta. Yapmamız gereken yalnızca
``<sysroot>/lib/ld-linux.so.3`` sembolik linkini oluşturmak. İşlerimizi
kolaylaştırması açısından sysroot dizinini /parm'a kopyalıyoruz::

    $ cp /opt/toolchain/armel/arm-pardus-linux-gnueabi/sysroot /parm -rf
    $ ln -s `readlink -f /parm/lib/ld-linux.so.3` /lib/ld-linux.so.3
    $ ls -l /lib/ld-linux.so.3
    lrwxrwxrwx 1 root root 67 Eyl  9 13:04 /lib/ld-linux.so.3 -> /parm/lib/ld-2.9.so
    $

binfmt_misc modülü ile ikilileri direkt çalıştırabilmek için binfmt_misc
modülüne registration yapıyoruz. Bu registration esnasında bir sarmalayıcı betik
kullanarak sysroot dizini içerisindeki kitaplıkların LD_LIBRARY_PATH değişkeni
içerisinde gösterilmesini sağlıyoruz::

    #!/bin/bash

    SYSROOT=/parm
    DYN_LOADER=/lib/ld-linux.so.3

    exec /qemu-arm-static -E LD_LIBRARY_PATH=${SYSROOT}/lib:${SYSROOT}/usr/lib "$@"

    # Should never reach here!
    echo "Unable to execute qemu-arm!"
    exit 1

Registration işlemini yapabiliriz artık::

    $ ls /proc/sys/fs/binfmt_misc/status
    register  status
    $ cat /proc/sys/fs/binfmt_misc/status
    enabled
    $ ./arm-register
    $ ls
    arm  register  status
    $ cat arm
    enabled
    interpreter /qemu-arm-debug
    flags:
    offset 0
    magic 7f454c4601010100000000000000000002002800
    mask ffffffffffffff00fffffffffffffffffbffffff
    $

ARM için derlenmiş bash kabuğunu çalıştırarak qemu ile bir test yapalım::

    $ file ./bin/bash
    ./bin/bash: ELF 32-bit LSB executable, ARM, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.35, stripped
    $ /qemu-arm-debug ./bin/bash
    memre-c2-x86_64 armel # echo $$
    13771
    memre-c2-x86_64 armel # ps aux | grep $$
    root     13771 10.2  0.1 134568  7912 pts/3    S    13:11   0:01 /qemu-arm-static -E LD_LIBRARY_PATH=/parm/lib:/parm/usr/lib bin/bash
    root     13790  0.0  0.0   6652   800 pts/3    S+   13:11   0:00 grep --color 13771
    memre-c2-x86_64 armel # exit
    exit
    $ ./bin/bash
    memre-c2-x86_64 armel # echo $$
    13834
    memre-c2-x86_64 armel # ps aux | grep $$
    root     13834  0.7  0.1 134568  7920 pts/3    S    13:18   0:01 /qemu-arm-static -E LD_LIBRARY_PATH=/parm/lib:/parm/usr/lib ./bin/bash
    root     13854  0.0  0.0   6652   804 pts/3    S+   13:22   0:00 grep --color 13834
    memre-c2-x86_64 armel #

Scratchbox
----------
scratchbox, binfmt_misc modülünün yanında sarmaladığı sistem çağrıları ile
tam bir emulated ortam sağlamayı amaçlar ve sanki bir hedef donanımın
içerisinde çalışıyormuş gibi derleme, test gibi işlemleri kolayca yapmamıza
olanak tanır.

scratchbox kullanmak için öncelikle bir ilklendirme (initialization) işlemi
yapılması gerekiyor. Bu initialization işleminde ``libtool``'un çapraz inşa
için derlenmesi ve toolchain içerisinde bulunan paylaşımlı kitaplıklar ile
birlikte scratchbox'un bir sysroot oluşturması sağlanır.

scratchbox derlemelerde hedef ikilileri emüle edecek uygulamanın belirlenmesi
istemektedir. Emüle edilecek uygulama qemu olabileceği gibi başka bir
uygulama veya sbrsh (scratchbox shell) de olabilir. Sbrsh, hedef donanım
içerisinde bir servis olarak çalışır ve scratchbox'un gönderdiği ikilileri
çalıştırarak çıktıları geri döndürür.

Corporate2 ARM sürümünde qemu linux-user modu ile emülasyon yapıldı, ancak
qemu linux-user modu her zaman başarılı sonuçlar vermiyor (bkz. perl).
linux-user modunda çalıştırılacak ikili qemu tarafından direkt çalıştırılır
ve bütün mikroişlemci instructionları java vm'in bytekodları çalıştırdığı
gibi çalışır. sbrsh'de ise qemu system-mod veya hedef donanım kullanılır.
qemu ile ufak bir linux imajı oluşturulur ve bu imaj içerisinde sbrshd
servisi gerçek sistem gibi çalışabilmektedir.

Konunun daha iyi anlaşılabilmesi açısından uygulamalara geçelim.

qemu linux-user modu ile derleme
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
İlklendirme işlemini ``qemu-arm`` ile yapıyoruz. Öncelikle ufak bir sysroot'a
ihtiyacımız var. Bunun için toolchain içerisinden çıkan sysroot'u kullanacağız.
Daha önceden hazırlamış olduğumuz toolchain'i ``/opt/toolchain/`` dizinine açtık.
Hedef platform için daha generic bir toolchain hazırlayabilirdik, ancak armv7-a
temelli cortex-a8 core'a sahip bir beagleboard'u kullanacağımızdan armv7l (sondaki
l little-endian bir sistem ile çalıştığımızı vurguluyor) için optimize edilmiş bir
toolchain hazırladık. Daha önceki örneklerde kullandığımız ``armel`` dizini
``armv7l`` ile değiştirilmiş olması bu nedenledir::

    $ cd /opt/toolchain/armv7l/arm-pardus-linux-gnueabi/sysroot
    $ sb2-init -c qemu-arm PardusCorporate arm-pardus-linux-gnueabi-gcc
    Info: Mapping mode not specified, using default (simple)
    Using arm-pardus-linux-gnueabi-gcc to detect target architecture:
    Finished writing sb2.gcc.config
    gcc configured.
    sb2-init: Target architecture is 'arm'
    sb2-init: Host architecture is 'x86_64'
    Finished writing sb2.config
    sb2-init: Creating Debian build system settings for this target:
    -h: error while loading shared libraries: -h: cannot open shared object file
    /bin/bash: error while loading shared libraries: /bin/bash: wrong ELF class: ELFCLASS64
    sb2-init: configuring libtool for this target:
    ## -------------------------- ##
    ## Configuring libtool 2.2.6b ##
    ## -------------------------- ##

    checking for a BSD-compatible install... /usr/bin/install -c
    checking whether build environment is sane... yes
    checking for a thread-safe mkdir -p... /bin/mkdir -p
    checking for gawk... gawk
    checking whether make sets $(MAKE)... yes
    checking whether subdir libobjs are useable... yes
    checking for gcc... gcc
    checking for C compiler default output file name... a.out
    checking whether the C compiler works... yes
    checking whether we are cross compiling... no

    ...

    sb2-init completed successfully, have fun!
    $ uname -a
    Linux memre-c2-x86_64 2.6.35.13 #1 SMP Wed Jun 22 10:15:17 EEST 2011 x86_64 x86_64 x86_64 GNU/Linux
    $ sb2 uname -a
    Linux memre-c2-x86_64 2.6.35.13 #1 SMP Wed Jun 22 10:15:17 EEST 2011 arm arm arm GNU/Linux
    $ 

autotools yaptığı testlerde ``checking whether we are cross compiling... no``
çıktısı verdi. Normalde çapraz inşada bu kısımda ``no`` sonucu dönmemesi
gerekiyordu. scratchbox2 sarmaladığı sistem çağrılarıyla ve derlenen ikilileri
sanki üzerinde çalıştığı platformun ikilileriymiş gibi çalıştırdığından
doğal derleme yapar gibi yapıyoruz derlemeleri.

Bu ilklendirme işleminde yarı-emüle bir yöntemle inşaları yaptırıyoruz. Yani
çağrılan uygulamalar eğer PC'de varsa onlar çalıştırılıyor, eğer yok da hedef
mimari için derlendiyse onlar emüle ediliyor. Bu şekilde inşalar geleneksel
çapraz inşa kadar olmasa da full-emulated bir ortam kadar yavaş olmuyor.

Şimdi scratchbox kullanarak bir inşa gerçekleştirelim::

    $ wget http://download.savannah.gnu.org/releases-noredirect/attr/attr-2.4.44.src.tar.gz
    $ tar xfz attr-2.4.44.src.tar.gz
    $ cd attr-2.4.44
    $ sb2 ./configure --libdir=/lib \
        --mandir=/usr/share/man \
        --libexecdir=/lib \
        --bindir=/bin
    checking build system type... arm-unknown-linux-gnueabi
    checking host system type... arm-unknown-linux-gnueabi
    checking for gcc... gcc
    checking for C compiler default output file name... a.out
    checking whether the C compiler works... yes
    checking whether we are cross compiling... no
    checking for suffix of executables...
    checking for suffix of object files... o
    checking whether we are using the GNU C compiler... yes
    checking whether gcc accepts -g... yes
    checking for gcc option to accept ISO C89... none needed
    checking for a sed that does not truncate output... /bin/sed
    checking for grep that handles long lines and -e... /bin/grep
    checking for egrep... /bin/grep -E
    checking for fgrep... /bin/grep -F
    checking for ld used by gcc... /opt/toolchain/armv7l/arm-pardus-linux-gnueabi/bin/ld
    checking if the linker (/opt/toolchain/armv7l/arm-pardus-linux-gnueabi/bin/ld) is GNU ld... yes
    checking for BSD- or MS-compatible name lister (nm)... /usr/bin/nm -B
    checking the name lister (/usr/bin/nm -B) interface... BSD nm
    checking whether ln -s works... yes

    ...

    libtool: compile:  gcc -g -O2 -DDEBUG -funsigned-char -fno-strict-aliasing -Wall -DVERSION=\"2.4.44\" -DLOCALEDIR=\"/usr/share/locale\" -DPACKAGE=\"attr\" -I../include -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -include libattr.h -c attr_copy_check.c -o attr_copy_check.o >/dev/null 2>&1
    /bin/sh ../libtool --mode=compile gcc -g -O2 -DDEBUG -funsigned-char -fno-strict-aliasing -Wall -DVERSION=\"2.4.44\" -DLOCALEDIR=\"/usr/share/locale\" -DPACKAGE=\"attr\" -I../include -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -include libattr.h  -c attr_copy_action.c
    libtool: compile:  gcc -g -O2 -DDEBUG -funsigned-char -fno-strict-aliasing -Wall -DVERSION=\"2.4.44\" -DLOCALEDIR=\"/usr/share/locale\" -DPACKAGE=\"attr\" -I../include -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -include libattr.h -c attr_copy_action.c  -fPIC -DPIC -o .libs/attr_copy_action.o
    libtool: compile:  gcc -g -O2 -DDEBUG -funsigned-char -fno-strict-aliasing -Wall -DVERSION=\"2.4.44\" -DLOCALEDIR=\"/usr/share/locale\" -DPACKAGE=\"attr\" -I../include -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -include libattr.h -c attr_copy_action.c -o attr_copy_action.o >/dev/null 2>&1
    /bin/sh ../libtool --mode=compile gcc -g -O2 -DDEBUG -funsigned-char -fno-strict-aliasing -Wall -DVERSION=\"2.4.44\" -DLOCALEDIR=\"/usr/share/locale\" -DPACKAGE=\"attr\" -I../include -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -include libattr.h  -c syscalls.c

    ...

    $ file libattr/.libs/libattr.so.1.1.0
    libattr/.libs/libattr.so.1.1.0: ELF 32-bit LSB shared object, ARM, version 1 (SYSV), dynamically linked, not stripped
    $

scratchbox ile derleme yapmak bu kadar basit.

Tabii ki pisi içerisinde bu parametreler vs. hazırlandığı için siz bu gereksiz
ayrıntılarla uğraşmak zorunda kalmayacaksınız. Yapmanız gereken tek şey
``pisi bi pspec.xml`` kadar kolay.

PARM için sysroot hazırlama
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Dağıtımda kullanılan kitaplık ve başlık bağımlılıklarını sistemde bir sysroot
dizinine atmak ve derleyiciye gerekli parametreleri vermek gerekmekte. Bu
bağımlılıkları aslında toolchain içerisinde bulunan sysroot dizinine de
atabiliriz, ancak sistemde gerekli olan kitaplık sayısını göz önüne alacak
olursak toolchain'in aşırı şişmesi gibi bir sorun ile karşı karşıya kalacağımızdan
ayrı bir sysroot hazırlama yoluna gitmemiz gerekiyor.

Sysroot içerisini toolchain içerisinden çıkan sysroot dizininin içeriği ile
veya daha önceden oluşturmuş olduğumuz pardus arm'ın system.base bileşeni ile
doldurabiliriz.

Ardından oluşacak bütün paketler bu sysroot dizinine eklenecek ve pisi ile inşa
ettiğimiz paketler bu dizinin içerisine kurulacak.

Sysroot'un system.base bileşeni hazırlama kısmı aslında biraz zorlu bir süreç.
Örneğin derlemeye ilk başta toolchain ve bileşenleri ile başlamak gerekiyor.
Cross-toolchain içerisinde bir glibc, gcc gelse bile bunların paketlenip arm
depolarına girmesi zorunlu. Paket yönetim sistemi kullanan (ki günümüzde kullanmayan
yoktur) her dağıtım bütün bileşenlerini paketler halinde sunar, eğer çalışması
gereken betikler varsa da bu betikler ``postinstall``, ``preinstall``, ``postremove``,
``preremove`` vs. gibi işlemler esnasında çalıştırılır. Yani bir dosyayı bir
konumdan direkt sysroot içerisine kopyalama gibi bir durum söz konusu olmamalıdır.

Bootstrap aşamasında öncelikle glibc, gcc, binutils ve bu bileşenlerin bağımlılıkları
tamamen cross-toolchain tarafından derlenip, cross-toolchain'in sysroot'undaki
libc libgcc vs. kitaplıklarına bağlanır ve oluşturulacak sysroot dizini içerisine
kurulur. Sonrasında tekrardan bu paketler (ve tabii ki bağımlılıkları) tekrardan
inşa edilerek yeni oluşturulmuş olan sysroot içerisindeki kitaplıklara bağlanır.
Bu ikinci aşama sonrasında system.base ve system.devel içerisindeki diğer paketler
derlenebilir.

Bütün system.base ve system.devel bileşenleri inşa edildikten sonra kalan diğer
paketlerin inşaları herhangi bir sıra ile olabilir, hangi bileşenler acil
yetiştirilmesi gerekiyorsa o bileşenler önce inşa edilebilir. Ancak tavsiye edilen
kernel sürücülerine öncelik verilmesidir. Pardus depolarında bir paket ile gelen
bütün özelliklerin sakıncalı bir durum olmaması halinde  açılması gibi bir gelenek
vardır. Bu durum kimi zaman çembersel bağımlılık sorununu beraberinde getirmektedir.
Örneğin bir ``a`` paketi inşa esnasında bir desteğin kullanımı için ``b`` paketine
ihtiyaç duymakta, ``b`` paketi de aynı şekilde bir desteğinin açık olması için ``a``
paketine ihtiyaç duymakta. Bu durumda öncelikle ``a`` paketi ``b`` paketinin var
olması ile gelecek desteği kapalı olarak ilk önce derlenir. ``a`` paketi derlendiği
için, ``b`` paketinin inşa gereksinimi sağlanır ve ``b`` paketi derlenir. Sonrasında
``a`` paketinin ``b`` paketi ile beraber gelen desteği açılarak ``a`` paketi tekrardan
derlenir. Bütün Linux dağıtımlarında bu tarz workaroundlar yapılmak zorunda
kalınmaktadır. Bu durum ``X11`` ailesi, ``alsa`` sürücüleri vb. kısımlarda
çokça karşılaşılan bir durumdur. Eğer ARM temelli cihazınızda grafik arayüzü,
ses çıktısı vs. isterseniz bu gibi durumlarla karşılaşabilirsiniz (tabii ikili
depoyu kullanmazsanız).

Openembedded grubu bu durumu çözmek için ``staging`` paketleri yapmaktadır. Staging
paketlerinde yukarıda belirttiğimiz sorunun çözümü için, ``a`` paketinin ``b``
paketi ile beraber desteğinin kapalı olduğu ara bir paket oluşturulması, ``b``
paketinin inşası ile birlikte ``a`` paketinin derlenmesi ve ``a`` paketinin
staging paketinin yeni oluşturulmuş olan paket tarafından override edilmesi
şeklinde çalışır. Openembedded grubu tamamen kaynak kod üzerinden derleme yapma
gibi bir mantık ile çalıştıklarından böyle bir çözüm sunmak zorunda kalmaktadır.
Pardus tarafında geliştiriciler bu kısımları çeşitli hackler ile halleder.

Böyle böyle paketleri yapıyosun işte..

