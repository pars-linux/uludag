===================================
reStructuredText Kullanma Kılavuzu
===================================








:Yazarlar:
    Anıl Özbek (maidis)

..  belgeye katkı yaptıktan sonra bilgilerinizi yazmayı unutmayın. -maidis

:Sürüm: 0.1 (2010.02.08) Pardus belgelendirme çalışmaları için oluşturulmuş ilk sürüm

..      yeni sürümleri alt alta yazarak yaptığınız değişikleri ve eklemeleri belirtin
.. Ör:  0.2 (2010.03.04) Hede höde bölümü eklendi, Satıriçi İşaretleme bölümü elden geçirildi -maidis

:Telif Hakkı: GNU FDL





Giriş
------
reStructuredText okuması kolay ve ne görürsen onu alırsın tipinde bir düz metin işaretleme sözdizimi ve ayrıştırıcı sistemidir. Satıriçi kaynak kod belgelendirmesinde, hızlıca inşa edilmek istenen internet sitelerinde ve bağımsız belgelendirmelerde kullanışlı bir araçtır. reStructuredText özel uygulama alanlarında kullanılabilecek esneklikte tasarlanmıştır. reStructuredText ayrıştırıcısı Docutils'in bir parçasıdır.


reStructuredText Kullanma Kılavuzu Hakkında
-------------------------------------------
Bu kılavuz reStructuredText'in (reST) konsepti ve sözdizimi hakkında kısa bir tanıtımdır. Kılavuzun amacı belge hazırlamak isteyenlerin verimli bir şekilde yazabilmesi için ihtiyaç duyduğu bilgileri sunmaktır. reStructuredText kullanımının basit olması için tasarlandığından kısa sürüde öğrenebilirsiniz. Gelişmiş konular ve detaylı bilgiler için Kaynaklar_ bölümünde belirtilen belgelerden faydalanabilirsiniz.


Pardus Belgelendirme Çalışmalarında reStructuredText
----------------------------------------------------
Pardus geliştiricileri ve katkıcılarının yararlanabileceği belgeleri bir araya toplamak ve eksikliği hissedilen belgelerin yazımının daha düzenli bir şekilde yürümesi için başlatılan 7 Şubat 2010 tarihli yeni belgelendirme çalışmasında standart dosya biçimi olarak ReStructuredText'nin kullanılacağı duyuruldu.

LaTeX gibi yetenekli, ancak çok daha rahat yazılan ve okunan bir teknoloji olması; HTML, LaTeX, PDF vb. bir seri dönüştürücüsünün bulunması ve Python PEP vb. yaygın uygulamaların belgelendirme çalışmalarında kullanılması dolayısıyla Pardus belgelendirme çalışmalarında ReStructuredText'in kullanılmasına karar verilmiştir.

Belgelendirme çalışması hakkında detaylı bilgiyi Pardus Geliştirici Listesinde'ki `Belge Açılımı <http://lists.pardus.org.tr/gelistirici/2010-February/023184.html>`_ başlıklı ileti dizisinden öğrenebilir, yazılması düşünülen belgeler hakkında bilgi edinmek içinse `Yapılacaklar Listesini <http://svn.pardus.org.tr/uludag/trunk/doc/TODO>`_ okuyabilirsiniz.


Satıriçi İşaretleme
-------------------
Satıriçi işaretleme kelime ve kelime dizilerini biçimlendirmeye (örneğin kalın veya italik olarak gösterilmeleri için) ve onlara ek (ağ bağlantıları vermek gibi...) özellikler katmaya yaramaktadır.

