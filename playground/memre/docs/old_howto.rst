================
Pardus ARM Nasıl
================

.. contents:: İçindekiler

Belge Hakkında
--------------
    :Yazar: Mehmet Emre Atasever (memre ~ pardus.org.tr)
    :Tarih: 07/09/2010
    :Konu: Pardus-ARM gelişim süreci ve Pardus-ARM geliştirme
    :Özet: Bu belge, Pardus'un ARM mimarisinde çalışacak şekilde uyarlanması sürecini açıklar.

           Bu belgeyi okuyan kişinin aşağıdaki konular hakkında bilgi sahibi olduğu varsayılmıştır:
            - Genel olarak mikroişlemciler
            - Temel Pardus Linux Yapısı
            - PiSi paket yapımı
            - GNU inşa araçları (ör: autotools, make)
            - bortu bocek
            - glibc nin tek seferde sorunsuz derlendiğini görüp, "oh be openembedded patchlerini
              mıncıklamak zorunda kalmayacağım" diye düşünüp mutlu olmak


Giriş
-----
    Pardus-ARM, gömülü sistemlerde Pardus çalıştırılması amacıyla başlamış bir projedir. Pardus,
    grafiksel arayüzü olan, son kullanıcı için kullanışlı bir işletim sistemi olmayı hedeflediğinden
    güçlü ARM cihazların desteklenmesi uygun görülmüştür.

    ARM, gömülü sistemlerde sık kullanılan güçlü bir mimaridir [#]_. Son zamanlarda ARM mimarisini,
    Cortex-A serisi gibi, üzerine çeşitli ek üniteler eklenmiş çiplerde görmekteyiz. Cortex-A serisi
    [#]_, standart gömülü sistemlerden daha fazla işlem yüküne sahip sistemlerin iş yükünü kaldırabilecek,
    aynı zamanda az güç tüketecek şekilde tasarlanmıştır. Cortex-A serisi işlemciler içerisinde
    Cortex-A5,A8,A9,A15 ürünleri vardır ve bunların içerisinde en yaygın kullanılanı, stabilitesini
    ispatlamış olan Cortex-A8 dir [#]_. Cortex-A8 i hemen hemen bütün yeni nesil cep telefonlarında
    ve ARM tabanlı tablet-pc lerde görebilirsiniz.

    Yeni nesil cep telefonları, tablet-pc ler, pad ler vs. incelediğinizde aygıtın hızı, grafiklerdeki
    kalite, matematiksel işlemlerdeki hız, ... dikkatinizi çekmiştir. Bu performansı sunan, Cortex-A
    serisi (ve benzeri) işlemcilerin yanınına eklenen grafiksel ve matematiksel işlemleri yapacak ek
    ünitelerdir. Bu platformlara  Texas Instruments ın OMAP platformunu [#]_, Apple A4 işlemcisini [#]_
    veya Qualcomm un Snapdragon mobil işlemcisi [#]_ örnek olarak gösterebiliriz. Biz denemelerimizi
    üzerinde OMAP3530 bulunan beagleboard [#]_ isimli board üzerinde yaptık. Beagleboard fiyat açısından
    makul, herkesin rahatlıkla temin edebileceği bir board olduğundan, gönüllü geliştiricilerimiz de
    bu board lardan alıp deneme yapabilirler.

    ARM hakkında bu kadar donanımsal bilgi verdikten sonra biraz da yazılımsal anlamda neler yaptığımızdan
    bahsedelim. Bir dağıtımı, başka bir mimariye uyarlama işleminde birden çok yöntem kullanılabilir.
    Örneğin hedef mimaride çalışan herhangi bir dağıtımı host sistem olarak kullanıp, dağıtımı bu mimaride
    yavaş yavaş derlemek, veya yazılımları inşa etmek için, inşa araçlarının bir kısmını çapraz ve static
    derleyip, static derlenmiş geçici sistem ile toolchain oluşturulması ve bu toolchain ile bütün
    sistemin baştan derlenmesi gibi çok aşamalı, çoğu zaman sinir bozucu bir yöntem de kullanılabilir.
    Ancak bu yöntemlerin uygulanması, hedef mimari dağıtımınızı hızlı bir şekilde inşa edecek kadar
    güçlüyse anlamlıdır (lakin biz de bu şekilde Pardus-ARM ı inşa etmeyi denemedik değil).

    Sisteminiz, üzerinde derleme yapmaya elverişli bir sistem değilse, kendi sisteminizde çalışıp (x86_64
    mesela) sistemi çapraz olarak inşa etmeniz daha anlamlı olabilir.

    FIXME: (çapraz derlemenin avantajları dezavantajları ...)

    Biz Pardus u ARM a, Slackware-ARM host sistemi üzerinde doğal derleme yöntemi ile başladık. Sonra
    ARM üzerinde doğal derleme yapmanın çok zaman alması üzerine çapraz derleme yöntemine geçmek zorunda
    kaldık ve Aralık-2009 tarihinden itibaren çalışmalarımız bu yönde ilerledi.

    Çapraz derleme doğal derlemeye kıyasla daha uğraştırıcıdır. İnşa sistemleri (ör: autotools) yazılımı
    derlemeden önce, yazılımın üzerinde çalışacağı platformu test eden kod parçaları derler veya
    çalıştırırlar. Hedef sistem için derlenmiş bir ikili dosya, host sistem üzerinde çalıştırılamaz,
    sonuçta mimari farkı var. Böylelikle inşa işlemi başarısız olur. Bu durumda inşa sistemi ile ilgili
    hack ler yapmak gerekir, bazı kısımların derlenmemesi sağlanır, bazı testlerin sonuçları verilir
    ve testler atlatılır. Bu gibi taklalar sonucunda paketler hazırlanır. (daha formal bir şekilde yaz)

    Şimdi Pardus-ARM paketlerinin nasıl oluşturulacağını ve Pardus-ARM oluştururken karşıma çıkan kimi
    zaman abuk kimi zaman saç baş yoldurtan hataları ve çözüm yollarını yazacağım.

Gelişim süreci
--------------
    #. Native build
        İlk deneyimimizi bu şekilde gerçekleştirdik. Bu şekilde çalışamayacağımızı anladığımızda
        çapraz derleme ile yolumuza devam etme kararı aldık.

    #. clfs
        Cross Linux From Scratch projesinden esinlenerek bir sistem oluşturuldu ve yavaş yavaş paketler
        Pardus-2009 a benzetilmeye çalışıldı. Sonrasında Pardus-2009 deposunu olduğu gibi port etmeye
        başladık.

    #. Fatih'in tavsiyesi üzerine, daha güncel bir süsüm olan Corporate2'ye geçiş yapıldı.

    #. çalışabilir bir sistem çıktı

    #. yıllık izine çıktık

    #. ramazan ayına girdik, o ara pisi-farm mıncıklandı, buildno lu paketler çıktı ortaya, gerekli mi
        bilinmez (hala çalışmayan bir pisi var elimizde, eskiden en azından çalışıyordu :) )

    #. farm ile build-no su olan paketler inşa edildi, bazı paketlerde sorunlar çıktı. buildfarm böcüklü

    #. Toolchain oluşturma
        Başta toolchain i baştan sona kendim oluşturmaya çalıştıysam da oluşan sorunlardan ötürü crosstool-ng
        aracını kullanmaya karar verdim. Bu araçla birçok toolchain oluşturdum, sebebi sorunlar başlığı altında.

        - uboot-native mkimage

          Birçok gömülü cihaz içerisinde NAND flash gelmektedir. İlk boot sürecinde NAND flash ın ilk
          sektörüne jump edilip çalıştırılmaya başlanmaktadır.

          Beagleboard'da ilk sektörlerde x-loader ve sonraısnda u-boot gelmektedir. u-boot kernel'i boot eden
          loader'dır. x-loader ile u-boot u BIOS ve grub a benzetebiliriz. x-loader her cihazda kullanılmasa
          da u-boot kullanan cihaz sayısı oldukça fazladır.

          u-boot un kernel i boot edebilmesi için, kernel'e bir header eklemesi gerekmektedir. Bunu ``mkimage``
          isimli uygulama yapmaktadır ve bu derlemenin yapıldığı makinede yapılmalıdır (yani sizim PC niz).
          Bunu ufak uygulamayı bu sebeple toolchain e eklemeyi uygun gördük.

        - python-native

          Python paketi derlenirken 2 aşamalı derleme yapılmaktadır. Öncelikle native derlenmiş python ve
          python paketinin derlenme aşamasında derlenip pakete alınmayan pgen isimli uygulamanın native
          derlenmesi gerekmektedir. Sonrasında native derlenen python ve pgen ile python paketinin
          kalan kısmı derlenmektedir.

          Bu 2 aşamalı derlemeyi yapmanın 2 yaklaşımı vardır. İlki native derlenmiş olan python ve pgen i
          toolchain içersine dahil etmek, diğeri de python paketine pgen'i de almak. Ancak cross-build
          yapmayacak kişiler için gereksiz bir uygulamanın pakete girmesi uygun olmayabilir. Pardus-ARM ı
          2011 tabanlı yapmış olsaydık pgen i python-devel e de alınabilirdi.

          Ayrıca libpython2.6 ve python headers ın toolchain içerisinde kalması gerekmekte, build esnasında
          sandbox hataları almaktayız.

          Konunun geliştirici listesinde tartışmaya açılmasında fayda var.

        - Gettext

          glibc derlenirken gettext ile ilgili çember bağımlılık sorunu ile karşılaştım. gettext derlenmesi için
          glibc gerekmekte, ancak glibc de gettext e build esnasında ihtiyaç duyuyor. Bu durumda toolchain
          içerisinde bulunan glibc ile gettext i derleyip, toolchain'in içerisine attım.

        - perl-native ve perl [#]_

          Perl derlemek gerçekten bir işkence. Perl i cross derlemek tarif edilemez :). Perl derlenirken miniperl
          isimli, pakete alınmayan bir uygulama derleniyor. Bu uygulama cross-build yapılırken de gerekmekte olduğu
          için aynı pythondaki gibi 2 aşamalı bir build gerekiyor.

          Buradaki sorunu perl-native i toolchain içerisine alarak çözdüm.

        - mesa

          mesa derlenirken de 2 aşamalı derleme yapıldı. ya bu geçici dosyalar devel paketlerine girsin,
          ya da toolchain e. aaa, öff.

actions.py değişiklikleri
-------------------------
    İlk actions.py ler şu aşağıdaki gibiydi::

        #!/usr/bin/python
        # -*- coding: utf-8 -*-
        #
        # Copyright 2005-2009 TUBITAK/UEKAE
        # Licensed under the GNU General Public License, version 2.
        # See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

        from pisi.actionsapi import autotools
        from pisi.actionsapi import pisitools
        from pisi.actionsapi import libtools
        from pisi.actionsapi import shelltools
        from pisi.actionsapi import get

        _build="i686-pc-linux-gnu"
        _host="arm-cortex_a8-linux-gnueabi"
        _target=_host

        # ugly hard-coded stuff, unfortunately..
        _RootDir="/pardus-arm"
        _ToolchainDir = "/home/memre/x-tools"

        # Pardus-ARM preparation
        def prepare():
            shelltools.export("LC_ALL", "C")
            shelltools.export("CXXFLAGS", "-I%s/usr/include -L%s/usr/lib -L%s/lib" % (_RootDir, _RootDir, _RootDir))
            shelltools.export("CFLAGS",   "-I%s/usr/include -L%s/usr/lib -L%s/lib" % (_RootDir, _RootDir, _RootDir))
            shelltools.export("LDFLAGS",  "-L%s/usr/lib -L%s/lib" % (_RootDir, _RootDir))

            shelltools.export("CC",     "%s-gcc" % _target)
            shelltools.export("CXX",    "%s-g++" % _target)
            shelltools.export("AR",     "%s-ar"  % _target)
            shelltools.export("AS",     "%s-as"  % _target)
            shelltools.export("LD",     "%s-ld"  % _target)
            shelltools.export("RANLIB", "%s-ranlib"  % _target)
            shelltools.export("OBJDUMP","%s-objdump" % _target)
            shelltools.export("STRIP",  "%s-strip"   % _target)
            shelltools.export("LIBTOOL","%s-libtool" % _target)

        def setup():
            # Pardus-ARM preparation
            prepare()

            autotools.autoreconf("-fi")
            libtools.libtoolize("--force --install")
            autotools.configure("--disable-static --build=%s --host=%s" % (_build, _host))

        def build():
            # Pardus-ARM preparation
            prepare()

            autotools.make()

        def install():
            autotools.rawInstall("DESTDIR=%s" % get.installDIR())
            pisitools.removeDir("/usr/share/doc")

            pisitools.dohtml("doc/*")
            pisitools.dodoc("AUTHORS", "CHANGES", "README", "TODO")


    gördüğünüz başlık kısımlarını her port edilecek paketin actions.py sine yazmak pek akıllıca gelmediğinden
    autotools.py yi forklayıp crosstools.py isimli bir source içerisine pis kodları ekledim.

    Bu değişiklik sonrasında actions.py ler şu hale geldiler::

        #!/usr/bin/python
        # -*- coding: utf-8 -*-
        #
        # Copyright 2005-2010 TUBITAK/UEKAE
        # Licensed under the GNU General Public License, version 2.
        # See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

        from pisi.actionsapi import crosstools
        from pisi.actionsapi import pisitools
        from pisi.actionsapi import shelltools
        from pisi.actionsapi import get

        WorkDir = "glib-%s" % get.srcVERSION()

        def setup():
            shelltools.export("LC_ALL", "C")

            cache = [ "glib_cv_sizeof_gmutex=${glib_cv_sizeof_gmutex=24}",
                      "glib_cv_sizeof_system_thread=${glib_cv_sizeof_system_thread=4}",
                      "glib_cv_stack_grows=${glib_cv_stack_grows=no}",
                      "glib_cv_uscore=${glib_cv_uscore=no}",
                      "glib_cv_use_pid_surrogate=${glib_cv_use_pid_surrogate=yes}",
                      "glib_cv_has__inline=${glib_cv_has__inline=yes}",
                      "glib_cv_has__inline__=${glib_cv_has__inline__=yes}",
                      "glib_cv_hasinline=${glib_cv_hasinline=yes}",
                      "glib_cv_sane_realloc=${glib_cv_sane_realloc=yes}",
                      "glib_cv_sizeof_gmutex=${glib_cv_sizeof_gmutex=24}",
                      "glib_cv_uscore=${glib_cv_uscore=no}",
                      "glib_cv_va_copy=${glib_cv_va_copy=yes}",
                      "glib_cv_va_val_copy=${glib_cv_va_val_copy=yes}",
                      "glib_cv___va_copy=${glib_cv___va_copy=yes}",
                      "glib_cv_rtldglobal_broken=${glib_cv_rtldglobal_broken=no}",
                      "glib_cv_sys_pthread_mutex_trylock_posix=${glib_cv_sys_pthread_mutex_trylock_posix=yes}",
                      "glib_cv_sys_pthread_getspecific_posix=${glib_cv_sys_pthread_getspecific_posix=yes}",
                      "glib_cv_sys_pthread_cond_timedwait_posix=${glib_cv_sys_pthread_cond_timedwait_posix=yes}",
                      "glib_cv_long_long_format=${glib_cv_long_long_format=ll}",
                      "glib_cv_sizeof_gmutex=${glib_cv_sizeof_gmutex=24}",
                      "glib_cv_sizeof_intmax_t=${glib_cv_sizeof_intmax_t=8}",
                      "glib_cv_sizeof_ptrdiff_t=${glib_cv_sizeof_ptrdiff_t=4}",
                      "glib_cv_sizeof_size_t=${glib_cv_sizeof_size_t=4}",
                      "glib_cv_sizeof_system_thread=${glib_cv_sizeof_system_thread=4}",
                      "glib_cv_sys_use_pid_niceness_surrogate=${glib_cv_sys_use_pid_niceness_surrogate=yes}",
                      "ac_cv_c_littleendian=${ac_cv_c_littleendian=yes}",
                      "ac_cv_c_bigendian=${ac_cv_c_bigendian=no}",
                      "ac_cv_libnet_endianess=${ac_cv_libnet_endianess=lil}"
                      "ac_cv_func_lstat_dereferences_slashed_symlink=${ac_cv_func_lstat_dereferences_slashed_symlink=yes}",
                      "ac_cv_func_lstat_empty_string_bug=${ac_cv_func_lstat_empty_string_bug=no}",
                      "ac_cv_func_stat_empty_string_bug=${ac_cv_func_stat_empty_string_bug=no}",
                      "ac_cv_func_stat_ignores_trailing_slash=${ac_cv_func_stat_ignores_trailing_slash=no}",
                      "ac_cv_header_netinet_sctp_h=${ac_cv_header_netinet_sctp_h=no}",
                      "ac_cv_header_netinet_sctp_uio_h=${ac_cv_header_netinet_sctp_uio_h=no}",
                      "ac_cv_sctp=${ac_cv_sctp=no}",
                      "ac_cv_header_pwd_h=${ac_cv_header_pwd=yes}",
                      "ac_cv_func_posix_getpwuid_r=${ac_cv_func_posix_getpwuid_r=yes}",
                      "ac_cv_func_posix_getgrgid_r=${ac_cv_func_posix_getgrgid_r=yes}" ]

            crosstools.autoconf()
            crosstools.configure("--with-threads=posix \
                                  --disable-gtk-doc \
                                  --with-pcre=system \
                                  --disable-fam \
                                  --disable-static", cache=cache)

            pisitools.dosed("libtool", " -shared ", " -Wl,--as-needed -shared ")

        def build():
            crosstools.make()

        def install():
            crosstools.rawInstall("DESTDIR=%s" % get.installDIR())
            pisitools.removeDir("/usr/share/gtk-doc")

            pisitools.dodoc("AUTHORS", "ChangeLog*", "README*", "NEWS*")


    Yukarıdaki actions.py dosyası glib2 paketine ait. ``crosstools.configure`` methodu içerisindeki ``cache=cache``
    kısmının anlamı ise ``Sık karşılaşılan sinir bozucu sorunlar`` başlığı altında ``AC_TRY_RUN`` kısmında
    açıklanmıştır. cache, autotools'un AC_TRY_RUN ile çalıştıramadığı yapamadığı testleri configure scriptine
    parametre olarak verilerek kullanılır. Böylelikle autotools yapamadığı testlerin sonuçlarını buradan alıyor
    ve bu testleri yapmıyor.

    sys.devel ve sys.base paketlerinde, ``from pisi.actionsapi import crosstools`` satırları kullanıldıysa
    da diğer paketlerde ``from pisi.actionsapi import crosstools as autotools`` kullanılmıştır. Böylelikle
    paket üzerinde çok az değişiklik yaparak arm için derlenebilir yapabilirsiniz. Örnek bir actions.py aşağıdaki
    gibidir::

        #!/usr/bin/python
        # -*- coding: utf-8 -*-
        #
        # Copyright 2005-2010 TUBITAK/UEKAE
        # Licensed under the GNU General Public License, version 2.
        # See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

        from pisi.actionsapi import crosstools as autotools # **tek değişen satır**
        from pisi.actionsapi import pisitools
        from pisi.actionsapi import get

        WorkDir = "dialog-%s" % get.srcVERSION().replace('_','-')

        def setup():
            autotools.configure("--with-ncursesw \
                                 --enable-nls")

        def build():
            autotools.make()

        def install():
            autotools.rawInstall("DESTDIR=%s" % get.installDIR())

            pisitools.insinto("/usr/share/doc/%s/samples" % get.srcNAME(), "samples/*")
            pisitools.dodoc("CHANGES", "README")


    actionsapi ye crosstools.py eklemek de temiz bir çözüm değil aslında, pisi tarafında actionsapi nin
    tamamının elden geçirilmesi gerekiyor. cross-compiling sorunları ile uğraşırken yalnızca sistemi
    ayağa kaldırmak ve temelleri oturtmak için uğraştığımızdan ötürü pisi üzerinde değişiklik kısımlarını
    ertelemek zorunda kaldık.

Geliştirme aşamaları
--------------------
    Bu aşamaları direkt esgeçip binary paketleri install edip paketlerinizi taşıyabilirsiniz. Bu
    başlık altında kabaca toolchain oluşturma sonrası ilk aşamlar anlatılmıştır.

    * cross-toolchain oluşturma ve sysroot hazırlama

      cross-toolchain crosstools-ng ile oluşturuldu ve ek uygulamalar içerisine atıldı (bu konu ile
      ilgili **``toolchain oluşturma``** kısmına bakabilirsiniz.), bu toolchain i
      `şu <http://http://cekirdek.pardus.org.tr/~memre/pardus-arm/arm7/pardus-arm-toolchain.tar.bz2>`_
      adresten indirebilirsiniz. İndirdiğiniz toolchain i /opt/toolchain/arm dizini içerisine açın ve
      PATH değişkeninize /opt/toolchain/arm/bin dizinini ekleyin. arm-pardus-linux-gnueabi- prefix ine
      sahip uygulamalar göreceksiniz, bunlar toolchain e ait. Bunların haricinde birkaç script ve
      derlenmiş ikili dosyalarımız da mevcut, bunlar zaman içerisinde **``toolchain oluşturma``**
      kısmında bahsettiğimiz toolchain e eklenmiş olan dosyalar görecekseniz.

      Paketlerinizi taşırken öncelikle bir ``sysroot`` dizini oluşturmanız gerekmekte. ``sysroot`` dizini
      pisi.conf içerisine yazmaktadır, isterseniz değiştirebilirsiniz, default olarak /pardus-arm gelmekte.
      Bu dizini oluşturduktan sonra sırasıyla kernel-headers, glibc ve libgcc nin emerge edilmesi gerekmektedir
      (isterseniz pisi it -c system.base -c system.devel ile sysroot u hazırlayabilirsiniz,
      ``**Paketlerinizi nasıl taşıyacaksınız**`` kısmında bunu nasıl yapacağınız ile ilgili ayrıntılar var).

      Paketleri inşa ederken ``pisi`` ye ``--ignore-comar`` parametresini vermelisiniz. Çünkü ``postinstall``
      lar ilk boot esnasında yapılmalı.

      Şu sırayı paketleri inşa etmek için kullanacaksınız:

      #. İşlemleri yapabilmeniz için root haklarına sahip olmanız gerekmektedir, ``sudo su`` ile root
         olabilirsiniz.

      #. toolchain içerisine yazdığım ``chconf`` ile conf dosyasını Pardus-ARM için değiştirmeniz gerekmektedir.
         ``chconf arm`` ile konfigürasyon dosyasını değiştirebilirsiniz.

      #. Pardus-ARM repo sunu eklemelisiniz. ``pisi ar local_src ${arm_repo}/pisi-index.xml.bz2`` ile depoyu
         ekleyebilirsiniz.

      #. kernel.default.kernel içerisinden kernel-headers çıkmakta ve bu glibc nin inşası için gerekmektedir.

         - ÖNEMLİ! ``/opt/toolchain/arm/bin`` içerisinde ``kerneltools.py``, ``/usr/lib/pardus/pisi/actionsapi``
           içerisine kopyalanmalıdır, aksi taktirde inşa işleminiz çakılacaktır.

         ``pisi em kernel --ignore-comar`` ile bu işlemi yapabilirsiniz.

      #. İkinci aşamada system.base.glibc inşa edilmelidir.

         ``pisi em glibc --ignore-comar --ignore-dep`` ile bu işlemi yapabilirsiniz.

         - ``glibc`` nin inşası sonrasında CFLAG larına ``isystem${sysroot}`` parametresi crosstool.py içerisinde
           verilmekte ve bu aşama sonrasında c kitaplığı için ``sysroot`` içerisindeki c kitaplığı kullanılmaktadır.

      #. 3. aşamada system.devel.gcc içerisinden gelen ``libgcc`` ve ``libtool`` emerge edilmelidir.

         ``pisi em gcc --ignore-comar && pisi em libtool --ignore-comar`` ile bu işlemi yapabilirsiniz.

      #. Son aşamada ``baselayout`` paketini emerge etmeliyiz.

         ``pisi em baselayout --ignore-comar --ignore-dep`` ile bu işlemi yapabilirsiniz.

    * sys.devel, sys.base emerge işlemi

       #. ``system.devel`` componenti altındaki paketler bağımlılıklarına göre tek tek build edilmeli.
          Kimi paketler ``system.base`` içerisinde olduğunu hatırlatmak isterim. ``system.base``
          bağımlılığı olan paketlere gelene kadar bütün paketleri emerge edin.

       #. ``system.base`` paketlerini emerge edin. ``pisi em -c system.base`` komutu ile bu işlemi yapabilirsiniz,
          ancak an itibariyle system.base paketi için çember bağımlılık (circular dependency) sorunu var. Bu yüzden
          paketleri gruplar halinde emerge etmelisiniz.

       #. ``sys.base`` ve ``sys.devel`` paketlerinde emerge etmediğiniz, birbirine bağımlı diğer paketleri de
          emerge edin.

    * ``sys.devel`` ve ``sys.base`` haricinde kalan bütün componentler inşa edilmeye hazırdır. Bağımlılıklarına göre
      emerge edebilirsiniz. Kendi paketlerinizi taşımak için ``**Paketlerinizi nasıl taşıyacaksınız?**``
      başlığına bakabilirsiniz.

Paketlerinizi nasıl taşıyacaksınız?
-----------------------------------
    Sysroot u hazırlayıp, system.base ve system.devel i sysroot a ``postinstall`` suz install ettikten sonra kendi
    paketlerinizi Pardus-ARM a uyarlayabilirsiniz.

    Karşınıza çıkan sorunları ``Sık karşılaşılan sinir bozucu sorunlar`` başlığı altında büyük ihtimalle bulacaksınız,
    bulamazsanız sorunu geliştirici listesinde sormaktan çekinmeyin lütfen.

``sysroot`` hazırlama
~~~~~~~~~~~~~~~~~~~~~
    Şu aşamaları takip edip sysroot hazırlayabilirsiniz::

    $ pisi ar local_bin http://cekirdek.pardus.org.tr/~memre/pardus-arm/farm/packages/pisi-index.xml.bz2
    $ pisi it -c system.devel -c system.base kernel --ignore-dep --ignore-comar


Paket port etme
~~~~~~~~~~~~~~~
    GNU lisansı ile dağıtılan çoğu uygulama ``autotools`` kullanmaktadır. Autotools kullanan paketler için
    pisi'de ``actionsapi`` altında ``autotools.py`` apisi var. sorunları autotools sorunları altında 
    çözebilirsiniz. ayrıntı yazacam. port edilmiş paketleri inceleyip bilgi sahibi olabilirsiniz.

    zaten pisi yi değiştiriyorum, hiçbir değişikliğe gerek kalmadan çat diye uyarlayabileceksiniz :).

Sık karşılaşılan sinir bozucu sorunlar
--------------------------------------
absolute sembolik link sorunu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    En temel paketlerden olan zlib i sysroot a direkt ekleyince, paket içerisinde yapılmış olan absolute-path
    toolchain in linker inin çakılmasına sebep oldu. Şöyle ki::

        $ ls -l /usr/lib | grep 'libz\.'
        lrwxrwxrwx  1 root root        9 2010-08-20 12:06 libz.so -> libz.so.1
        lrwxrwxrwx  1 root root       13 2010-08-20 12:06 libz.so.1 -> libz.so.1.2.3
        lrwxrwxrwx  1 root root       18 2010-08-20 12:06 libz.so.1.2.3 -> /lib/libz.so.1.2.3


    bu sembolik bağlar aynen pardus-arm sysroot unda olunca, linker 8086 için derlenmiş olan **/lib/libz.so.1.2.3**
    kitaplığını bağlamaya çalışıp hata veriyor ve çıkıyordu. Bunun uzun bir süre linker ı suçlasak da sorunun
    kaynağını tespit ettik. linker ile ilgili bir hata alıyorsanız, ilk önce sembolik linklerin doğru olduğundan
    emin olun, kitaplık bağlayamıyor da linker gidip standart kitaplık dizinlerinden (``/lib``, ``/usr/lib``)
    bir kitaplık bağlıyorsa hata her zaman ``CFLAGS`` da veya ``linker`` da değildir.

glibc ve ``isystem`` sorunu
~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #. file libc.so
        Paketleri inşa ederken yöntem değiştirmenin ne kadar sakıncalı olduğuna dair bir kısmı yazıyorum şu anda.
        Muhtemelen 1-1,5 ay kadar bir süre bu sorunun neden kaynaklandığını anlayamamış ve defalarca toolchain i
        baştan oluşturup sistemi debug etsem de sorunu bulamamıştım. En sonunda tek tek paketleri incelemeye
        karar verdim. Adım adım hangi paketler derleniyor hangi paketler derlenmiyor denemesi yapıyordum.
        En sonunda, glibc nin sysroot a alınması ve CPPFLAGS a ``isystem${sysroot}`` parametresi değişikliği
        sonrası bu hataların oluştuğunu farkettim. "glibc nin içerisinden acaba 8086 için derlenmiş bir kod mu
        çıkıyor?" testi sonrasında şu gerçekle yüzleştim::

            $ export arm-sysroot=/var/cross/sysroot
            $ file ${arm-sysroot}/usr/lib/libc.so
            /var/cross/sysroot/usr/lib/libc.so: ASCII C program text
            $ cat ${arm-sysroot}/usr/lib/libc.so
            /* GNU ld script
            Use the shared library, but some functions are only in
            the static library, so try that secondarily.  */
            OUTPUT_FORMAT(elf32-i386)
            GROUP ( /lib/libc.so.6 /usr/lib/libc_nonshared.a  AS_NEEDED ( /lib/ld-linux.so.2 ) )
            $ 


        ``${arm-sysroot}/usr/lib/libc.so`` içerisindeki değerleri düzelttiğimizde diğer paketlerin düzgün inşa 
        edildiğini gördük::

            $ cat ${arm-sysroot}/usr/lib/libc.so
            /* GNU ld script
            Use the shared library, but some functions are only in
            the static library, so try that secondarily.  */
            OUTPUT_FORMAT(elf32-littlearm)
            GROUP ( ../../lib/libc.so.6 libc_nonshared.a  AS_NEEDED ( ../../lib/ld-linux.so.3 ) )
            $ 


        linker aslında doğru libc kitaplığını buluyor, ancak bu linker scripti, içerisinde kendi sistemimiz için
        kullanılan (8086 için derlenmiş) libc yi hedef gösterdiğinden inşa işlemi çakılıyor.

        1-1,5 aylık vaktimizi alan sorunun böylelikle üstesinden gelmiş oluyoruz, sorunu çözmüş olmak insanı sevindirse de 
        böylesine bir hatanın/dikkatsizliğin bu kadar zaman alması, Onur'un "toolchainde bir şeyler yanlış, bütün sistemi baştan
        inşa etmen gerekiyor" sözü, Akın'ın `değerli müziklerini <http://http://www.youtube.com/watch?v=yMx2SKIRkw4>`_ bizimle
        paylaşması bizi hüzne boğdu.


    #. CFLAG ları ve optimizasyonlar
        Optimizasyon tehlikeli bir iştir, ciddi okunarak yapılması gerekmektedir. ``-O3`` optimizasyonu cortex-a8 de
        "performans ı 4 kat artırıyor ve düzgün çalışıyor" tarzı bir blog okuyup bir iki pakette bunu denedim. sonrasında
        bütün depoyu tekrardan ``-O3`` ile derleyip deneme yaptım ve her bir uygulamanın segfault verdiği bir sistem elde ettim.
        Hatta öyle ki debug etmek imkansızdı (boot bile olmuyor, init çalışmıyor).

        ``-O3`` parametresinden vazgeçip, "normal performansta çalışsa da olur" deyip, ``-O2`` ve openembedded
        grubunun yaptığı birkaç optimizasyon ile sistemi tekarardan build ettiğimde hala segfault veren birçok
        uygulama olduğunu gördüm. toolchain i build ettiğim crosstools-ng aracının listesinde FORTIFY_SOURCE ile ilgili
        bir açık olduğunu öğrendim ve cross-toolchain i ve glibc'yi '-UFORTIFY_SOURCE ile yeniden build ettiğimde
        segfault veren uygulama kalmadığını gördüm. İlgili thread ı `buradan <http://comments.gmane.org/gmane.comp.gcc.cross-compiling/11513>`_
        okuyabilirsiniz.


``autotools`` sorunları
~~~~~~~~~~~~~~~~~~~~~~~
    #. build, host ve target parametreleri
       autotools tarafından oluşturulmuş configure parametresine --host parametresi verilerek farklı bir toolchain
       ile derleme yapması sağlanabilir. Yukarıda actions.py üzerinde bu parametre veriliyordu, şimdi ise crosstools.py
       tarafında bu iş hallediliyor.

    #. AC_TRY_RUN sorunu

       autotools testleri bazen bir fonksiyonun geri döndüreceği değerle ilgili testler yapabilir. çapraz derleme
       sırasında, test için derlenen uygulamalar ARM mimarisinde çalışacak şekilde hazırlandığından PC üzerinde çalışmıyor
       ve inşa çakılıyor::

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


       Bu durumda test sonucunu bir şekilde öğrenip, autotools a parametre olarak geçmek gerekmektedir.
       Mimari/ABI vs. ile ilgili ise board üzerinde native derleyerek sonucu görebilirsiniz, veya openembedded
       ekibi bu işi sizin yerinize yapmışsa onların testlerinin sonuçlarını alabilirsiniz (her zaman uyumlu
       olmayabilir oe patchleri, dikkat etmek lazım). sonuç olarak da actions.py de şu tarz girdiler yapmak
       zorunda kalabilirsiniz::

            #!/usr/bin/python
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


pkg-config sorunları
~~~~~~~~~~~~~~~~~~~~
    Bildiğiniz gibi pkg-config uygulamaları bir kitaplık ile ilgili CFLAG larını ve LDFLAG larını
    verir. İnşa esnasında gcc ye paramere olarak bu flaglar verilir. Kitaplıkların flaglar
    ile ilgili ayarları ``/usr/lib/pkgconfig`` dizini içerisinde bulunan ``.pc`` uzantılı
    dosyalarda bulunur. Örneğin alsa kitaplığı için ``alsa.pc`` içeriği ve örnek pkg-config
    çıktıları aşağıdaki gibidir::

        $ cat alsa.pc
        prefix=/usr
        exec_prefix=/usr
        libdir=${exec_prefix}/lib
        includedir=${prefix}/include

        Name: alsa
        Description: Advanced Linux Sound Architecture (ALSA) - Library
        Version: 1.0.23
        Requires: 
        Libs: -L${libdir} -lasound
        Libs.private: -lm -ldl -lpthread -lrt
        # -I${includedir}/alsa below is just for backward compatibility
        # (it was set so mistakely in the older version)
        Cflags: -I${includedir} -I${includedir}/alsa
        $ pkg-config --cflags alsa
        -I/usr/include/alsa
        $ pkg-config --libs alsa
        -lasound
        $ 


    Uygulamalarımızı derlerken, kendi sistemimizdeki header larımızı kullanmamız her zaman
    hataya sebep olmaz, ama bu yaklaşım yanlıştır. Ayrıca ``linker`` a kendi sisteminize ait
    kitaplıkların bulunduğu dizinlerin içerisine bakmasını söylerseniz 8086 için derlenmiş
    kitaplıkları bulduğunda bu kitaplıkları bağlamaya çalışacak ve inşa işleminiz çakılacaktır.

    ``pkg-config`` in dizinleri düzgün göstermesi için, ``sysroot`` olarak kullanılan
    dizinin tanımlanması gerekmektedir. Bunu kimi cross-build yapan kişiler direkt ``.pc``
    dosyalarını değiştirerek (``sed`` leme olarak tanımlanan işlem), kimileri pkg-config i
    yamalayarak halletmişler. İlk başlarda ``pkg-config`` çok sıkıntı olmadığından
    autotools üzerinde çeşitli hackler yaparak durumu düzeltme yoluna gittiysek de, sys.base
    sys.devel dışına çıkıp da multimedia ailesine girince pkg-config ciddi sıkıntı olmaya
    başladı ve ``pkg-config`` i bir script yardımıyla düzelttik::

        $ which pkg-config
        /opt/toolchain/arm/bin/pkg-config
        $ cat `which pkg-config`
        #!/bin/sh

        case "$*" in
            --cflags*|--libs*|--variable*)
                    if ! [ -z "$SYSROOT" ]; then
                        cross_fix_arg="--define-variable=prefix=$SYSROOT/usr --define-variable=exec_prefix=$SYSROOT/usr"
                    fi ;;
            *) cross_fix_arg= ;;
        esac

        /usr/bin/pkg-config $cross_fix_arg $*


    Her build esnasında ``SYSROOT`` değişkeni export edilmelidir. Sonuç aşağıdaki gibidir::

        $ export SYSROOT=/var/cross/sysroots/cortex-a8
        $ pkg-config --cflags --libs alsa
        -I/var/cross/sysroots/cortex-a8/usr/include -I/var/cross/sysroots/cortex-a8/usr/include/alsa  -L/var/cross/sysroots/cortex-a8/usr/lib -lasound
        $


    ``SYSROOT`` çevresel değişkenini export etme işi ``crosstools.py`` içerisinde yapımaktadır.
    Ayrıca ``PATH`` değişkeninin ilk değeri ``/opt/toolchain/arm/bin/`` olmalıdır ki build esnasında
    pkg-config çağrıldığında sistem ``/usr/bin/pkg-config`` i bulmasın.

python inşa işlemi
~~~~~~~~~~~~~~~~~~
    Aslında bu işlem için sizin yapacağınız bir şey kalmadı, pek hoşuma gitmeyen inşa
    sistemine sahip olan python u build etmek için oldukça fazla çaba harcamak zorunda
    kaldım. Birçok cross-compile yapan kişiler de aynı sorunlarla yüzleşmiş.

``strip`` sorunu
~~~~~~~~~~~~~~~~
    En çok başımızı ağrıtan, kimi kitaplıkların kodlarını incelememize sebep olan bir sorundan
    bahsediyorum.

    PiSi'nin inşa zamanında nasıl çalıştığını biliyorsunuz: setup, build, install işlemleri sonrasında
    paketleme yapılır. Paketleme yapılırken aynı zamanda kod içerisindeki debug sembollerini atmak için
    PiSi ``strip`` kullanır. Pisi'de strip işlemi ``util.py`` altında ``strip_file`` fonksiyonu altında
    ``run_strip`` fonksiyonu altında yapılmaktadır::

        def strip_file(filepath, fileinfo, outpath):
        """Strip an elf file from debug symbols."""
            def run_strip(f, flags=""):
                p = os.popen("strip %s %s" %(flags, f))
                ret = p.close()
                if ret:
                    ctx.ui.warning(_("strip command failed for file '%s'!") % f)


    Birçok kısımda ``strip`` herhangi bir soruna sebep olmasa da ``flex`` ve ``pam`` paketlerinde
    saç baş yolduran bir hata ile karşılaştık.

    Öncelikle ``flex`` i derliyoruz::

        $ cd system/devel/flex
        $ pisi bi pspec.xml
        Outputting packages in the working directory.
        Building PiSi source package: flex
        DEBUG: ComponentDB initialized in 0.0371789932251.
        DEBUG: RepoDB initialized in 0.0429599285126.
        DEBUG: InstallDB initialized in 0.0274591445923.
        Safety switch: system.devel is already installed
        PartOf tag not defined, looking for component
        Source is part of system.devel component
        flex-2.5.35.tar.gz [cached]
        Unpacking archive(s)...
        * Applying patch: flex-2.5.34-isatty.patch
          DEBUG: return value for "patch --remove-empty-files --no-backup-if-mismatch  -p0 < "/r/pardus/playground/memre/arm/corp2/system/devel/flex/files/flex-2.5.34-isatty.patch"" is 0
        * Applying patch: flex-2.5.35-signedwarn.patch
          DEBUG: return value for "patch --remove-empty-files --no-backup-if-mismatch  -p0 < "/r/pardus/playground/memre/arm/corp2/system/devel/flex/files/flex-2.5.35-signedwarn.patch"" is 0
        * Applying patch: fwrite_return.patch
          DEBUG: return value for "patch --remove-empty-files --no-backup-if-mismatch  -p1 < "/r/pardus/playground/memre/arm/corp2/system/devel/flex/files/fwrite_return.patch"" is 0
        * Applying patch: pic.patch
          DEBUG: return value for "patch --remove-empty-files --no-backup-if-mismatch  -p1 < "/r/pardus/playground/memre/arm/corp2/system/devel/flex/files/pic.patch"" is 0
        unpacked (/var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/work)
        Setting up source...
        Sandbox enabled build...
        autoreconf: Entering directory `.'
        autoreconf: running: true --force
        autoreconf: running: aclocal --force -I m4

        ...

        checking whether build environment is sane... yes
        checking for arm-pardus-linux-gnueabi-strip... arm-pardus-linux-gnueabi-strip
        checking for a thread-safe mkdir -p... /bin/mkdir -p
        checking for gawk... gawk
        checking whether make sets $(MAKE)... yes
        checking whether NLS is requested... no
        checking for msgfmt... /usr/bin/msgfmt
        checking for gmsgfmt... /usr/bin/msgfmt
        checking for xgettext... /usr/bin/xgettext
        checking for msgmerge... /usr/bin/msgmerge
        checking for style of include used by make... GNU
        checking for arm-pardus-linux-gnueabi-gcc... arm-pardus-linux-gnueabi-gcc
        checking whether the C compiler works... yes
        checking for C compiler default output file name... a.out
        checking for suffix of executables... 
        checking whether we are cross compiling... yes
        checking for suffix of object files... o

        ...

        config.status: creating config.h
        config.status: executing default-1 commands
        config.status: creating po/POTFILES
        config.status: creating po/Makefile
        config.status: executing depfiles commands

        ...

        DEBUG: return value for "./configure --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info --datadir=/usr/share --sysconfdir=/etc --localstatedir=/var/lib --libexecdir=/usr/libexec --build=i686-pc-linux-gnu --host=arm-pardus-linux-gnueabi --target=arm-pardus-linux-gnueabi --disable-nls --disable-dependency-tracking --cache-file=config.cache" is 0
        Building source...
        Sandbox enabled build...
        make  all-recursive
        make[1]: Entering directory `/var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/work/flex-2.5.35'
        Making all in .
        make[2]: Entering directory `/var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/work/flex-2.5.35'
        arm-pardus-linux-gnueabi-gcc -DHAVE_CONFIG_H -I.  -DLOCALEDIR=\"/usr/share/locale\" -I./intl -isystem/pardus-arm/usr/include  -march=armv7-a -mtune=cortex-a8 -mfpu=neon -mfloat-abi=softfp -pipe -fexpensive-optimizations -fomit-frame-pointer -frename-registers -O2 -ggdb3 -I/pardus-arm/usr/include -fPIC -c libmain.c
        arm-pardus-linux-gnueabi-gcc -DHAVE_CONFIG_H -I.  -DLOCALEDIR=\"/usr/share/locale\" -I./intl -isystem/pardus-arm/usr/include  -march=armv7-a -mtune=cortex-a8 -mfpu=neon -mfloat-abi=softfp -pipe -fexpensive-optimizations -fomit-frame-pointer -frename-registers -O2 -ggdb3 -I/pardus-arm/usr/include -fPIC -c libyywrap.c
        rm -f libfl.a
        arm-pardus-linux-gnueabi-ar cru libfl.a libmain.o libyywrap.o 
        arm-pardus-linux-gnueabi-ranlib libfl.a
        arm-pardus-linux-gnueabi-gcc -DHAVE_CONFIG_H -I.  -DLOCALEDIR=\"/usr/share/locale\" -I./intl -isystem/pardus-arm/usr/include -fPIC  -march=armv7-a -mtune=cortex-a8 -mfpu=neon -mfloat-abi=softfp -pipe -fexpensive-optimizations -fomit-frame-pointer -frename-registers -O2 -ggdb3 -I/pardus-arm/usr/include -fPIC -c -o libfl_pic_a-libmain.o `test -f 'libmain.c' || echo './'`libmain.c
        arm-pardus-linux-gnueabi-gcc -DHAVE_CONFIG_H -I.  -DLOCALEDIR=\"/usr/share/locale\" -I./intl -isystem/pardus-arm/usr/include -fPIC  -march=armv7-a -mtune=cortex-a8 -mfpu=neon -mfloat-abi=softfp -pipe -fexpensive-optimizations -fomit-frame-pointer -frename-registers -O2 -ggdb3 -I/pardus-arm/usr/include -fPIC -c -o libfl_pic_a-libyywrap.o `test -f 'libyywrap.c' || echo './'`libyywrap.c
        rm -f libfl_pic.a
        arm-pardus-linux-gnueabi-ar cru libfl_pic.a libfl_pic_a-libmain.o libfl_pic_a-libyywrap.o 
        arm-pardus-linux-gnueabi-ranlib libfl_pic.a
        arm-pardus-linux-gnueabi-gcc -DHAVE_CONFIG_H -I.  -DLOCALEDIR=\"/usr/share/locale\" -I./intl -isystem/pardus-arm/usr/include  -march=armv7-a -mtune=cortex-a8 -mfpu=neon -mfloat-abi=softfp -pipe -fexpensive-optimizations -fomit-frame-pointer -frename-registers -O2 -ggdb3 -I/pardus-arm/usr/include -fPIC -c ccl.c
        arm-pardus-linux-gnueabi-gcc -DHAVE_CONFIG_H -I.  -DLOCALEDIR=\"/usr/share/locale\" -I./intl -isystem/pardus-arm/usr/include  -march=armv7-a -mtune=cortex-a8 -mfpu=neon -mfloat-abi=softfp -pipe -fexpensive-optimizations -fomit-frame-pointer -frename-registers -O2 -ggdb3 -I/pardus-arm/usr/include -fPIC -c dfa.c
        arm-pardus-linux-gnueabi-gcc -DHAVE_CONFIG_H -I.  -DLOCALEDIR=\"/usr/share/locale\" -I./i

        ...

        make[1]: Leaving directory `/var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/work/flex-2.5.35'
        DEBUG: return value for "make DESTDIR=/var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/install install" is 0
        DEBUG: return value for "install -m0644 "NEWS" /var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/install/usr/share/doc/flex" is 0
        DEBUG: return value for "install -m0644 "README" /var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/install/usr/share/doc/flex" is 0
        strip: Unable to recognise the format of the input file `/var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/install/usr/bin/flex'
        strip command failed for file '/var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/install/usr/bin/flex'!
        DEBUG: /usr/bin/flex [stripped]
        strip: Unable to recognise the format of the input file `/var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/install/usr/lib/libfl_pic.a(libfl_pic_a-libyywrap.o)'
        DEBUG: /usr/lib/libfl_pic.a [stripped]
        strip: Unable to recognise the format of the input file `/var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/install/usr/lib/libfl.a(libyywrap.o)'
        DEBUG: /usr/lib/libfl.a [stripped]
        ** Building package flex
        Generating files.xml,
        Generating metadata.xml,
        Creating PiSi package ./flex-2.5.35-6-1.pisi.
        DEBUG: return value for "lzma -9 -z install.tar" is 0
        Done.
        All of the files under the install dir (/var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/install) has been collected by package(s)
        Keeping Build Directory
        *** 0 error(s), 1 warning(s)
        $ pisi it *pisi


    Yukarıdaki logda ``strip`` geri dönüş değerlerine ve hata çıktılarına dikkat etmenizi istiyorum. Bu kısma
    geri döneceğiz. Şimdi ``pam`` paketini inşa edelim::

        $ cd ../..
        $ cd base/pam
        $ pisi bi pspec.xml -dv

        ...

        Making all in pam_conv1
        make[3]: Entering directory `/var/cross/sysroots/cortex-a8/var/pisi/pam-1.1.1-28/work/Linux-PAM-1.1.1/conf/pam_conv1'
        make  all-am
        make[4]: Entering directory `/var/cross/sysroots/cortex-a8/var/pisi/pam-1.1.1-28/work/Linux-PAM-1.1.1/conf/pam_conv1'
        arm-pardus-linux-gnueabi-gcc -DHAVE_CONFIG_H -I. -I../..   -isystem/pardus-arm/usr/include  -march=armv7-a -mtune=cortex-a8 -mfpu=neon -mfloat-abi=softfp -pipe -fexpensive-optimizations -fomit-frame-pointer -frename-registers -O2 -ggdb3 -I/pardus-arm/usr/include -fPIC -D_GNU_SOURCE -W -Wall -Wbad-function-cast -Wcast-align -Wcast-qual -Wmissing-declarations -Wmissing-prototypes -Wpointer-arith -Wreturn-type -Wstrict-prototypes -Wwrite-strings -Winline -Wshadow -c pam_conv_l.c
        arm-pardus-linux-gnueabi-gcc -DHAVE_CONFIG_H -I. -I../..   -isystem/pardus-arm/usr/include  -march=armv7-a -mtune=cortex-a8 -mfpu=neon -mfloat-abi=softfp -pipe -fexpensive-optimizations -fomit-frame-pointer -frename-registers -O2 -ggdb3 -I/pardus-arm/usr/include -fPIC -D_GNU_SOURCE -W -Wall -Wbad-function-cast -Wcast-align -Wcast-qual -Wmissing-declarations -Wmissing-prototypes -Wpointer-arith -Wreturn-type -Wstrict-prototypes -Wwrite-strings -Winline -Wshadow -c pam_conv_y.c
        pam_conv_l.c: In function 'yy_get_next_buffer':
        pam_conv_l.c:1023: warning: comparison between signed and unsigned integer expressions
        pam_conv_l.l: At top level:
        pam_conv_l.c:1122: warning: 'yyunput' defined but not used
        pam_conv_l.c:1163: warning: 'input' defined but not used
        /bin/sh ../../libtool --tag=CC   --mode=link arm-pardus-linux-gnueabi-gcc  -march=armv7-a -mtune=cortex-a8 -mfpu=neon -mfloat-abi=softfp -pipe -fexpensive-optimizations -fomit-frame-pointer -frename-registers -O2 -ggdb3 -I/pardus-arm/usr/include -fPIC -D_GNU_SOURCE -W -Wall -Wbad-function-cast -Wcast-align -Wcast-qual -Wmissing-declarations -Wmissing-prototypes -Wpointer-arith -Wreturn-type -Wstrict-prototypes -Wwrite-strings -Winline -Wshadow  -Wl,-O1 -Wl,-z,relro -Wl,--hash-style=gnu -Wl,--as-needed -Wl,--sort-common                   -L/pardus-arm/lib -Wl,-rpath-link,/pardus-arm/lib                   -L/pardus-arm/usr/lib -Wl,-rpath-link,/pardus-arm/usr/lib  -Wl,--as-needed -Wl,-O1 -o pam_conv1 pam_conv_l.o pam_conv_y.o  -lcrypt 
        libtool: link: arm-pardus-linux-gnueabi-gcc -march=armv7-a -mtune=cortex-a8 -mfpu=neon -mfloat-abi=softfp -pipe -fexpensive-optimizations -fomit-frame-pointer -frename-registers -O2 -ggdb3 -I/pardus-arm/usr/include -fPIC -D_GNU_SOURCE -W -Wall -Wbad-function-cast -Wcast-align -Wcast-qual -Wmissing-declarations -Wmissing-prototypes -Wpointer-arith -Wreturn-type -Wstrict-prototypes -Wwrite-strings -Winline -Wshadow -Wl,-O1 -Wl,-z -Wl,relro -Wl,--hash-style=gnu -Wl,--as-needed -Wl,--sort-common -Wl,-rpath-link -Wl,/pardus-arm/lib -Wl,-rpath-link -Wl,/pardus-arm/usr/lib -Wl,--as-needed -Wl,-O1 -o pam_conv1 pam_conv_l.o pam_conv_y.o  -L/pardus-arm/lib -L/pardus-arm/usr/lib -lcrypt
        pam_conv_l.o: In function `yylex':
        /var/cross/sysroots/cortex-a8/var/pisi/pam-1.1.1-28/work/Linux-PAM-1.1.1/conf/pam_conv1/pam_conv_l.c:871: undefined reference to `yywrap'
        collect2: ld returned 1 exit status
        make[4]: *** [pam_conv1] Error 1
        make[4]: Leaving directory `/var/cross/sysroots/cortex-a8/var/pisi/pam-1.1.1-28/work/Linux-PAM-1.1.1/conf/pam_conv1'
        make[3]: *** [all] Error 2
        make[3]: Leaving directory `/var/cross/sysroots/cortex-a8/var/pisi/pam-1.1.1-28/work/Linux-PAM-1.1.1/conf/pam_conv1'
        make[2]: *** [all-recursive] Error 1
        make[2]: Leaving directory `/var/cross/sysroots/cortex-a8/var/pisi/pam-1.1.1-28/work/Linux-PAM-1.1.1/conf'
        make[1]: *** [all-recursive] Error 1
        make[1]: Leaving directory `/var/cross/sysroots/cortex-a8/var/pisi/pam-1.1.1-28/work/Linux-PAM-1.1.1'
        make: *** [all] Error 2
        DEBUG: return value for "make -j4" is 2
        Traceback (most recent call last):
        File "/r/pardus/playground/memre/arm/corp2/system/base/pam/actions.py", line 34, in build
        crosstools.make()
        File "/usr/lib/pardus/pisi/actionsapi/crosstools.py", line 298, in make
        if system('make %(makejobs)s %(parameters)s' % environment):
        File "/usr/lib/pardus/pisi/actionsapi/shelltools.py", line 255, in system
        error(_("Command \"%s\" failed, return value was %d.") % (command, retValue))
        File "/usr/lib/pardus/pisi/actionsapi/__init__.py", line 27, in error
        raise Error(msg)
        pisi.actionsapi.Error: Command "make -j4" failed, return value was 2.
        Action script error caught.
        *** 1 error(s), 0 warning(s)
        Program terminated.
        Please use 'pisi help' for general help.
        $ 


    Şimdi ``pisi/util.py`` içerisindeki ``strip`` i toolchain tarafından oluşturulmuş strip ile değiştirip
    (``util.py`` içerisinde ``run_strip`` fonksiyonundaki ``p = os.popen("strip %s %s" %(flags, f))``
    fonksiyonunu ``p = os.popen("arm-pardus-linux-gnueabi-strip %s %s" %(flags, f))`` ile değiştiriyoruz)
    ``flex`` paketini tekrardan inşa ediyoruz. İnşa öncesinde önceden oluşturduğunuz pisi dosyasını
    bir dizine kaydedin::

        $ mkdir /tmp/strip_magduriyeti -pv && cp *pisi /tmp/strip_magduriyeti/flex_old.pisi
        $ pisi bi pspex.xml

        ...

        make[2]: Leaving directory `/var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/work/flex-2.5.35/tests'
        make[1]: Leaving directory `/var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/work/flex-2.5.35'
        DEBUG: return value for "make DESTDIR=/var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/install install" is 0
        DEBUG: return value for "install -m0644 "NEWS" /var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/install/usr/share/doc/flex" is 0
        DEBUG: return value for "install -m0644 "README" /var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/install/usr/share/doc/flex" is 0
        DEBUG: /usr/bin/flex [stripped]
        DEBUG: /usr/lib/libfl_pic.a [stripped]
        DEBUG: /usr/lib/libfl.a [stripped]
        ** Building package flex
        Generating files.xml,
        Generating metadata.xml,
        (found old version ./flex-2.5.35-6-1.pisi)
        DEBUG: [('./flex-2.5.35-6-1.pisi', 1)]
        DEBUG: old build number: 1
        There are changes, incrementing build no to 2
        Creating PiSi package ./flex-2.5.35-6-2.pisi.
        DEBUG: return value for "lzma -9 -z install.tar" is 0
        Done.
        All of the files under the install dir (/var/cross/sysroots/cortex-a8/var/pisi/flex-2.5.35-6/install) has been collected by package(s)
        Keeping Build Directory
        *** 0 error(s), 0 warning(s)
        $ pisi it *pisi
        $ cp *pisi /tmp/strip_magduriyeti/flex_new.pisi


    Şimdi ``strip`` komutu sorunsuz çalıştı. ``pam`` ı yeniden inşa ediyoruz::

        $ pisi bi pspec.xml

        ...

        DEBUG: /lib/security/pam_keyinit.so [stripped]
        DEBUG: /lib/security/pam_motd.so [stripped]
        DEBUG: /lib/security/pam_issue.so [stripped]
        DEBUG: Removing special libtool file: /var/cross/sysroots/cortex-a8/var/pisi/pam-1.1.1-28/install/lib/security/pam_namespace.la
        DEBUG: Removing special libtool file: /var/cross/sysroots/cortex-a8/var/pisi/pam-1.1.1-28/install/lib/security/pam_succeed_if.la
        DEBUG: /lib/security/pam_filter/upperLOWER [stripped]
        DEBUG: Removing special libtool file: /var/cross/sysroots/cortex-a8/var/pisi/pam-1.1.1-28/install/usr/lib/libpamc.la
        DEBUG: Removing special libtool file: /var/cross/sysroots/cortex-a8/var/pisi/pam-1.1.1-28/install/usr/lib/libpam_misc.la
        DEBUG: /usr/lib/libpamc.so.0.82.1 [stripped]
        DEBUG: /usr/lib/libpam.so.0.82.2 [stripped]
        DEBUG: /usr/lib/libpam_misc.so.0.82.0 [stripped]
        DEBUG: Removing special libtool file: /var/cross/sysroots/cortex-a8/var/pisi/pam-1.1.1-28/install/usr/lib/libpam.la
        DEBUG: /sbin/pam_timestamp_check [stripped]
        DEBUG: /sbin/pam_tally2 [stripped]
        DEBUG: /sbin/unix_chkpwd [stripped]
        DEBUG: /sbin/unix_update [stripped]
        DEBUG: /sbin/mkhomedir_helper [stripped]
        ** Building package pam
        Generating files.xml,
        Including directory '/var/cross/sysroots/cortex-a8/var/pisi/pam-1.1.1-28/install/etc/security/limits.d'
        Including directory '/var/cross/sysroots/cortex-a8/var/pisi/pam-1.1.1-28/install/etc/security/namespace.d'
        Generating metadata.xml,
        Build number is not available. For repo builds you must enable buildno in pisi.conf.
        Creating PiSi package ./pam-1.1.1-28.pisi.
        DEBUG: return value for "lzma -9 -z install.tar" is 0
        Done.
        All of the files under the install dir (/var/cross/sysroots/cortex-a8/var/pisi/pam-1.1.1-28/install) has been collected by package(s)
        Keeping Build Directory
        *** 0 error(s), 1 warning(s)


    Sorunsuz derlendi. Sorunun sebebinin strip olduğunu aşağıda gösteriyorum::

        $ cd /tmp/strip_magduriyeti
        $ lspisi flex_old.pisi
        /usr/bin/flex
        /usr/bin/lex
        /usr/include/FlexLexer.h
        /usr/lib/libfl.a
        /usr/lib/libfl_pic.a
        /usr/share/doc/flex/NEWS
        /usr/share/doc/flex/README
        /usr/share/info/flex.info
        /usr/share/info/flex.info-1
        /usr/share/info/flex.info-2
        /usr/share/man/man1/flex.1
        $ mkdir old
        $ cd old
        $ unpisi ../flex_old.pisi
        $ ls
        files.xml  metadata.xml  usr
        $ cd usr/lib
        $ ls
        libfl.a  libfl_pic.a
        $ file libfl.a
        libfl.a: current ar archive
        $ ar x libfl.a
        $ ls
        libfl.a  libfl_pic.a  libmain.o  libyywrap.o
        $ file *o
        libmain.o:   ELF 32-bit LSB relocatable, no machine, version 1 (SYSV), not stripped
        libyywrap.o: ELF 32-bit LSB relocatable, ARM, version 1 (SYSV), not stripped
        $ cd ../../../new
        $ unpisi ../flex_new.pisi
        $ cd usr/lib
        $ s
        libfl.a  libfl_pic.a
        $ ar x libfl.a
        $ s
        libfl.a  libfl_pic.a  libmain.o  libyywrap.o
        $ file *o
        libmain.o:   ELF 32-bit LSB relocatable, ARM, version 1 (SYSV), not stripped
        libyywrap.o: ELF 32-bit LSB relocatable, ARM, version 1 (SYSV), not stripped
        $ arm-pardus-linux-gnueabi-strip *o
        $ file *o
        libmain.o:   ELF 32-bit LSB relocatable, ARM, version 1 (SYSV), stripped
        libyywrap.o: ELF 32-bit LSB relocatable, ARM, version 1 (SYSV), stripped
        $ strip libmain.o
        strip: Unable to recognise the format of the input file `libmain.o'
        $ file *o
        libmain.o:   ELF 32-bit LSB relocatable, ARM, version 1 (SYSV), stripped
        libyywrap.o: ELF 32-bit LSB relocatable, ARM, version 1 (SYSV), stripped
        $ strip libfl.a
        strip: Unable to recognise the format of the input file `libfl.a(libyywrap.o)'
        $ ar x libfl.a
        $ ls
        libfl.a  libfl_pic.a  libmain.o  libyywrap.o
        $ file *o
        libmain.o:   ELF 32-bit LSB relocatable, no machine, version 1 (SYSV), stripped
        libyywrap.o: ELF 32-bit LSB relocatable, ARM, version 1 (SYSV), not stripped


    Sorunu tespit etmek oldukça uzun vaktimizi aldı. Strip'in sadece "strip edemedim
    haberin olsun" tarzı bir mesaj yazıp geçiyor diye düşünürken, statik kitaplıkların
    **en başındaki** objeyi bozduğunu anlamamıştık. Statik kitaplığı kullanan
    diğer uygulamaların, arşivin diğer objelerini kullandıklarında sorun çıkarmaması
    sorunu anlamamızı oldukça zorlaştırmıştı. Neyse ki çözdük.

    Sorunun sebeplerinden birisi, pisi içerisine strip komutunun direkt verilmesi,
    diğeri strip işlemini pisi nin nasıl yaptığını kontrol etmemiş olmamız. Ayrıca
    hala hacky yöntemlerle sorunu çözmekteyiz (``chconf`` scripti).

Bundan sonra yapılacaklar
-------------------------
 - paket yapın :)
 - (x86|x86_64) paketlerde yapılacak değişiklikler konusunda kararlar için geliştirici 
   listesine mail atılacak vsvs. (mesa ve python paketlerinden örnek ver)
 - toolchain paketlenecek ve dokümante edilecek, şimdilik tarball ver
 - bu belgenin ayrıntıları da yazılacak
 - crosstools.py gidiyor, yerine actionsapi değişiklikleri geliyor.
 - var olan pisi yi forklayacağım sanırım, emin değilim
 - enlightenment icin managerlar yazilmasi, tam planlanan bir sey degil

TODO
----
 - audit portulmalı mı?

Kaynaklar
---------
 .. [#] http://www.arm.com/
        http://en.wikipedia.org/wiki/ARM_architecture

 .. [#] http://www.arm.com/products/processors/cortex-a/index.php
        http://www.embedinfo.com/en/ARM_Cortex-list.asp?id=15

 .. [#] http://www.arm.com/products/processors/cortex-a/cortex-a8.php?tab=Why+Cortex-A8

 .. [#] http://en.wikipedia.org/wiki/Omap

 .. [#] http://www.macworld.com/article/145998/2010/01/apple_a4.html?lsrc=rss_main
        http://en.wikipedia.org/wiki/Apple_A4

 .. [#] http://en.wikipedia.org/wiki/Snapdragon_(processor)

 .. [#] http://beagleboard.org/

 .. [#] İsmail YK dan geliyor, ABV: http://www.youtube.com/watch?v=3DVIdyNTVw0
