Stack Trace(Backtrace) nedir?
-----------------------------

Program içerisinde kullanılan fonksiyon çağrılarının ulaştıkları noktaların listesine stack trace (backtrace) denilmektedir. gdb gibi çeşitli debug araçları geliştiricilerin çöken programın sorununu bulabilmeleri için stack trace verirler.

Stack Trace neye benzer?
-------------------------

Tipik bir stack trace aşağıdaki gibidir.

::

    [New Thread 8192 (LWP 15167)]

    0x420ae169 in wait4 () from /lib/i686/libc.so.6
    .
    .
    .

Debug sembolleri ile birlikte daha ayrıntılı bir stack trace:

::

    0x000000350a6c577f in *__GI___poll (fds=0xe27460, nfds=9, timeout=-1) at ../sysdeps/unix/sysv/linux/poll.c:83
    83          return INLINE_SYSCALL (poll, 3, CHECK_N (fds, nfds), nfds, timeout);
    .
    .
    .

Çağrılan dosyaların ve fonksiyon çağrılarının listelendiğini görmekteyiz.


Debug sembolleri nedir ve ne işe yararlar?
------------------------------------------

Program debug sembolleri ile birlikte derlendiğinde, ek bilgiler program içeriend eklenmektedir. Bu bilgiler stack trace oluşturularak, kaynak dosyadaki sorunlu satır numarası gibi daha değerli bilgilere erişilebilir. Debug sembolleri olmadan stack trace'e bakarak sorunu anlamanın yolu çok zordur.

Debug paketleri nelerdir, nasıl ulaşabilirim?
---------------------------------------------

Pardus özelleşmiş debug paketlerine de sahiptir. Bu paketler degub sembollerini içeren veriler ile otomatik olarak derlenmektedir. Bu sayede ihtiyaç duyduğunuzda gerekli olan debug bilgisinizi almanıza yarar. Debug etmek istediğininiz uygulamaya uygun versiyona sahip debug paketini kurmanız gerekmeketedir. Debug paketlerini kullanabilmek için öncesinde test deposu kullanmanız gerekmektedir. Eğer test deposu kullanıyorsanız, ilgili sürüme ait http://packages.pardus.org.tr/pardus-x-debug/pisi-index.xml.bz2 debug deposunu ekleyip, hata aldığınız uygulamanın debug paketini kurabilir ve stack trace'de kullanışlı bir çok debug sembolünü yakalayabilirsiniz:


Örnek: Paket ve ilgili versiyona ait debug paketini bulmak:

[test@computer ~] $ pisi info amarok
Yüklü paket:
İsim: amarok, sürüm 2.3.0, yayım 38, inşa 20


Debug paketinini aynı sürümünü bulabilmek için, örneğin sürüm Pardus 2009 sürümü ise http://packages.pardus.org.tr/pardus-2009-debug/ bağlantısına girip amarok ile aynı sürüme ait amarok-dbginfo paketini bulun ve bu paket uygulamaya uygun olan debug paketi olacaktır.

Her paketin debug paketi bulunmaktadır pisi komutunu kullanarak çok kolay bir şekilde debug paketini kurabilirsiniz.

Örneğin amarok için:

sudo pisi it http://packages.pardus.org.tr/pardus-2009-debug/amarok-dbginfo-2.3.0.90-40-16.pisi


GDB kullanarak stack trace üretmek:
------------------------------------

GDB'yi başlatmak için aşağıda bulunan komutu çalıştırınız. 

::

    gdb <program-adı>

<program-adı> çöken programın adıdır. (örneğin: amarok).

GDB komut satırına daha sonra aşağıda bulunan komutu yazın.

::

    run

Eğer herhangi bir değişken vermeniz gerekiyor ise aşağıda bulunduğu şekilde yazmalısınız

::

    run --argument

Program çalıştıktan sonra, programın çökmesini gerektirecek senaryoyu uygulayın ve çökme gerçekleştikten sonra gdb komutunu çalıştırdığınız terminale dönün. gdb komut satırı görünüyor olmalıdır, eğer görünmüyor ise CONTROL+C tuşlarına aynı anda basın ve aşağıda bulunan komutu yazın:
::

    thread apply all bt full

Eğer bu işlemler işe yaramaz ise, komut satırına sadece "bt" yazın. 

Bu komutlar sonrasında bir çıktı üretilecektir bu çıktı stack trace'dir. Bu çıktıyı bir text dosyasına kopyalayın ve gdb'den çıkın.

