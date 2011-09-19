.. _how-to-be-contributor:

How to be a Contributor?
========================

**Last Modified Date:** |today|

:Author: Semen Cirit

:Version: 0.3

Process of Being Pardus Contributor
***********************************

Pardus needs accurate and continuous contributions. Even if there is no precise period that we look for, it is rare for applications to be accepted from people contributing for less than 6 months. If you are unsure if your contributions constitute as accurate and continuous, ask your mentors_ or the other Pardus community members (They do not need to be Pardus Contributor, just a part of the community). Maybe they can even add some kind of assistance to your application.

******************************
Applicant Tracking on Bugzilla
******************************

- Developers and testers can follow this process in order to be a Pardus contributor.
- For translators applications can be held from `Pardus translation website`_. (See :ref:`introduction-to-translation`)
- For bug triagers please see `Bug reporting and triaging`_
- For content writers please see `Documentation`_
- For designers please see `Graphical design and multimedia`_

****************
Tracking Process
****************

Application Request
--------------------

#. Report a bug for the related component of "Yeni Katkıcı / New Contributor" product.
#. The summary of the bug likes "Testçi veya Geliştirici Adaylık Ad Soyad" "Tester or Developer Applicant Name Surname".
#. The bug details part should contains the answers of the following personal questions.

    #. What are the distributions that you use properly?
    #. From when and at what level do you use Pardus?
    #. What does it mean for you to contribute to a free software project
    #. Have you ever contributed any free software project before? If yes, which project, in what way, how long?
    #. Why would you want to contribute Pardus?
    #. How much time could you spend for Pardus?
    #. Please attach your short background as an attachment or give links.
    #. If the application is for development, the applicant should also attach these informations that you have already done:
        #. The prepared packages for Pardus repositories, or a improvement for Pardus projects.
        #. The bugs that you have fixed at `Pardus bugzilla`_.
        #. The other contributions that you have done for other distributions.
        #. If you are/were an intern at Pardus, you can directly request for beeing contributor developer with your internship.
    #. What are your plans and ideas for Pardus in the near and far future.

#. If the application has missing parts or the applicant report his/her bug carelessly, it will be closed with status RESOLVED/INVALID by application coordinators and the `Rejection Stock Response`_ is given.
#. If the applicant gets a rejection at that stage, in the case of his/her effort to Pardus, he/she can reapply in 3 months to be tester, 6 months to be developer.

IRC Interview
-------------
#. Application coordinators triage **NEW** status bugs weekly on "New Contributor" product and make a interview plan with mentor group and choose an interviewer.
#. Assign the bug to interviewer
#. Interviewer write and ask the time of the IRC meeting if the applicant is available at that time.
#. Besides the interviewer, the mentors that have reviewed  applicants' contributions can also attend to IRC meeting
#. At some cases some additional jobs can be demanded, and contributor application can be delayed and wait for this jobs.
    #. The new bugs depend to the applicant bug in order to track easily
#. According to applicant contributions and the result of the meeting, interviewer give their opinions on applicant bug
    #. If the opinions are positive, interviewer change the bug status to **RESOLVED/FIXED**
    #. If not the bug status is taken to **RESOLVED/INVALID** and `Rejection Stock Response`_ will be given

Guiding Rules
-------------
#. Until an interviewer has been assigned to applicant, the mentor coordinators will track the process. (Traking the applicant bugs, assign interviewer etc.)
#. After the interviewer has assigned, he/she is responsible for the applicant. (Tracking his/her applicants, sending necessary comments to bug and editing it etc.)


***************
Stock Responses
***************

