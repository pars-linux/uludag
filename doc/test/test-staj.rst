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
akregator
firefox
groupware
kget
kmail
knetattach
knode
konqueror
kopete
kppp
krdc
krfb
thunderbird

Office
^^^^^^
kontact (e-posta, kişiler, takvim, yapılacak öğeler, günlük, notlar, haberler için ayrı ayrı test edilmeli)
evolution
kalarm
karm
libreoffice calc
libreoffice draw
libreoffice impress
libreoffice writer


Sistem
^^^^^^
kwallet
kpowersave
Sanal Makine yöneticisi (Test aşaması yok)
Yazdırma (Test aşaması yok)


Grafik
^^^^^^
digikam
ghostview
gimp
gwenview
kdvi
kfaxview
kolourpaint
kooka
kpdf
ksnapshot
kuickshow
showphoto

Multimedia
^^^^^^^^^^^
Amarok
Juk
k3b
GnomeMedia player
mplayer
kaffeine
kmix
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

