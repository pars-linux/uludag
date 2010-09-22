Hata ve Özellik Bildirimleri
============================

Bugzilla Pardus Linux Dağıtım projesinde kullanılan hata izleme aracıdır. Bu araç ile kullanıcılar ve geliştiriciler tarafından hatalar ile ilgili geri dönüşler sağlanmakta ve Pardus Linux Dağıtımının gelişmesi ve iyileşmesi amaçlanmaktadır.

yeni raporlanan hatalarda, eksik veya yanlış bilgiler bulunabilmektedir. Bu durum zaman kaybına neden olmaktadır. Raporlayan kişi eksik veya hatalı olan raporu yazarak zaman kaybederken, geliştirici hatayı anlamak ve çözmek için daha fazla vakit kaybetmekte ve çoğunlukla eksik ve hatalı raporlanma nedeniyle hata kapatılmakta veya ilgilenilmemektedir.

Bu sayfa etkili ve kaliteli hata raporlama adımlarını anlatmaktadır

Hata raporlamaya ihtiyacım var mı?
----------------------------------

Bugzilla üzerinde hatanın raporlandığını görmedikçe, sürüm notlarında açıklanan, formel belgelerde dile getirilen, geliştiricinin e-posta listesinde tartıştığı, derleme çiftliğinde kırık bağımlılğı bulunan paketler veya yazılımların hataları bugzillla üzerinden raporlanmalıdır. Herkesin aynı hata ile karşılaştığını ve bildiğini düşünerek hata raporlamaktan vazgeçilmemelidir. Hatanın e-posta listelerininveya forumların kirliliği içerisinde kaybolmaması ve izlenebilir hale gelmesi için mutlaka hata raporlanmalıdır.

Hata Takip Döngüsü
------------------

Pardus Linux Dağıtımının hata takip döngüsü ile ilgili açıklamalar için bkz. bug_cycle.rst.
..(bug cycle hata ayıklayıcılar ile tekrar yapılacak)

Hata raporlamaya başlarken
--------------------------

İlk yapmanız gereken bugs.pardus.org.tr üzerindne bir hesap edinmektir. Bu çok hızlı bir süreçtir, hesap almak için terreddüt etmenize gerek yoktur. `Detaylı bilgi için <https://bugs.pardus.org.tr/docs/en/html/myaccount.html>_`.

Hata Takip Sistemini Anlamak
----------------------------

Geliştiricilerin hata raporlamadan beklentileri doğrultusunda hata raporlamanız hatanızın açıklanma yöntemini iyileştirecek ve geliştiricilerin hatanızı daha ilgili ve çözmeye istekli yaklaşmalarını sağlayacaktır. Eğer daha önce hiç bugzilla'yı kullanmadıysanız aşağıda bulunan bağlantılar size yardımcı olacaktır:

    * https://bugzilla.mozilla.org/page.cgi?id=etiquette.html
    * `Etkili hata raporlama effective_bug_reporting.rst`_

Eğer bir uygulama çok fazla kullanılıyor ise, kullanıcıların bu uygulamaya daha çok hata ve iyileştirme girmesi mümkündür. Fakat bu o uygulamanın hata çöplüğü olduğunu göstermez.

Aynısı olan Hataları Arama
--------------------------

Bugzilla'ya hata raporlamadan önce hatanın daha önce raporlanmamış olduğuna emin olmalısınız. En kolay yolu anahtar kelime ile hata aramadır. Yada gelişmiş aramayı kullanmaktır.

Ben de bu hata ile karşılaşıyorum yorumu yapmak genellikle iyi bir yöntem değildir. Fakat hatayı daha kolay tekrarlayabilecek yöntemler açıklamak, daha ayrıntılı hata çıktıları ve log dosyaları göndermek iyi bir yöntemdir.

Daha ayrıntılı bilgi için finding_duplicates.rst.

İşe yarar bilgi toplama
-----------------------

Ayrıntılı bilgi için `Hata Tipine Göre Bilgi Toplama`_ bölümüne bakınız.

Aldığınız hataya yönelik olarak tüm kullanıcılar için /var/log/messages ve ~/.xsession-errors (masaüstü kullanıcıları için) dosyalarını kontrol etmelisiniz. Bunun yanı sıra /var/log dizini altında programlara özgü log dosyaları da oluşmaktadır, aldığınız hata doğrultusunda bu dosyaları da inceleyebilir ve gerekli olduğunu düşündüğünüz durumlarda hataya ekleyebilirsiniz.

Hata Raporlamaya Başlama
------------------------

Aldığınız hatayı `buradan <http://bugs.pardus.org.tr/enter_bug.cgi>_` girebilirsiniz. 

