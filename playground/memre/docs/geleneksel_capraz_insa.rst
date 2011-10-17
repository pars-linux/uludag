====================================
GELENEKSEL ÇAPRAZ DERLEME YÖNTEMLERİ
====================================

Hazırlıklar
-----------
Öncelikle bir çapraz derleyicimizi de içerisinde bulunduran çapraz inşa
ortamına (cross toolchain) ihtiyacımız var. Çapraz derleme oluşturma
aşamalarını *``toolchain_olusturma.rst``* belgesinden okuyabilirsiniz.

Çapraz derleyimizi indirip ortamımızı oluşturuyoruz::

    $ cd /tmp
    $ wget http://cekirdek.pardus.org.tr/~memre/archives/toolchain-armel.tar.xz
    $ sudo mkdir -p /opt/toolchain
    $ sudo tar xfvJ toolchain-armel.tar.xz -C /opt/toolchain/

Toolchain'in içerisindeki 8086 sistemimiz için derlenmiş ikililerin bulunduğu
``bin`` dizinini ``PATH`` değişkenimize ekliyoruz::

    $ export PATH=/opt/toolchain/armel/bin:$PATH

Ufak bir derleme denemesi yapalım::

    $ cat > main.c << __EOF
    #include <stdio.h>

    int main (int argc, char **argv, char **envp)
    {
        fprintf (stderr, "It works ;)\n");

        return 0;
    }

    __EOF
    $ arm-pardus-linux-gnueabi-gcc -o tryout main.c
    $ file tryout
    tryout: ELF 32-bit LSB executable, ARM, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.35, not stripped
    $

Gördüğünüz gibi derleme işlemi başarılı. Şimdi derlediğimiz kodun düzgün
çalışıp çalışmadığını test edelim.

Testleri direkt board üzerinde yapabildiğimiz gibi qemu ile de yapabiliyoruz.
board üzerinde debug işlemleri daha sonra ele alınacak bir konu olduğundan
testleri ``qemu`` ile gerçekleyeceğiz. ``qemu`` kurulu değilse kurulmasını
sağlayalım::

    $ [ `which qemu-arm` ] || pisi it qemu -y

qemu sistemimize yüklendiğine göre teste başlayabiliriz. qemu ile ilgili
daha ayrıntılı bir belgeyi *``qemu.rst``* den okuyabilirsiniz. qemu
``Linux-user`` modunda ``LD_LIBRARY_PATH`` değişkeni ve dynamic loader
gösterilmeli, aksi taktirde derlediğiniz uygulamayı çalıştıramazsınız.
Bu sebepten ötürü bu işlemleri yapacak ufak bir betik yazıp bütün testler
boyunca bu betiği kullanacağız::

    $ cat > /usr/bin/qemu-arm-debug << __EOF
    #!/bin/bash

    TOOLCHAIN=/opt/toolchain/armel
    SYSROOT=\${TOOLCHAIN}/arm-pardus-linux-gnueabi/sysroot
    DYN_LOADER=\${SYSROOT}/lib/ld-linux.so.3

    exec qemu-arm -E LD_LIBRARY_PATH=\${SYSROOT}/lib:\${SYSROOT}/usr/lib \${DYN_LOADER} "\$@"

    # Should never reach here!
    echo "Unable to execute qemu-arm!"
    exit 1

    __EOF
    $ chmod a+x /usr/bin/qemu-arm-debug
    $ qemu-arm-debug ./tryout
    It works ;)
    $

Uygulamamız çalışıyor. En basit haliyle ufak bir uygulamayı derleyip
çalıştırmak bu kadar basit.

Sıra dağıtımda kullanılan yazılımları inşa etmeye gelince işler bu kadar
basit olmayabiliyor. Şimdi tek tek ele alalım bu işlemleri.

Makefileları çapraz derleme için değiştirmek
--------------------------------------------

Kimi uygulamaların Makefile'ları bir inşa sistemi tarafından ``generate``
edilir ve çok karmaşık olurlar. Kimi projelerde ise geliştiriciler inşa
sistemi kullanmazlar ve Makefile'ları elle yazıldıklarından bu
Makefile'lar rahat bir şekilde değiştirilebilir durumda olurlar.