================================  ================================  ========================================================
Düz Metin                         Görünüş                           Notlar
--------------------------------  --------------------------------  --------------------------------------------------------
\*vurgulama*                      *vurgulama*                       İtalik olarak gösterilir.
--------------------------------  --------------------------------  --------------------------------------------------------
\**önemli vurgulama**             **önemli vurgulama**              Kalın gösterilir.
--------------------------------  --------------------------------  --------------------------------------------------------
\`yorumlanacak metin`             (bkz: sağ taraftaki not)          Yorumlanacak metinin gösterimi ve anlamı birlikte kullanııldığı uygulamaya bağlıdır.
--------------------------------  --------------------------------  --------------------------------------------------------
\``komut gösterimi``              ``komut gösterimi``               Eşaralıklı metin biçiminde gösterilir. Boşluklar korunur fakat satır atlamalar korunmaz.
================================  ================================  ========================================================


Kaçış İşareti
-------------
reStructuredText sola eğik çizgi ("\\") kullanarak işaretleme için kullanılan özel karakterlerin normal olarak da kullanılmasına imkan verir, bir bakıma bize bu özellikten kaçış yolu sunar. Yani normal bir sola eğik çizgi istiyorsanız yapmanız gereken tek şey ("\\\\") ifadesini kullanmak. Örneğin:

========================================    ========================================
Düz Metin                                   Görünüş
----------------------------------------    ----------------------------------------
"\\" \``ile`` \*kaçış*                      "\" ``ile`` *kaçış*
----------------------------------------    ----------------------------------------
"\\\\" \\``ile`` \\*kaçış*                  "\\" \``ile`` \*kaçış*
========================================    ========================================


Bölüm Yapısı
------------
::

    ======
    Başlık
    ======
    Altbaşlık
    ---------

Başlıklar altı çizili (veya hem altı hem de üstü çizili) olarak belirtilirler. Çizgiler en az başlığın genişliğinde olmalıdır. Örneğin bunlar aşağıdaki gibi görünür:

.. Bu bölümün içeriği tablo içinde gösterilebilirse iyi olur. Kendi sitesinde öyle ama henüz çözemedim nasıl. En azında şimdilik satır atlamadan hizalanması için bir yol bulursak iyi olur. -maidis

.. Hıım nasıl yapıldığını anladım sanırım ama düz metinin okunmasını biraz zorlaştırır gibi, diğerlerinde deneyeyim olursa buna da bakarım. -maidis

======
Başlık
======
Altbaşlık
---------
Başlıklar altı çizili (veya hem altı hem de üstü çizili) olarak belirtilirler. Çizgiler en az başlığın genişliğinde olmalıdır. Örneğin bunlar yukarıdakilerden oluşturuldu.


Madde İmli Listeler
-------------------
+---------------------------------------+---------------------------------------+
|Düz Metin                              | Görünüş                               |
+=======================================+=======================================+
|Madde imli liste örnekleri:            | Madde imli liste örnekleri:           |
|                                       |                                       |
|\- Bu birinci                          | - Bu birinci                          |
|                                       |                                       |
|\- Bu da ikinci                        | - Bu da ikinci                        |
|                                       |                                       |
|\* Madde imleri "-", "*" veya "+"      | * Madde imleri "-", "*" veya "+"      |
|\  olabilir. Devam eden metinlerin     |   olabilir. Devam eden metinlerin     |
|\  hizalandırılması gerekmektedir.     |   hizalandırılması gerekmektedir.     |
+---------------------------------------+---------------------------------------+

.. Tablo çizmek kolay değilmiş, artık daha az tablo, daha çok kelime. -maidis

Listelere başlamadan önce ve listeleri bitirdikten sonra en azından tek bir boş satır bırakmanız gerekmektedir.


Numaralandırılmış Listeler
--------------------------
+-----------------------------------------+---------------------------------------+
|Düz Metin                                | Görünüş                               |
+=========================================+=======================================+
|Örnek bir liste:                         | Örnek bir liste:                      |
|                                         |                                       |
|\3. Bu birinci                           | 3. Bu birinci                         |
|                                         |                                       |
|\4. Bu da ikinci                         | 4. Bu da ikinci                       |
|                                         |                                       |
|\5. Liste elemanları sayılara veya       | 5. Liste elemanları sayılara veya     |
|\   harflere göre numaralandırılabilir.  |    harflere göre numaralandırılabilir.|
|\   Numaralandırma ardışık olarak        |    Numaralandırma ardışık olarak      |
|\   yapılır fakat liste herhangi         |    yapılır fakat liste herhangi       |
|\   bir değerden başlayabilir.           |    bir değerden başlayabilir.         |
|                                         |                                       |
|\#. Bu otomatik numaralandırılacaktır.   | #. Bu otomatik numaralandırılacaktır. |
+-----------------------------------------+---------------------------------------+