`Hata raporlama kılavuzunu <http://bugs.pardus.org.tr/page.cgi?id=bug-writing.html>_` dikkatli bir şekilde okuduktan sonra tüm istenen bilgileri girip hatanızı raporlayabilirsiniz.

Hata raporlarken gerekli olan tüm bilgileri vermeye ve açık bir dil kullanmaya çalışın. "Bu hata derhal çözülmeli!", "Bu hata tahammül edilemez bir hata!" gibi açıklamalarda bulunulmamalı, geliştiricilerin bu hatalardan etkilendiğini ve çabuk çözmeye çalıştığı düşünülmemelidir.

Doğru Bileşeni Bulmak
---------------------

Hata raporlarken doğru ürün ve bileşen ve sürümü seçmek çok önemlidir. Bunu yaparak hatanın etkilendiği geliştiriciyi direkt olarak bulmuş olursunuz ve böylece hatanız daha çabuk çözümlenmek için hız almış olur. Eğer hatanızı yanlış bir bileşene atarsanız, daha sonra geliştiriciler veya hata ayıklayıcılar tarafından doğru bileşene atanana kadar hatanız zaman kaybetmiş olur.

Ayrıntılı bilgi için correct_component.rst

Hata Raporlandıktan Sonra
-------------------------

    * Geliştiriciler genelde hata raporuna, hatanız işleme alınmıştır gibi bir onay yorumu göndermezler, hatanıza yorum yapılmadığı süre boyunce sabırlşı olmalı ve takip etmeyi sürdürmelisiniz.

    * Hata raporladıktan sonra, diğer kullanıcılar tarafından yorum alabilir, veya geliştiricinin hata durumunu ve çözümünü değiştirdiğini fark edebilirsiniz. Pardus Hata sisteminde kullanılan farklı durum ve çözümleri görebilmek için bkz. bug_cycle.rst

    * Hatanızın temel probleminizden uzaklaşacak şekilde değişmesine izin vermeyin, yorumlarda devam eden hatadan bağımsız tartışmalar kafa karıştırıcı ve takip etmeyi zorlaştırıcı olmaktadır. Eğer bu süre içerisinde uygulamada başka bir problem ile karşılaştıysanız veya raporladığınız hatanın çözüldüğünü ve başka bir hatanın oluştuğunu fark ettiyseniz, yeni bir hata açmalısınız.

    * Eğer raporladığınız hata güncellenmeyen bir sürüme ait ise (EOL) hata ayıklayıcılar yeni sürümde bu hatanın tekrarlanıp tekrarlanmadığını kontrol edecek ve eğer tekrarlanmıyor ise bu hatayı kapatacaktır. 

Hata Tipine Göre Bilgi Toplama
==============================

Kurulum hataları için
----------------------
    * Kurulan sistemdeki /var/log/yali.log dosyasını hata raporuna ekleyin.
    * Bölümleme ile ilgili hatalarda disk bölümleme bilgisini rapora ekleyin. Bunun için "fdisk - l" komutunu kullanabilirsiniz. 

YALI log dosyasını alabilmeniz için:

* CTRL+ALT+F1 tuşlarına aynı anda basınız.(Bu komut ile sitem konsoluna geçmiş olmalısınız.)
* Bilgisayarınıza usb bellek takınız.
* Usb belleğinizi bilgisayarınıza bağlayınız:.

::

    mount /dev/<your_usb_stick_partition> /mnt/flash

* Yalı için gerekli olan çıktıları /mnt/flash dizinine kopyalayınız.·

::

    cp <output> /mnt/flash

* Bağı manuel bir şekilde kaldırınız.
::

    umount /dev/<your_usb_stick_partition>

Program Çökmesi:
----------------

Eğer bir programın çökmesi problemi ile karşılaştıysanız, hata raporunuza stack trace bilgisini eklemelisiniz. Program çökmeleri genelde tekrarlanması ve çözülmesi zor olan problemlerdir. Bu yüzden olabildiğince bilgi vermek çok önemlidir.

Eğer test deposu kullanıyorsanız, ilgili sürüme ait http://packages.pardus.org.tr/pardus-x-debug/pisi-index.xml.bz2 debug deposunu ekleyip, hata aldığınız uygulamanın debug paketini kurabilir ve stack trace'de kullanışlı bir çok debug sembolünü yakalayabilirsiniz: bkz stack_trace.rst

Donma ve panikler:
---------------------