Örneğin Makefile'ları elle yazılmış olan zip uygulamasını ``CC`` ve ``CXX``
değişkenlerini belirleyerek inşa edelim::

    $ wget http://heanet.dl.sourceforge.net/infozip/Zip%203.x%20%28latest%29/3.0/zip30.tar.gz
    $ tar xfvz zip30.tar.gz
    $ cd zip30

    $ make -f unix/Makefile \
           CC=arm-pardus-linux-gnueabi-gcc \
           CXX=arm-pardus-linux-gnueabi-g++ \
           generic

    sh unix/configure "arm-pardus-linux-gnueabi-gcc" "-I. -DUNIX " ""
    Check C compiler type (optimization options)
      GNU C (-O3)
    Check bzip2 support
      Check for bzip2 in bzip2 directory
      Check if OS already has bzip2 library installed
    -- Either bzlib.h or libbz2.a not found - no bzip2
    Check for the C preprocessor
    Check if we can use asm code
    Check for ANSI options
    Check for prototypes

    ...

    make[1]:`/tmp/zip30' dizinine giriliyor
    arm-pardus-linux-gnueabi-gcc -c -I. -DUNIX -O3 -DUIDGID_NOT_16BIT -DUNICODE_SUPPORT -DHAVE_DIRENT_H -DHAVE_TERMIOS_H zip.c
    arm-pardus-linux-gnueabi-gcc -c -I. -DUNIX -O3 -DUIDGID_NOT_16BIT -DUNICODE_SUPPORT -DHAVE_DIRENT_H -DHAVE_TERMIOS_H zipfile.c
    arm-pardus-linux-gnueabi-gcc -c -I. -DUNIX -O3 -DUIDGID_NOT_16BIT -DUNICODE_SUPPORT -DHAVE_DIRENT_H -DHAVE_TERMIOS_H zipup.c
    arm-pardus-linux-gnueabi-gcc -c -I. -DUNIX -O3 -DUIDGID_NOT_16BIT -DUNICODE_SUPPORT -DHAVE_DIRENT_H -DHAVE_TERMIOS_H fileio.c
    arm-pardus-linux-gnueabi-gcc -c -I. -DUNIX -O3 -DUIDGID_NOT_16BIT -DUNICODE_SUPPORT -DHAVE_DIRENT_H -DHAVE_TERMIOS_H util.c

    ...

    arm-pardus-linux-gnueabi-gcc -o zipcloak  zipcloak.o zipfile_.o fileio_.o util_.o globals.o unix_.o crc32_.o   crypt_.o ttyio.o
    arm-pardus-linux-gnueabi-gcc -c -I. -DUNIX -O3 -DUIDGID_NOT_16BIT -DUNICODE_SUPPORT -DHAVE_DIRENT_H -DHAVE_TERMIOS_H zipnote.c
    arm-pardus-linux-gnueabi-gcc -o zipnote  zipnote.o  zipfile_.o fileio_.o util_.o globals.o unix_.o crc32_.o
    arm-pardus-linux-gnueabi-gcc -c -I. -DUNIX -O3 -DUIDGID_NOT_16BIT -DUNICODE_SUPPORT -DHAVE_DIRENT_H -DHAVE_TERMIOS_H zipsplit.c
    arm-pardus-linux-gnueabi-gcc -o zipsplit  zipsplit.o zipfile_.o fileio_.o util_.o globals.o unix_.o crc32_.o
    make[1]: `/tmp/zip30' dizininden çıkılıyor