Tanım Listeleri
---------------
nedir bu
  Tanım listeleri bir ifadeyi bir tanımla birleştirmek için kullanılır.

nasıl kullanılır
  İfade tek satırlık kelime veya kelime grubu olabilir. Tanım ise bir veya birden fazla paragraftan mürekkep olabilir.

  İfade ve tanım arasında satır atlama mümkün değildir.


Alan Listeleri
--------------
::

    :Yazarlar:
        Anıl Özbek,
        Hede Hedeoğlu
    :Sürüm: 1.0 (2010.02.09)
    :Telif Hakkı: GNU FDL

:Yazarlar:
    Anıl Özbek,
    Hede Hedeoğlu
:Sürüm: 1.0 (2010.02.09)
:Telif Hakkı: GNU FDL

Alan listeleri ayrıca iki sütunlu tablolar oluşturmak için de kullanılabilir.


Seçenek Listeleri
-----------------
.. Pek kulanışlı değil gibi ya da ben tam kullanamadım. Örneğin PiSi'nin seçeneklerini listeletemedim. Hem iki kullanım biçimi olduğundan hem de çizgilerle ("-") başlamadıkları için. -maidis

--all                  . ile başlayan girdileri saklamaz
--almost-all           örtük . ve .. değerlerini göstermez
--author               -l ile her dosyanın yazarını gösterir
--escape               grafik olmayan karakterleri sekizlik değerlerle gösterir

Seçenek ve açıklaması arasında en azından iki boşluk olması gerekmektedir.


Tablolar
--------
reStructuredText'de tablo oluşturmak için iki sözdizimi vardır. Izgara tipi tablolar tam bir çözüm sunmasına rağmen oluşturulmaları biraz sıkıcıdır. Basit tipli tablolar ise oluşturulması kolay olmasına rağmen özellikleri sınırlıdır.

Izgara tablo örneği:
::

    +------------+------------+-----------+
    | Başlık 1   | Başlık 2   | Başlık 3  |
    +============+============+===========+
    | eleman 1   | hede 2     | hede 3    |
    +------------+------------+-----------+
    | eleman 2   | İki sütünlük bir eleman|
    +------------+------------+-----------+
    | eleman 3   | Çok satırlı| - madde 1 |
    +------------+ bir eleman | - madde 2 |
    | eleman 4   |            | - madde 3 |
    +------------+------------+-----------+

+------------+------------+-----------+
| Başlık 1   | Başlık 2   | Başlık 3  |
+============+============+===========+
| eleman 1   | hede 2     | hede 3    |
+------------+------------+-----------+
| eleman 2   | İki sütünlük bir eleman|
+------------+------------+-----------+
| eleman 3   | Çok satırlı| - madde 1 |
+------------+ bir eleman | - madde 2 |
| eleman 4   |            | - madde 3 |
+------------+------------+-----------+

Basit tablo örneği:
::

    =====  =====  ========
      Girişler      Çıktı
    ------------  --------
      A      B    A veya B
    =====  =====  ========
      0      0       0
      1      0       1
      0      1       1
      1      1       1
    =====  =====  ========

=====  =====  ========
  Girişler      Çıktı
------------  --------
  A      B    A veya B
=====  =====  ========
  0      0       0
  1      0       1
  0      1       1
  1      1       1
=====  =====  ========


