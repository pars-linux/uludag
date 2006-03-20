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
#


#e-mail message templates for mailer module..

error_message = """\
From: Derleme =?utf-8?q?=C3=87iftli=C4=9Fi?= <%(mailFrom)s>
To: %(mailTo)s
Cc: %(ccList)s
Subject: [buildfarm] %(type)s: %(subject)s
Content-Type: text/plain;
            utf-8

 Merhaba,

 Bu ileti derleme çiftliği tarafından otomatik olarak gönderilmektedir.

 Sorumlusu '%(recipientName)s' olan '%(pspec)s' dosyası işlenirken olmaması gereken bir şeyler oldu. Hata mesajı şöyle:


-- <Hata Mesajı> -------------------------------------------------------

%(message)s

-- </Hata Mesajı> ------------------------------------------------------


 Olaydan önce tutlan kayıtların son 20 satırı ise şöyle idi:


-- <Kayıt Dosyası> -----------------------------------------------------

%(log)s

-- </Kayıt Dosyası> ----------------------------------------------------


 Kolay gelsin.
 (Vallahi ben bir şey yapmadım..)
"""

info_message = """\
From: Derleme =?utf-8?q?=C3=87iftli=C4=9Fi?= <%(mailFrom)s>
To: %(mailTo)s
Cc: %(ccList)s
Subject: [buildfarm] %(subject)s
Content-Type: text/plain;
            utf-8

 Merhaba,

 Bu ileti derleme çiftliği tarafından aşağıdaki mesajı size iletmek için otomatik olarak gönderildi:

 %(message)s


 İyi çalışmalar.
"""
