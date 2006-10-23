# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.

#e-mail message templates for mailer module..

error_message = """\
From: Derleme =?utf-8?q?=C3=87iftli=C4=9Fi?= <%(mailFrom)s>
To: %(mailTo)s
Cc: %(ccList)s
Subject: [buildfarm] %(type)s: %(subject)s
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="boundary42"


--boundary42
Content-Type: text/plain;
            charset="utf-8"

 Merhaba,

 Bu ileti derleme çiftliği tarafından otomatik olarak gönderilmektedir.

 Sorumlusu '%(recipientName)s' olan '%(pspec)s' dosyası işlenirken olmaması gereken bir şeyler oldu. Hata mesajı şöyle:

--------------------------------------------------------------------------
%(message)s
--------------------------------------------------------------------------

 Olaydan önce tutulan kayıtların son 20 satırı ise şöyle idi:

--------------------------------------------------------------------------
%(log)s
--------------------------------------------------------------------------

 Kayıt dosyası: http://paketler.pardus.org.tr/logs/%(packagename)s.log

 Kolay gelsin.
 (Vallahi ben bir şey yapmadım..)


--boundary42
Content-Type: text/html;
            charset="utf-8"

<p> Merhaba,

<p> Bu ileti derleme çiftliği tarafından otomatik olarak gönderilmektedir.

<p> Sorumlusu '<b>%(recipientName)s</b>' olan '<b>%(pspec)s</b>' dosyası işlenirken olmaması gereken bir şeyler oldu. Hata mesajı şöyle:

<p><div align=center>
    <table bgcolor=black width=100%% cellpadding=10 border=0>
        <tr>
            <td bgcolor=orangered><b>Hata Mesajı</b></td>
        </tr>
        <tr>
            <td bgcolor=ivory>
                <pre>
%(message)s
                </pre>
            </td>
        </tr>
    </table>
</div>


<p> Olaydan önce tutulan kayıtların son 20 satırı ise şöyle idi:

<p><div align=center>
    <table bgcolor=black width=100%% cellpadding=10 border=0>
        <tr>
            <td bgcolor=orange>cat "<b>Kayıt dosyası</b>" | tail -n 20</td>
        </tr>
        <tr>
            <td bgcolor=ivory>
                <pre>
%(log)s
                </pre>
            </td>
        </tr>
    </table>
</div>

<p> Kayıt dosyası: <a
href="http://paketler.pardus.org.tr/logs/%(packagename)s.log">http://paketler.pardus.org.tr/logs/%(packagename)s.log</a>.

<p> Kolay gelsin.<br> (Vallahi ben bir şey yapmadım..)

--boundary42--
"""

info_message = """\
From: Derleme =?utf-8?q?=C3=87iftli=C4=9Fi?= <%(mailFrom)s>
To: %(mailTo)s
Cc: %(ccList)s
Subject: [buildfarm] %(subject)s
Content-Type: text/plain;
            charset="utf-8"

 Merhaba,

 Bu ileti derleme çiftliği tarafından aşağıdaki mesajı size iletmek için otomatik olarak gönderildi:

 %(message)s


 İyi çalışmalar.
"""
