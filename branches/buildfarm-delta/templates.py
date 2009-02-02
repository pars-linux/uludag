# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2008 TUBITAK/UEKAE
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.

#e-mail message templates for mailer module..

error_message = """\
From: Pardus Buildfarm 2008 <%(mailFrom)s>
To: %(mailTo)s
Cc: %(ccList)s
Subject: [buildfarm] %(type)s: %(subject)s
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="boundary42"


--boundary42
Content-Type: text/plain;
            charset="utf-8"

Hello,

This message is sent from Pardus buildfarm. Please do not reply as it is automatically generated.

An error occured while processing the file '%(pspec)s' (maintainer: '%(recipientName)s'). Error log is as follows:

--------------------------------------------------------------------------
%(message)s
--------------------------------------------------------------------------

The last 20 lines of the log before the error happens is as follows:

--------------------------------------------------------------------------
%(log)s
--------------------------------------------------------------------------

Log file: http://paketler.pardus.org.tr/logs/2008/%(packagename)s.log

Happy hacking!

--boundary42
Content-Type: text/html;
            charset="utf-8"

<p>Hello,

<p>This message is sent from Pardus buildfarm. Please do not reply as it is automatically generated.

<p>An error occured while processing the file '<b>%(pspec)s</b>' (maintainer: <b>%(recipientName)s</b>). Error log is as follows:

<p><div align=center>
    <table bgcolor=black width=100%% cellpadding=10 border=0>
        <tr>
            <td bgcolor=orangered><b>Error log</b></td>
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


<p>The last 20 lines of the log before the error happens is as follows:

<p><div align=center>
    <table bgcolor=black width=100%% cellpadding=10 border=0>
        <tr>
            <td bgcolor=orange>cat "<b>Log file</b>" | tail -n 20</td>
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

<p>Log file: <a
href="http://paketler.pardus.org.tr/logs/2008/%(packagename)s.log">http://paketler.pardus.org.tr/logs/2008/%(packagename)s.log</a>.

<p>Happy hacking!<br>

--boundary42--
"""

info_message = """\
From: Pardus Buildfarm 2008 <%(mailFrom)s>
To: %(mailTo)s
Cc: %(ccList)s
Subject: [buildfarm] %(subject)s
Content-Type: text/plain;
            charset="utf-8"

Hello,

This message is sent from Pardus buildfarm. Please do not reply as it is automatically generated.

%(message)s
Happy hacking!
"""

announce_message = """\
From: Pardus Buildfarm 2008 <%(mailFrom)s>
To: %(announceAddr)s
Subject: [buildfarm] [REPORT] New packages in -testing repository
Content-Type: text/plain;
            charset="utf-8"

Hello,

This message is sent from Pardus buildfarm. Please do not reply as it is automatically generated.

%(message)s

Happy hacking!
"""