Eğer tüm makine kilitlenmiş ise veya ekran siyah bir durumda bulunmakta ise:
    * Kernel'in askıda kalıp kalmadığından emin olmak için, CapsLoc, NumLock tuşlarını aktif hale getirdiğinizde ışıklarının yanıp yanmadığını gözlemleyin. Eğer ışıklar hala yanıyor ise birşeyler çalışmay
a devam ediyor demektir.
    * Başlatma ile ilgili sorunları gözlemleyebilmek için splash'ı kapalı olarak çalıştırın. Bunu yapabilmek için açılış sırasında çıkan açılış seçenekleri bölümünden "splah=silent" değişkeni yerine "splash=verbose" değerini girin.
    * Sorunun ekran kartı ile ilgili olabileceği ihtimaline karşı açılış ekranı geldiğinde F4 tuşuna basın ve grafik ekranı Kapalı duruma getirin ve bilgisayarınızı bu şekilde açın, bu şekilde açılabiliy
or ise sorun büyük bir ihtimal ekran kartından kaynaklanmaktadır.
    * Sorunun bulunduğu noktayı daha spesifik olarak algılayabilmek için F5 tuşuna basarak sırası ile ACPI kapalı, Yerel APIC kapalı seçenekleirini de deneyerek başlatabilrirsiniz.
    * Sistemi başlatmaya çalıştığınızda, başlatamıyor iseniz: kamera ile alınan hatayı çekin.


Donanıma Özgü Hatalar
----------------------

Eğer aldığınız hatanın sizde bulunan bir donanımdan kaynaklandığını düşünüyorsanız, hata raporunuza smolt profilinizin bağlantınızı ekleyebilirsiniz. Bunun için konsoldan "smoltGui" yazınız ve açılan pencerede sendProfile butonuna basın ve size profil bağlantınızı gönderecektir.

Donanıma özgü hatalar genellikle ekran kartı, video card, kamera, yazıcı gibi çevresel aygıtlar ile ilgilidir. Bu yüzden özellikle kelime işlemci, hesap makinası gibi uygulamalar donanıma bağlı değildir.

Programlardaki hatalar için:
----------------------------

    * Programı menüden değil konsoldan çalıştırın ve tüm konsol çıktılarını rapora ekleyin. bkz. correct_component.rst

X server hataları için:
------------------------

* Aşağıdaki komutların çıktıları eklenmelidir:

::

    lspci -nn > lspci.txt
    dmesg > dmesg.txt
    lsmod > lsmod.txt

* Eğer bilgisayar veya klavye hala çalışabiliyorsa, X server logları da çok yararlı olacaktır. 

::

    cat /var/log/Xorg.0.log > xserver.txt

* Eğer çalışmıyorlarsa, izlemeniz gereken yol: Bilgisayarınızı yeniden başlatın, vesa modunda açın ve aşağıda bulunan logu alınız:

::

    cat /var/log/Xorg.0.log.old

Bütün çıktılar için, eğer X çökmüş ise, bu çıktıları aşağıdaki prosedürle alabilirsiniz:

* CTRL+ALT+F1 tuşlarına aynı anda basınız.(Bu komut ile sitem konsoluna geçmiş olmalısınız.)
* Bilgisayarınıza usb bellek takınız.
* Bilgisayarınıza usb bellek takınız.

::

    mount /dev/<your_usb_stick_partition> /mnt/flash

* X için gerekli olan çıktıları /mnt/flash dizinine kopyalayınız. 

::

    cp <output> /mnt/flash

* Bağı manuel bir şekilde kaldırınız.
::

    umount /dev/<your_usb_stick_partition>




Birçok durum için COMAR'ın log dosyası yardımcı olabilir.

::

    cat /var/log/comar3/trace.log > comar.txt

network-manager için:
---------------------

Ağ aygıtınızı öğrenmek için:

::

    lspci -nn > lspci.txt

Ethernet'e özel problemler:

::

    ifconfig -a > ifconfig.txt

Wireless'a özel problemler:

::

    iwconfig > iwconfig.txt

disk-manager için:
------------------

::

    fdisk -l > fdisk.txt
    cat /etc/fstab > fstab.txt

service-manager için:
---------------------

::

    service -N > service.txt

boot-manager için:
------------------

::

    cat /boot/grub/grub.conf > grub.txt

firewall-manager için:
----------------------
::

    service -N > service.txt
    iptables > iptables.txt

Kamera/video aygıtları ile ilgili hatalar için:
-----------------------------------------------

Bu komutların çıktıları kamera aygıtını kullanabilecek olan tüm uygulamaları kapattıktan sonra alınmalıdır.

::
    dmesg > dmesg.txt
    cat /var/log/syslog > syslog.txt
    lsusb > lsusb.txt
    test-webcam > webcam.txt

