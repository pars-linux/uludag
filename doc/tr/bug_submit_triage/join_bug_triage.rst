Hata Ayıklama Neleri İçerir (Bug Triage)
========================================

Hata ayıklayan kişiler aşağıda bulunan durumlardan emin olmalıdırlar:

    * Geliştiricilerin hatayı tekrarlamaları ve çözmeleri için, hata raporu yeterli bilgiyi içeriyor mu?
    * Hata doğru bileşene ve sürüme atanmış mı?
    * Hatanın aynısı daha önce raporlanmış mı?
    * Yeni özellik olarak raporlanan hatalar düzgün bir şekilde raporlanmış mı?
    * Çözümlenmiş hatalar kapatılmış mı?

* Hata ayıklayan kişiler bir hata üzerinde tek başına çalışabilecekleri gibi, tek bir bileşen üzerinde grup olarak çalışabilirler.
* Haftalık toplantılar yaparak problemler ve emin olunmayan hatalar hakkında tartışılır.
* Pardus test ekibi listesi hata ayıklıyıcılarının yardımlaşmaları ve emin olmadıkları durumlar hakkında soru sorabilmeleri için kullanılır.
* Tecrübeli hata ayıklayıcılar, yeni hata ayıklayıcıların mentorudur.
* Hata ayıklamak hatayı anlayıp çözüme ulaştırmak değildir. Yeni raporlanan hatalara bakmak, birbiri ile aynı olan, ek bilgiye ihtiyaç duyulan, yanlış bileşene atanan, yeni özellik olarak raporlanan hataları bulmak ve raporlamak demektir.
* Başvurmak için programlama bilgisine ihtiyaç duyulmamaktadır, sadece Pardus ve Linux'a aşina olmak yeterlidir.
* Tamamıyle gönüllü bir iştir. Saatlerce oturup uğraşmanız gerekmez. (Vakit harcamak isteyene de hayır demeyiz tabi :))

Neden Hata Ayıklanmalıdır?
==========================

    * Geliştiricilerin hataların aynısını bulma, hataları tekrarlama, eksik bilgileri isteme gibi işlemler yerine hatayı çözmeye daha fazla vakit ayırabilmeleri içindir.
    * Sürümler öncesinde çözümlenmesi gereken hataları bulmak içindir. (Sürüm adında açılmış olan hatalara ve sürüm engelleyici listelerine ekleyebilmek için.)
    * Hata raporlayan kişilerin hataları ile ilgilenildiğini hissetmeleri içindir.
    * Doğru ve kesin toplam hata sayısını elde edebilmek içindir.
    * Sürümün bitişi (EOL) için kapatılacak olan ve diğer sürüme aktarılacak olan hataların düzenlenmesi içindir.
    * Hata çözülene kadar, kullanıcılara yardım edecek bazı kısa çözüm yollarının ortaya çıkmasını sağlar.
    * Hata yoğunluğunun dağıtımın hangi kısmında olduğunun ortaya çıkmasına yardımcı olur.
    * Pardus'u öğrenmenin iyi bir yoludur.

.. Nasıl Katılınır?
.. ================

..   * Pardus hata sisteminde bir hesap açın ve hata takip sistemi üzerinde yürütülen katkıcı başvuru sürecine dahil olun. (bkz joinus_policy.rst)
..   * Üyeliğinizin kabul edilmesi zaman alabilir, bu yüzden biraz sabırlı olmalısınız. (Üyeliğiniz kabul edildikten sonra hata takip sisteminde hata ayıklamanız için size bazı özel haklar verilecektir.)

İletişim
========

   * Pardus test ekibi listesi
          * Hata ayıklama ile ilgili tüm duyurular ve tartışmalar bu liste üzerinden yapılmaktadır.
   * IRC #pardus-bugtriage
   * Haftalık IRC hata ayıklama toplantıları

Hata ayıklamaya nereden başlanır
================================
    * bkz howto.triage.rst
