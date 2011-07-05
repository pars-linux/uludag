Test için Gerekli Kısa Bilgiler
===============================
**Author:** Semen Cirit

#. Tüm testler Kurumsal2 pardus üzerinde denenecektir
#. Tüm Pardus test sütreci [1] belgesinde 
#. Tüm bulunan hatalar [2] belgesine uygun şekilde raporlanmalıdır.
#. Tüm uygulamaların testlerinde, öncelikli olarak türkçe çeviri eksiklikleri, türkçe sıralama ve karakter görüntüleme problemleri ile ilgilenilecektir.
#. Teknoloji test aşamalarına [3] belgesinden ulaşılabilir. Eksik olan kısımlar staj süresince eklenilmeli ve eski olan kısımlar değiştirilmelidir. Değişiklikler [4] linkinde bulunan ilgili dosyalar üzerinden yapılabilir
#. Paket test aşamalarına [5] linkinden ulaşılabilir. Eksik olan kısımlar staj süresince eklenilmeli ve eski olan kısımlar değiştirilmelidir. Değişiklikler [4] linkinde bulunan ilgili dosyalar üzerinden yapılabilir.
#. Test edilecek paketlerin hangileri olduğunu ve bunların hangi bileşende olduklarını aşağıda bulunan komutları kullanarak bulabilirsiniz (bileşen isimleri test aşaması belge isimleridir)::

    pisi sr <paket adı>
    pisi info <paket adı>

Test edilecek Tenolojiler
-------------------------

#. Tasma (Test aşamalarının tamamı bulunmamaktadır)
    #. Güvenlik duvarı yöneticisi
    #. Açılış yöneticisi
    #. Disk yöneticisi
    #. Ekran ayarları (Test aşaması yok)
    #. Servis yöneticisi
    #. Kullanıcı yöneticisi
    #. Tasmada bulunan diğer bölümler (Test aşaması yok)
#. Yalı (Test aşaması belgesi yenilenmeli)
#. Paket yöneticisi (Test aşaması belgesi yenilenmeli)

Test Edilecek Paket Grupları
----------------------------

(Test aşaması bulunmayan paketleri ve güncellenmesi gerekenleri güncelleyiniz.)

Internet
^^^^^^^^
Salı
----
akregator
groupware
kget

Çarşamba
-------
kmail

Perşembe
--------
thunderbird

Cuma
----
kopete

Pazartesi
---------
konqueror

Salı
----
firefox

Çarşamba
--------
knetattach
knode

Perşembe
--------
kppp
krdc
krfb

Office
^^^^^^
Salı, Çarşamba
--------------
kontact (e-posta, kişiler, takvim, yapılacak öğeler, günlük, notlar, haberler için ayrı ayrı test edilmeli)

Perşembe
--------
evolution

Cuma
----
kalarm
karm

Pazartesi
---------
libreoffice calc
Salı
---
libreoffice draw
Çarşamba
--------
libreoffice impress
Perşembe
--------
libreoffice writer


Sistem
^^^^^^
Salı
----
kwallet
kpowersave

Çarşamba, Perşembe, Cuma
------------------------
Sanal Makine yöneticisi (Test aşaması yok)

Pazartesi-Perşembe
------------------
Yazdırma (Test aşaması yok)


Grafik
^^^^^^
Salı
----
digikam

Çarşamba
--------
gimp

Perşembe
--------
kolourpaint

Cuma
----
gwenview

Pazartesi
---------
kpdf
kdvi
ghostview

Salı
----
kuickshow

Çarşamba
--------
showphoto

Perşembe
--------
ksnapshot
kooka
kfaxview

Multimedia
^^^^^^^^^^^
Salı
----
Amarok
Çarşamba
--------
Juk
Perşembe
--------
k3b
Cuma
----
GnomeMedia player
Pazartesi
---------
mplayer
Salı
----
kaffeine
Çarşamba
--------
kmix
Perşembe
--------
kaudio creator
kscd

Server
^^^^^^

Depoda server bileşeninde bulunan paketler test edilmeli, eksik test aşamaları yazılmalıdır.

[1] http://developer.pardus.org.tr/guides/releasing/testing_process/index.html
[2] http://developer.pardus.org.tr/guides/bugtracking/index.html
[3] http://svn.pardus.org.tr/uludag/trunk/doc/test/2009/testguide/turkish/alfabeta/
[4] http://svn.pardus.org.tr/uludag/trunk/doc/test/2009/testcases/turkish/
[5] http://cekirdek.pardus.org.tr/~semen/testcases/turkish/