Ses kartı ile ilgili hatalar için:
-----------------------------------

Aşağıdaki komutu root kullanıcısı olarak çalıştırın ve en son olarak çıktıda bulunacak olan WWW linkini not alın:

::

    alsa-info

Kullanıcı onayı ve izinleri ilgili sorunlar:
---------------------------------------------

Eğer audit sunucusu çalışıyor ise aşağıda bulunan komutun çıktısını hata raporuna ekleyebilirsiniz:

::

    tail /var/log/audit/audit.log > audit.txt

Eğer audit sunucusu çalışmıyor ise.

::

    tail /var/log/messages


Firefox ile ilgili hatalar:
---------------------------

* Hatanın firefox'un kendisinden mi yoksa bir eklentisinden mi kaynaklandığını bulabilmek için: (Eğer hata bir eklentiden kaynaklanıyor ise hata özetine mutlaka bu eklentinin ismini ekleyin) 

    * Araçlar -> Eklentiler yolunu takip ederek, aktif olan eklentilerinizi sırası ile kapatarak hatayı tekrarlamayı deneyin. (Her eklenti kapatılması sonrasında firefox yeniden başlatılmalıdır.) 
    * Hiç bir tema ve eklentiyi kullanmadan "firefox -safe-mode" komutunu çalıştırarak firefox'u çalıştırabilirsiniz.
    * Hangi eklenti ve temaların kurulu olduğunu hataya eklemek her zaman bir artı olacaktır.
* Bazı durumlarda sizin daha önce yapmış olduğunuz özelleştirmeler nedeni ile hata alıyor olabilirsiniz, hatayı başka bir kullanıcı yaratarak tekrarlamayı deneyin. 

Firefox çökmeleri için stack_traces.rst.


Openoffice ile ilgili hatalar
-----------------------------

Çökmeler:

* Openoffice uygulamasının açılışnda bir çökme gerşekleşiyor ise bu durum OpenGl ile ilgili bir sorun olabilir. 
    * Bunun için testgl.c dosyanı çalıştırın

        ::

            gcc testgl.c -o testgl -lX11 -lGL
            ./testgl
    * Eğer bu komut da çöküyor ise sorun openoffice'ten kaynaklanmamaktadır.
* Eğer openoffice uygulaması çöktüğünde dialog çıkartıyor ise bunu hata raporuna ek olarak ekleyebilirsiniz.
* Aynı zamanda debug paketini kurarak stack trace alabilirsiniz. bkz stack_traces.rst

    ::

        Örneğin kelime işlemcide bir çökme olduğunda aşağıda bulunan komutlar sırası ile çalıştırılmalıdır:
        vim `which oowriter`
            /opt/OpenOffice.org/lib/ooo-3.2/program/soffice.bin

        gdb /opt/OpenOffice.org/lib/ooo-3.2/program/soffice.bin
        run -writer
        bt

Çıkan backtrace'ı hata raporunuza eklemeli veya yapıştırmalısınız. (-writer openoffice uygulamasına göre değişecektir. -calc, -impress, -math etc)


İyileştirme ve Yeni Özellik istekleri
-------------------------------------

* Yeni özellik isteğinde bulunurken, newfeature ile işaretlemeyi unutmayın. İyileştirmenizi anlatacak derecede objectif bir açıklama yapmaya çalışın.
* Pardus Linux Dağıtımı Projesi bir özgür yazılım projesidir, bu yüzden herhangi bir iyileştirme veya yeni özellik isteğinde bulunmadan önce lütfen forbidden_items.rst sayfasına göz atın.
* Eğer yeni bir özellik girmek istiyorsanız, bu özellik için yeni bir wiki sayfası oluşturun ve kabul edilmesini takip edin. features_policy.rst
* Yeni paket istekleri için Paketler/Yeni Paket ürününe istediğiniz paket ile ilgili bir hata raporlayın.

Grafiksel Kullanıcı Arayüzü ile İlgili Hatalar
----------------------------------------------
Eğer herhangi bir kullanıcı arayüzü ile ilgili hatanız bulunmakta ise, genellikle hata raporuna ekran görüntüsü eklemek en uygun olanıdır. Bu ekran görüntüleri geliştiricinin hatanın hangi bölgede olduğunu daha kolay tespit etmelerini sağlayacaktır. 

* Ekran görüntüsü almak için "Print Screen" butonuna basabilirsiniz veya gimp uygulamasını açıp Dosya -> Yarat -> Ekran Görüntüsü yolunu izleyerek ekran görüntüsü alabilirsiniz.
* Video görüntüsü alabilmek için recordmydesktop paketini kullanabilirsiniz.