Rejection Stock Response
------------------------
    ::

        Başvurunuz ilgili ekip tarafından incelenmiş, maalesef sorulara verdiğiniz
        yanıtlar yeterli bulunmamıştır. Ayrıca başvurunuz hangi alanda Pardus'a katkı verebileceğinizi
        ölçmemize yardımcı olabilecek örnek bir uygulama kodu, çözümüne katkıda bulunduğunuz bir hata,
        yama, vb. gibi geçmiş katkı referansları da içermemektedir.

        Unutmayın ki, Pardus'u kullanmak, sorunlarınızı hata takip sistemine bildirmek,
        listeleri takip edip listelerdeki yardım taleplerini yanıtlamak Pardus'a katkı
        vermenin en güzel yollarından biridir. Moralinizi bozmayın ve bilgi birikiminizin
        bizi ikna edecek düzeye geldiğini düşündüğünüzde tekrar başvurmaktan çekinmeyin.

        Bol şanslar.

    ::

        Your application has been reviewed and we are sorry to say that the
        answers you have given were found inadequate. Furthermore your
        application does not contain any code samples, patches, a reference to
        a bug that you have solved or any other contribution that help us
        determine your potential as a future developer.
        Please note that using Pardus, reporting bugs, following and
        habitually reading the mail lists and responding to any help demand is
        also a good way to contribute.
        Do not hesitate to reapply whenever you decide your contribution to
        Pardus and knowledge is adequate for persuading the Pardus Application
        Review Team.



Tester Acceptence Stock Response
--------------------------------

    ::

        Başvurunuz olumlu sonuçlanmıştır,  testçi@pardus.org.tr için gerekli izinleriniz verilmiştir.
        Pardus'a yapacağınız katkılarda dolayı şimdiden size teşşekür ederiz.

    ::

        Your application is favorable, the permissions about testçi@pardus.org.tr has been given. 
        Thank you in advance for their generous contributions to make for Pardus.

Waiting in the Queue Stock Response
-----------------------------------
    ::

        Şu anda tüm mentor'larımızın slotları doludur, slot'ları uygun olan mentor'lar oluştuğunda
        size geri dönüş yapılacaktır. Bu süre içerisinde Pardus'a yaptığınız katkılara devam edebilir 
        ve kendinizi bu yönde daha fazla geliştirebilir ve mentor sürecinizi kısaltabilirsiniz.

        İyi günler,

    ::

        ll slots of our mentors are occupied, when the slots are available we will back to your application.
        uring this period, you can continue to contribute to Pardus, and may shorten your mentoring process.


.. _Junior Jobs: http://bugs.pardus.org.tr/buglist.cgi?keywords=JUNIORJOBS&query_format=advanced&keywords_type=allwords&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED
.. _bugzilla: http://bugs.pardus.org.tr
.. _Pardus translation website: http://translate.pardus.org.tr
.. _Bug reporting and triaging: http://developer.pardus.org.tr/guides/newcontributor/areas-to-contribute.html#bug-reporting-and-triaging
.. _Documentation: http://developer.pardus.org.tr/guides/newcontributor/areas-to-contribute.html#documentation
.. _Graphical design and multimedia: http://developer.pardus.org.tr/guides/newcontributor/areas-to-contribute.html#graphical-design-and-multimedia
.. _QUIZSEND: http://bugs.pardus.org.tr/describekeywords.cgi
.. _ANSWERREC: http://bugs.pardus.org.tr/describekeywords.cgi
.. _QUIZAPPROVED: http://bugs.pardus.org.tr/describekeywords.cgi
.. _MENTORASSIGNED: http://bugs.pardus.org.tr/describekeywords.cgi
.. _responsibilities of the contributor: http://developer.pardus.org.tr/guides/newcontributor/new-contributor-guide.html#responsibilities-of-a-contributor
.. _technical mail list: http://liste.pardus.org.tr/mailman/listinfo/teknik
.. _Pardus bugzilla: http://bugs.pardus.org.tr
.. _expected developer: http://developer.pardus.org.tr/guides/newcontributor/developer_roles.html#expected-developer
.. _mentors: http://developer.pardus.org.tr/guides/newcontributor/newcontributor_mentors.html