Dipnotlar
---------
::

    Dipnot referanslar şu şekilde [1]_ verilebilir.

    Bu [#]_ ve şu [#]_ şekilde otomatik numaralandırılmış dipnotlar oluşturmak mümkündür.

    Otomatik numaralandırılmış dipnotların sıraları değiştirilebilir, [#besinci]_ ve [#dorduncu]_ dipnotlar bunu örneklemektedir.

    .. [1] Merhaba dipnotu.
    .. [#] Bu ikinci dipnottur.
    .. [#] Bu üçüncü dipnottur.
    .. [#dorduncu] dorduncu_ olarak da bilinir.
    .. [#besinci] besinci_ olarak da bilinir.

Dipnot referanslar şu şekilde [1]_ verilebilir.

Bu [#]_ ve şu [#]_ şekilde otomatik numaralandırılmış dipnotlar oluşturmak mümkündür.

Otomatik numaralandırılmış dipnotların sıraları değiştirilebilir, [#besinci]_ ve [#dorduncu]_ dipnotlar bunu örneklemektedir.

.. [1] Merhaba dipnotu.
.. [#] Bu ikinci dipnottur.
.. [#] Bu üçüncü dipnottur.
.. [#dorduncu] dorduncu_ olarak da bilinir.
.. [#besinci] besinci_ olarak da bilinir.


Harici Ağ Bağlantıları
----------------------
::

    Belgelerinizde istediğiniz internet sayfalarına bağlantı verebilirsiniz, örneğin: Pardus_.

    .. _Pardus: http://pardus.org.tr

Belgelerinizde istediğiniz internet sayfalarına bağlantı verebilirsiniz, örneğin Pardus_.

.. _Pardus: http://pardus.org.tr

::

    reStructuredText belgesinin okunurluğunu bir parça azaltsa da bağlantılar aynı satır üzerinden de verilebilir, örneğin: `Pardus <http://pardus.org.tr>`_.

reStructuredText belgesinin okunurluğunu bir parça azaltsa da bağlantılar aynı satır üzerinden de verilebilir, örneğin: `Pardus <http://pardus.org.tr>`_.


Dahili Ağ Bağlantıları
----------------------
::

    Dahili çapraz başvuru bağlantıları da oluşturabilirsiniz, örneğin hede_.

    .. _hede:

    Bu bir çapraz başvuru bağlantı hedefidir.

Dahili çapraz başvuru bağlantıları da oluşturabilirsiniz, örneğin hede_.

.. _hede:

Bu bir çapraz başvuru bağlantı hedefidir.


Dolaylı Ağ Bağlantıları
-----------------------
::

    Python_ benim `en sevdiğim dildir`__.

    .. _Python: http://www.python.org

    __ Python_

Python_ benim `en sevdiğim dildir`__.

.. _Python: http://www.python.org

__ Python_

.. C++ yazdığınızda kabul etmiyor. -maidis


Örtülü Ağ Bağlantıları
----------------------
Bölüm başlıkları, dipnotlar, alıntılar otomatik olarak ağ bağlantısı oluştururlar. Başlık metni veya dipnot/alıntı etiketi ağ bağlantısı ismi olarak kullanılır.

::

    Belgeyi bir daha okumak için `Giriş`_ bölümüne gidebilirsiniz. Kelime gruplarında oluşan örnek bir başlığa ise şu şekilde gidebilirsiniz: `Dolaylı Ağ Bağlantıları`_.

Belgeyi bir daha okumak için `Giriş`_ bölümüne gidebilirsiniz. Kelime gruplarında oluşan örnek bir başlığa ise şu şekilde gidebilirsiniz: `Dolaylı Ağ Bağlantıları`_.

.. HTML'de sorun olmuyor ama PDF'ler de sorunlu: _Giriş, aslında tek kelime olduğu için tırnaklara gerek olmaması lazım gibi. -maidis

Direktifler
-----------
Direktifler yeni yapıları yeni sözdizim kuralları eklemeye gerek kalmadan desteklemek için genel amaçlı genişleme mekanizmasıdır. Tüm standart direktiflerin açıklamaları için `reStructuredText Directives <http://docutils.sourceforge.net/docs/ref/rst/directives.html>`_'e bakabilirsiniz.

::

    Örneğin bir kedi gördüm sanki:
    .. image:: application-pisi.png

Örneğin bir kedi gördüm sanki:

.. image:: application-pisi.png

Direktifler satıriçi olarak kullanılarak resimlerin ve diğer yapıların metinle daha bütünleşik olması sağlanabilir.

::

    Örneğin bir |kedi| gördüm sanki.
    .. |kedi| image:: application-pisi.png

Örneğin bir |kedi| gördüm sanki.

.. |kedi| image:: application-pisi.png


Yorumlar
--------
Belgelerinizi yazarken hem çalışma arkadaşlarınızın hem de ileride kendinizin neyi niçin ve nasıl yaptığınızı daha kolay anlaması için küçük notlar ve yorumlar yazabilirsiniz. Örneğin:

::

    .. Yorum yorum yorulmak :)

.. Yorum yorum yorulmak :)


Paragraflar
-----------
reStructuredText'in en temel parçalarından biri paragraflardır. Paragraflar bir veya daha fazla boşlukla ayrılan cümlelerden oluşur. Bir paragrafa ait tüm satırlar soldan hizalı olmalıdır.

::

    Örneğin bu kendi halinde olan birinci paragrafımızdır. Gördüğünüz gibi birden fazla cümleden oluşmaktadır.

    Bu da ikinci paragrafımızdır. Birincisiyle arasında yalnızca tek bir boşluk vardır.

Örneğin bu kendi halinde olan birinci paragrafımızdır. Gördüğünüz gibi birden fazla cümleden oluşmaktadır.

Bu da ikinci paragrafımızdır. Birincisiyle arasında yalnızca tek bir boşluk vardır.


Kod parçacıkları
----------------
Değişmesi istenmeyen kod parçacıkları \:: ile birlikte yazılabilir. Yazılmak istenen kod parçacıkları girintilenerek yazının geri kalanından ayrıştırılabilir.

::

    Aşağıdaki örnek actions.py dosyasını inceleyebilirsiniz:
    ::

        #!/usr/bin/python
        # -*- coding: utf-8 -*-
        #
        # Licensed under the GNU General Public License, version 2.
        # See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

        from pisi.actionsapi import cmaketools
        from pisi.actionsapi import pisitools
        from pisi.actionsapi import get

        def setup():
            cmaketools.configure("-DCMAKE_BUILD_TYPE=release", installPrefix="/usr/kde/4")

        def build():
            cmaketools.make()

        def install():
            cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
            pisitools.dodoc("ChangeLog", "COPYING", "README", "TODO")


Aşağıdaki örnek actions.py dosyasını inceleyebilirsiniz:
::

    #!/usr/bin/python
    # -*- coding: utf-8 -*-
    #
    # Licensed under the GNU General Public License, version 2.
    # See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

    from pisi.actionsapi import cmaketools
    from pisi.actionsapi import pisitools
    from pisi.actionsapi import get

    def setup():
        cmaketools.configure("-DCMAKE_BUILD_TYPE=release", installPrefix="/usr/kde/4")

    def build():
        cmaketools.make()

    def install():
        cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
        pisitools.dodoc("ChangeLog", "COPYING", "README", "TODO")




Kaynaklar
---------
- `reStructuredText <http://docutils.sourceforge.net/rst.html>`_
- `Quick reStructuredText <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_
- `reStructuredText Howto <http://developer.pardus.org.tr/howto/howto-rst.html>`_
- `Markdown ve reStructuredText: Hafif Siklet İşaretleme Dilleri <http://www.ustunozgur.com/2009/03/hafif-siklet-isaretleme-dilleri.html>`_
- `Sphinx: Otomatik Belge Oluşturma Yazılımı ve İlk PDF <http://www.istihza.com/blog/tag/otomatik-belge-olusturma/>`_


..
    bu belgeyi diğer biçimlere çevirmek için:
    HTML: rst2html.py reStructuredText.rst > reStructuredText.html
    PDF : rst2pdf reStructuredText.rst
