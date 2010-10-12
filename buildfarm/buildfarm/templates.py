# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.

# E-mail message templates for mailer module..

error_message = """\
From: %(distribution)s %(release)s %(arch)s Buildfarm <%(mailFrom)s>
To: %(mailTo)s
Cc: %(ccList)s
Subject: [%(subjectID)s] %(type)s: %(subject)s
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="boundary42"


--boundary42
Content-Type: text/plain;
            charset="utf-8"

Hello,

This message is sent from Pardus buildfarm. Please do not reply as it is automatically generated.

An error occured while building the package %(packagename)s (maintainer: %(recipientName)s):

--------------------------------------------------------------------------
%(message)s
--------------------------------------------------------------------------

The last 20 lines of the log before the error happens is as follows:

--------------------------------------------------------------------------
%(log)s
--------------------------------------------------------------------------

Plain log file: http://packages.pardus.org.tr/logs/%(logsdir)s/%(packagename)s.log
Fancy log file: http://packages.pardus.org.tr/logs/%(logsdir)s/%(packagename)s.html

Happy hacking!

--boundary42
Content-Type: text/html;
            charset="utf-8"

<p>Hello,

<p>This message is sent from Pardus buildfarm. Please do not reply as it is automatically generated.

<p>An error occured while building the package '<b>%(packagename)s</b>' (maintainer: <b>%(recipientName)s</b>):

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

<p>Plain log file:
<a href="http://packages.pardus.org.tr/logs/%(logsdir)s/%(packagename)s.log">http://packages.pardus.org.tr/logs/%(logsdir)s/%(packagename)s.log</a><br>
Fancy log file:
<a href="http://packages.pardus.org.tr/logs/%(logsdir)s/%(packagename)s.html">http://packages.pardus.org.tr/logs/%(logsdir)s/%(packagename)s.html</a>


<p>Happy hacking!<br>

--boundary42--
"""

## Info

info_message = """\
From: %(distribution)s %(release)s %(arch)s Buildfarm <%(mailFrom)s>
To: %(mailTo)s
Cc: %(ccList)s
Subject: [%(subjectID)s] %(subject)s
Content-Type: text/plain;
            charset="utf-8"

Hello,

This message is sent from Pardus buildfarm. Please do not reply as it is automatically generated.

%(message)s

Happy hacking!
"""

## Announce

announce_message = """\
From: %(distribution)s %(release)s %(arch)s Buildfarm <%(mailFrom)s>
To: %(announceAddr)s
Subject: [%(subjectID)s] List of recently built packages
Content-Type: text/plain;
            charset="utf-8"

Hello,

This message is sent from Pardus buildfarm. Please do not reply as it is automatically generated.

%(message)s

Happy hacking!
"""

# Convenience dict
_all = {
         'error'     : error_message,
         'announce'  : announce_message,
         'info'      : info_message,
       }