Derleme işlemi sorunsuz tamamlandı, şimdi test edelim::

    $ file zip
    zip: ELF 32-bit LSB executable, ARM, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.35, not stripped

    $ qemu-arm-debug ./zip
    Copyright (c) 1990-2008 Info-ZIP - Type 'zip "-L"' for software license.
    Zip 3.0 (July 5th 2008). Usage:
    zip [-options] [-b path] [-t mmddyyyy] [-n suffixes] [zipfile list] [-xi list]
      The default action is to add or replace zipfile entries from list, which
      can include the special name - to compress standard input.
      If zipfile and list are omitted, zip compresses stdin to stdout.
      -f   freshen: only changed files  -u   update: only changed or new files
      -d   delete entries in zipfile    -m   move into zipfile (delete OS files)
      -r   recurse into directories     -j   junk (don't record) directory names
      -0   store only                   -l   convert LF to CR LF (-ll CR LF to LF)
      -1   compress faster              -9   compress better
      -q   quiet operation              -v   verbose operation/print version info
      -c   add one-line comments        -z   add zipfile comment
      -@   read names from stdin        -o   make zipfile as old as latest entry
      -x   exclude the following names  -i   include only the following names
      -F   fix zipfile (-FF try harder) -D   do not add directory entries
      -A   adjust self-extracting exe   -J   junk zipfile prefix (unzipsfx)
      -T   test zipfile integrity       -X   eXclude eXtra file attributes
      -y   store symbolic links as the link instead of the referenced file
      -e   encrypt                      -n   don't compress these suffixes
      -h2  show more help
    $

Bu örneğimizde çapraz derleme için ``CC`` ve ``CXX`` değişkenlerini
belirlemek yeterli oldu. ``kBuild`` tarzı hazırlanmış Makefile'larda
``CROSS_COMPILE`` değişkeni üzerinden gerekli çapraz derleyici
ve diğer araçlar belirlenebilir. Şöyle ki::

    Makefile içeriği:
    8<------8<------8<------8<------8<------8<------8<------8<------8<------

    HOSTCC       = gcc
    HOSTCXX      = g++
    HOSTCFLAGS   = -Wall -Wmissing-prototypes -Wstrict-prototypes -O2 -fomit-frame-pointer
    HOSTCXXFLAGS = -O2

    CROSS_COMPILE ?=

    AS      = $(CROSS_COMPILE)as
    LD      = $(CROSS_COMPILE)ld
    CC      = $(CROSS_COMPILE)gcc
    CPP     = $(CC) -E
    AR      = $(CROSS_COMPILE)ar
    NM      = $(CROSS_COMPILE)nm
    STRIP   = $(CROSS_COMPILE)strip
    OBJCOPY = $(CROSS_COMPILE)objcopy
    OBJDUMP = $(CROSS_COMPILE)objdump

    8<------8<------8<------8<------8<------8<------8<------8<------8<------

Çapraz derleme süresince, inşa işlemleri için kimi zaman PCnizde çalışması
gereken araçlar olabilir. Bunları cross-compiler ile inşa ettiğinizde
hedef platform için çalışacak ikililer oluşacağından direkt
çalıştırılamayacaktır. İnşa işlemi sırasında her bilgisayarda qemu gibi
bir emulator de olmayabilir. Bu sebepten ötürü ``HOSTCC`` gibi bir değişkenle
PC tarafında çalışacak uygulamalar derlenir. ``CROSS_COMPILE`` değişkeni
özellikle belirlenmediği sürece değişkenin içerisi boş kalacağından
native platformunuzda bulunan derleyiciler tarafından uygulamalar inşa
edilir.

Bu inşa yöntemini ``linux kernel``, ``busybox`` gibi araçlar kullanmaktadır.
Busybox için derleme işlemi örneği aşağıdaki gibidir::

      $ wget http://www.busybox.net/downloads/busybox-1.17.3.tar.bz2
      $ cd busybox-1.17.3
      $ make CROSS_COMPILE=arm-pardus-linux-gnueabi- -j10
        GEN     include/applets.h
        GEN     include/usage.h
        GEN     printutils/Kbuild
        GEN     printutils/Config.in
        GEN     findutils/Kbuild
        GEN     findutils/Config.in
        GEN     editors/Kbuild
        GEN     editors/Config.in
        GEN     console-tools/Kbuild

      ...

        SPLIT   include/autoconf.h -> include/config/*
        HOSTCC  applets/usage
        HOSTCC  applets/applet_tables
        GEN     include/usage_compressed.h
        GEN     include/bbconfigopts.h
        GEN     include/applet_tables.h
        CC      applets/applets.o
        HOSTCC  applets/usage_pod
        LD      applets/built-in.o
        DOC     busybox.pod
        DOC     BusyBox.txt
        DOC     BusyBox.1
        DOC     BusyBox.html
        LD      archival/built-in.o
        CC      archival/bbunzip.o
        CC      archival/bzip2.o
        CC      archival/cpio.o

      ...

        CC      libbb/xfunc_die.o
        CC      libbb/xfuncs.o
        CC      libbb/xfuncs_printf.o
        CC      libbb/xgetcwd.o
        CC      libbb/xreadlink.o
        CC      libbb/xgethostbyname.o
        CC      libbb/xrealloc_vector.o
        CC      libbb/xregcomp.o
        AR      libbb/lib.a
        AR      shell/lib.a
        LINK    busybox_unstripped
      Trying libraries: crypt m
       Library crypt is not needed, excluding it
       Library m is not needed, excluding it
      Final link with: <none>

      $

Test işlemine geçelim::

    $ file busybox
    busybox: ELF 32-bit LSB executable, ARM, version 1 (SYSV), statically linked, for GNU/Linux 2.6.35, stripped
    $ qemu-arm-debug ./busybox
    qemu: uncaught target signal 11 (Segmentation fault) - core dumped
    zsh: segmentation fault  qemu-arm-debug ./busybox
    $ readelf -d busybox

    There is no dynamic section in this file.
    $

Busybox statik derlendiğinden bir segfault aldık. Daha önce yazmış olduğumuz
sarmalayıcı ``qemu-arm-debug`` betiğinde bir dinamik yükleyici ile uygulamaları
çalıştıracağımızı belirtmiştik. Statik derlenmiş bir ikili dinamik yükleyiciye
ihtiyaç duymaz. Herhangi bir dynloader kullanmadan direkt ``qemu-arm`` ile
çalıştırdığımızda sorun çıkmayacaktır. (daha temiz bir çözüm ilerleyen aşamalarda
verilecek)::

    $ qemu-arm ./busybox
    BusyBox v1.17.3 (2011-08-24 23:20:08 EEST) multi-call binary.
    Copyright (C) 1998-2009 Erik Andersen, Rob Landley, Denys Vlasenko
    and others. Licensed under GPLv2.
    See source distribution for full notice.

    Usage: busybox [function] [arguments]...
       or: function [arguments]...

            BusyBox is a multi-call binary that combines many common Unix
            utilities into a single executable.  Most people will create a
            link to busybox for each function they wish to use and BusyBox
            will act like whatever it was invoked as.

    Currently defined functions:
            [, [[, ash, awk, basename, blkid, bunzip2, bzcat, bzip2, cat, chgrp, chmod, chown, chroot, clear, cp,
            cpio, cut, date, dd, df, dirname, dmesg, dnsdomainname, du, echo, egrep, false, fdisk, fgrep, find,
            findfs, free, fsck, fuser, grep, gunzip, gzip, halt, head, hostname, hwclock, ifconfig, insmod, kill,
            killall, less, ln, loadfont, loadkmap, losetup, ls, lsmod, mkdir, mknod, mktemp, modinfo, modprobe,
            more, mount, mv, pidof, ping, poweroff, printf, ps, pwd, readlink, reboot, reset, rm, rmdir, rmmod,
            route, sed, seq, setkeycodes, sh, sha1sum, sleep, sort, stat, strings, switch_root, sync, tail, tar,
            tee, test, time, touch, tr, true, udhcpc, umount, uname, uniq, unxz, unzip, usleep, vi, wc, which,
            xargs, xz, xzcat, zcat

İnşa için ``kBuild`` kullanılmış yazılımlarda çapraz derlemede pek sıkıntı
yaşamazsınız.

İnşa sistemleri
---------------

GNU projelerinde taşınabilirlik, özelleştirilebilirlik ve platformlardan
bağımsızlık önemsenir. Hali hazırda kullanılan dağıtımların her biri farklı
amaçlar için sistemlerini özelleştirirler, kimileri bir kitaplığın desteğini
verirken başkaları bir kitaplığın desteğini gereksiz görüp sistemlerine dahil
etmek istemeyebilir. Bunun yanında Linux, MacOSX ve Windows altında
uygulamaların çalışması istenebilir.

Bu durumda yazılımın kaynak kodları içerisinde şartlı derlemeler için çeşitli
``makro`` lar yerleştirilir ve inşa esnasında da çeşitli testlerle sistemde
bulunan kitaplıklar/başlıklar/kitaplık versiyonları vs. belirlenir. İnşa
sistemleri bu testlerin sonuçlarında ``Makefile(lar)`` ve çeşitli ``config.h``
lar oluşturur. Oluşturulan bu Makefile(lar) ile yazılımın kolayca derlenmesi
amaçlanır.

Doğal derleme esnasında, yani hedef mimari ve sistemin derleme yapılan ortam
ile aynı olan bir sistemde bu testler sorunsuz yapılabilir. Ancak çapraz derleme
yapılacağında belirli testlerde sıkıntılar çıkmakta ve bu testleri aşmak için
çeşitli workaround lar ile uğraşmak zorunda kalınabilinir.

autotools
~~~~~~~~~

autotools GNU projelerinde kullanılan en yaygın ve uzun zamandır kullanılan
bir inşa sistemidir. autotools içerisinde libtool, automake, autoconf, autoheader
vs. gibi araçları barındırır. Bu araçların her birisini ayrı ayrı ele almayacağız,
yalnızca genel olarak autotools ile çapraz derlemenin nasıl yapıldığı üzerinde
duracağız.

Daha önce de belirtildiği gibi bir yazılım inşa edilirken çeşitli testler
yapılır. Bu testler sistemin mimarisi, sistemde kullanılan kitaplıklar,
bu kitaplıkların versiyonları, bir fonksiyonun davranışı, -eğer kullanılacaksa-
sistemde bulunan bir uygulamanın yeri vs. olabilir. Hatta isterseniz kendiniz
autotools'a bir takım testler yaptırıp sonuçlarını kullanabilirsiniz.

Çapraz derleme esnasında autotools'da yapılan testlerin bir kısmı rahat bir
şekilde yapılabilirken bir takım testler yapılamaz (şeffaf çapraz derlemede bu
durum biraz farklı). Örneğin bir fonksiyonun geri döndürdüğü değer testi
yapılırken, ilgili fonksiyon için kullanılan kod parçası çapraz derleyici
ile derlenir. Derlenen ikili çalıştırılıp sonucu değenlendirileceğinde, farklı
platform için derlenen uygulama direkt çalıştırılamayacağından inşa işlemi
çakılacaktır. Bu işlem için ``xorg-app`` paketindeki ``xcompmgr`` aracının
``configure`` scriptine bakabiliriz::

    { $as_echo "$as_me:$LINENO: checking whether malloc(0) returns NULL" >&5
    $as_echo_n "checking whether malloc(0) returns NULL... " >&6; }
    if test "x$MALLOC_ZERO_RETURNS_NULL" = xauto; then
        if test "$cross_compiling" = yes; then
    { { $as_echo "$as_me:$LINENO: error: in \`$ac_pwd':" >&5
    $as_echo "$as_me: error: in \`$ac_pwd':" >&2;}
    { { $as_echo "$as_me:$LINENO: error: cannot run test program while cross compiling
    See \`config.log' for more details." >&5
    $as_echo "$as_me: error: cannot run test program while cross compiling
    See \`config.log' for more details." >&2;}
    { (exit 1); exit 1; }; }; }
    else
    cat >conftest.$ac_ext <<_ACEOF

    char *malloc();
    char *realloc();
    char *calloc();
    main() {
        char *m0, *r0, *c0, *p;
        m0 = malloc(0);
        p = malloc(10);
        r0 = realloc(p,0);
        c0 = calloc(0);
        exit(m0 == 0 || r0 == 0 || c0 == 0 ? 0 : 1);
    }
    _ACEOF

Gördüğünüz gibi test için ufak bir kod parçası çalıştırılmaya çalışılmakta
ve çapraz derleme esnasında bu test yapılamayacağından daha testler yapılmadan
inşa işlemi sonlandırılmakta.

Bu durumlarda autotools'a bu testlerin sonuçları hazır verilmelidir::

    $ cat > cache << __EOF
    ac_cv_func_malloc_0_nonnull=yes
    ac_cv_func_calloc_0_nonnull=yes
    ac_cv_func_realloc_0_nonnull=yes
    __EOF
    $ ./configure --build=`gcc -dumpmachine` --host=arm-pardus-linux-gnueabi \
        --cache-file=cache

Bu testlerin sonuçlarını bulmak kimi zaman oldukça fazla zaman alabilmektedir.
Bu uygulamada toplamda 3 adet test için bir board içerisinde, configure scriptinin
içerisine ufak debug bilgileri yazarak ``native`` derleme ile test sonuçlarını
görebiliyoruz, ancak kimi uygulamaların inşalarında kimi zaman 15-20 ayrı test
sonucunu başka elle vermeniz gerekebilir.

PiSi'de yapılan önceki değişikliklerde ``cachefile``'ı parametre olarak ``autotools``
modülünde şu şekilde veriliyordu::

    # -*- coding: utf-8 -*-
    #
    # Copyright 2010 TUBITAK/UEKAE
    # Licensed under the GNU General Public License, version 2.
    # See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

    from pisi.actionsapi import crosstools as autotools

    def setup():
        cache = [ "ac_cv_func_malloc_0_nonnull=yes",
                  "ac_cv_func_calloc_0_nonnull=yes",
                  "ac_cv_func_realloc_0_nonnull=yes" ]

        autotools.autoreconf("-vif")
        autotools.configure("--disable-static", cache=cache)

    def build():
        autotools.make()

    def install():
        autotools.install()

Şu anda PARM inşası için şeffaf çapraz inşa yöntemini kullandığımızdan cache
hazırlama işleri ile uğraşmak zorunda değiliz.

cmake
~~~~~

cmake autotools'a göre nispeten daha konforlu bir inşa sistemidir. autotools
çok dağıtık bir yapıya sahiptir ve semantik açıdan cmake'e göre daha çirkindir.
cmake ayrıca birçok işletim sistemini desteklemektedir. Açık kaynak
geliştirdiğiniz uygulamalarda cmake kullanırsanız bütün platformlarda
rahat bir şekilde derleme yapabilirsiniz.

Çapraz derleme esnasında cmake değişkenlerini belirlemeniz veya bir toolchain
file oluşturmanız gerekmekte. PiSi için yapılan ilk değişikliklerde actionsapi'ler
içerisinde parametere olarak cmake'e gerekli parametreler verilmekteydi.
şeffaf derleme yöntemi ile sistemi inşa ettiğimizde, toolchain file ile
bu değişkenler verilmeye başlandı.

cmaketools.py içeriğindeki önceki kullanım::

    8<------8<------8<------8<------8<------8<------8<------8<------8<------
    ...

    # environment, içerisinde çevresel değişkenleri barındıran bir dictionary

    if can_access_file(join_path(sourceDir, 'CMakeLists.txt')):
        args = 'cmake -DCMAKE_INSTALL_PREFIX=%(installPrefix)s \
                      -DCMAKE_C_COMPILER="%(CC)s" \
                      -DCMAKE_C_FLAGS="%(CFLAGS)s" \
                      -DCMAKE_CXX_FLAGS="%(CXXFLAGS)s" \
                      -DCMAKE_LD_FLAGS="%(LDFLAGS)s" \
                      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
                      %(parameters)s %(sourceDir)s' % environment

        if system(args):
            raise ConfigureError(_('Configure failed.'))
    else:
        raise ConfigureError(_('No configure script found for cmake.'))

    8<------8<------8<------8<------8<------8<------8<------8<------8<------

toolchain file oluşturarak çapraz inşa::

    <toolchain-dir>/parm.cmake:
    8<------8<------8<------8<------8<------8<------8<------8<------8<------
    set(CMAKE_C_COMPILER   arm-pardus-linux-gnueabi-gcc)
    set(CMAKE_CXX_COMPILER arm-pardus-linux-gnueabi-g++)

    set(CMAKE_FIND_ROOT_PATH "/var/cross/sysroots/armv7l")
    set(CMAKE_SYSTEM_PREFIX_PATH ${CMAKE_FIND_ROOT_PATH})
    set(CMAKE_SYSTEM_LIBRARY_PATH ${CMAKE_SYSTEM_PREFIX_PATH}/lib ${CMAKE_SYSTEM_PREFIX_PATH}/usr/lib)

    set(CMAKE_SHARED_LINKER_FLAGS "-L${CMAKE_SYSTEM_PREFIX_PATH}/lib -Wl,-rpath-link,${CMAKE_SYSTEM_PREFIX_PATH}/lib \
                                   -L${CMAKE_SYSTEM_PREFIX_PATH}/usr/lib -Wl, -rpath-link,${CMAKE_SYSTEM_PREFIX_PATH}/usr/lib \
                                   -L${CMAKE_SYSTEM_PREFIX_PATH}/usr/qt/4/lib -Wl,-rpath-link,${CMAKE_SYSTEM_PREFIX_PATH}/usr/qt/4/lib \
                                   -L${CMAKE_SYSTEM_PREFIX_PATH}/usr/qt/3/lib -Wl,-rpath-link,${CMAKE_SYSTEM_PREFIX_PATH}/usr/qt/3/lib" )

    set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM BOTH) # sb2 build, ARM executables can be run
    set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
    set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

    set(CMAKE_C_HAS_ISYSROOT "yes")

    set(CMAKE_LIBRARY_PATH "${CMAKE_SYSTEM_LIBRARY_PATH}" "${CMAKE_FIND_ROOT_PATH}/usr/qt/4/lib" "${CMAKE_FIND_ROOT_PATH}/usr/qt/3/lib")

    set(KDESupport_SOURCE_DIR "${CMAKE_SYSTEM_PREFIX_PATH}/usr/lib")

    set(AUTOMOC4_MOC_HEADERS "${CMAKE_SYSTEM_PREFIX_PATH}/usr/qt/4/include")
    set(AUTOMOC4_ADD_LIBRARY QT SHARED "${CMAKE_SYSTEM_PREFIX_PATH}/usr/qt/4/lib")

    set(QT_INCLUDE_DIR  "${CMAKE_SYSTEM_PREFIX_PATH}/usr/qt/4/include")
    set(QT_LIBRARY_DIR "${CMAKE_SYSTEM_PREFIX_PATH}/usr/qt/4/lib")
    set(QT_LIBRARIES  "${CMAKE_SYSTEM_PREFIX_PATH}/usr/qt/4/lib")
    set(QT_MOC_EXECUTABLE "${CMAKE_SYSTEM_PREFIX_PATH}/usr/qt/4/bin/moc")
    set(QT_UIC_EXECUTABLE "${CMAKE_SYSTEM_PREFIX_PATH}/usr/qt/4/bin/uic")
    set(QT_UIC3_EXECUTABLE "${CMAKE_SYSTEM_PREFIX_PATH}/usr/qt/4/bin/uic3")
    set(QT_RCC_EXECUTABLE "${CMAKE_SYSTEM_PREFIX_PATH}/usr/qt/4/bin/rcc")
    8<------8<------8<------8<------8<------8<------8<------8<------8<------

    cmaketools.py:
    8<------8<------8<------8<------8<------8<------8<------8<------8<------
    ...
    args = 'cmake -DCMAKE_INSTALL_PREFIX=%s \
                  -DCMAKE_C_FLAGS="%s" \
                  -DCMAKE_CXX_FLAGS="%s" \
                  -DCMAKE_LD_FLAGS="%s" \
                  -DCMAKE_BUILD_TYPE=RelWithDebInfo %s %s' % (installPrefix, get.CFLAGS(),
                        get.CXXFLAGS(), get.LDFLAGS(), parameters, sourceDir)

    if crosscompiling:
        args = "sb2 %s -DCMAKE_TOOLCHAIN_FILE=/opt/toolchain/%s/parm.cmake" % (args, arch)
    ...
    8<------8<------8<------8<------8<------8<------8<------8<------8<------

sysroot kullanarak çapraz derleme
---------------------------------
Bir uygulama bir veya daha çok kitaplığa ve bu kitaplığa ait başlıklara
çalışma anında ve derlenme anında ihtiyaç duyabilir. Bu bağımlılıkların
ya kitaplıklarını toolchain'e ait sysroot'un içerisindeki ``lib/`` dizinine,
başlık dosyalarını da ``include/`` dizinine atmanız gerekmektedir.

Embedded sistemler için oluşturulmuş ``custom`` SDK'larda gerekli kitaplıklar
bu şekilde verilebilir. Ancak iş bütün dağıtımın tamamı ile uğraşmaya gelince
bağımlılıkları toolchain içerisine atmak kitaplıkların sayısı göz önünde
bulundurulduğunda pek mantıklı değildir.

Dağıtımı başka bir platforma uyarlama esnasında, bu sebepten dolayı bir
``sysroot`` dizini oluşturuldu ve bütün bağımlılıklar bu ``sysroot`` dizini
içerisinden kontrol edildi::

    variables.py
    8<------8<------8<------8<------8<------8<------8<------8<------8<------
    ...

    # if we are crosscompiling, some extra flags and variables has to be defined.
    if values.build.crosscompiling:
        # Toolchain environmental variables
        os.environ["AR"]      = "%s-ar" % values.build.host
        os.environ["AS"]      = "%s-as" % values.build.host
        os.environ["LD"]      = "%s-ld" % values.build.host
        os.environ['NM']      = "%s-nm" % values.build.host
        os.environ["STRIP"]   = "%s-strip"   % values.build.host
        os.environ["RANLIB"]  = "%s-ranlib"  % values.build.host
        os.environ["OBJDUMP"] = "%s-objdump" % values.build.host
        os.environ["OBJCOPY"] = "%s-objcopy" % values.build.host
        os.environ['FORTRAN'] = "%s-gfortran" % values.build.host

        os.environ['PYTHON_INCLUDES'] = "-I%s/usr/include/python2.6" % sysroot
        os.environ['PYTHON_LIBS']   = "-I%s/usr/lib/python2.6" % sysroot
        os.environ['PYTHON_PREFIX'] = "%s/usr" % sysroot
        os.environ['PYTHONPATH']    = "%s/usr/lib/python2.6" % sysroot
        os.environ['PYTHON']        = "%s/usr/bin/python" % sysroot
        os.environ['SBOX_TARGET_ROOT'] = sysroot
        os.environ['SYSROOT']   = sysroot
        os.environ['BUILDARCH'] = os.popen('uname -m').read().strip()
        os.environ['ARCH']      = values.general.architecture

        os.environ['ASFLAGS']   = ""
        os.environ['CPPFLAGS'] += " -isystem%s/usr/include" % sysroot
        os.environ['CFLAGS']   += " -I%s/usr/include" % sysroot
        os.environ['CXXFLAGS'] += " -I%s/usr/include" % sysroot
        os.environ['LDFLAGS']  += " -L%(sysroot)s/lib -Wl,-rpath-link,%(sysroot)s/lib \
                                    -L%(sysroot)s/usr/lib -Wl,-rpath-link,%(sysroot)s/usr/lib \
                                    " % { 'sysroot' : sysroot, }

        os.environ['PKG_CONFIG_SYSROOT_DIR']  = sysroot
        os.environ['PKG_CONFIG_DISABLE_UNINSTALLED']  = "yes"
        os.environ['PKG_CONFIG_ALLOW_SYSTEM_CFLAGS']  = "yes"
        os.environ['PKG_CONFIG_ALLOW_SYSTEM_LIBS']    = "yes"
        os.environ['PKG_CONFIG_LIBDIR'] = "%s/usr/lib/pkgconfig" % sysroot
        os.environ['PKG_CONFIG_PATH']  = "%s/usr/lib/pkgconfig:%s/usr/share/pkgconfig:%s/usr/qt/4/lib/pkgconfig:%s/usr/qt/3/lib/pkgconfig" % (sysroot, sysroot, sysroot, sysroot)
        os.environ['PATH'] = "%(path)s:%(sysroot)s/bin:%(sysroot)s/sbin:%(sysroot)s/usr/bin:%(sysroot)s/usr/sbin:%(sysroot)s/usr/qt/3/bin:%(sysroot)s/usr/qt/4/bin" % {\
            'sysroot' : sysroot,
            'path'    : os.environ['PATH'] }
    8<------8<------8<------8<------8<------8<------8<------8<------8<------

