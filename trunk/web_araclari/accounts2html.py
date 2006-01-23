#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2004, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

# accounts2html.py
# converts SVN account to web page view.

import codecs
import getopt

accounts_start="""
<html>
<body>
<!-- SAYFA İÇERİK BAŞI -->

<p><span class="baslik"> - Pardus Geliştiricileri</span>
<br>
<br>

<table border="0" cellspacing="10">
<tr align="left">
<th><b>Geliştirici</b></th>
<th><b>E-posta Adresi</b></th>
<th><b>Hızlı Mesajlaşma Adresi</b></th>
</tr>
"""
account_template="""<tr>
<td><span class="isimler">$NAME$ ($ACCOUNT$)</span></td>
<td><span class="metin"><a href="mailto:$MAIL$">$MAIL$</a></span></td>
<td><span class="metin">$IM$</span></td>
</tr>
"""
accounts_end="""
</table>
<!-- SAYFA İÇERİK SONU -->
</body>
</html>
"""

class A2HError(Exception):
    pass

def usage():
    print "\n\t%s -a hesap_dosyası -o çıktı_dosyası -t şablon_dosyası\n" % sys.argv[0]
    sys.exit(0)

class AccountsToHtml:
    def __init__(self, file):
        self.f = codecs.open(file, "r", "utf-8")

    def accounts(self):
        """Get accounts; you know the lines which don't start with a #"""
        return [act.strip() for act in self.f.readlines() if not act.strip().startswith("#")]

    def accountToHtml(self):
        for act in self.accounts():
            html = account_template
            try:
                accountname, name, mail, im = act.split(":")
            except ValueError:
                e = "Each entry should have 4 columns.\n"
                e += "This doesn't: '%s'" % (act)
                raise A2HError, e
            
            html = html.replace("$NAME$", name)
            html = html.replace("$ACCOUNT$", accountname)
            html = html.replace("$MAIL$", mail)
            html = html.replace("$IM$", im)
            yield html

    def toHtml(self):
        tmp = unicode(accounts_start, "utf-8")
        for a in self.accountToHtml():
            tmp += "\n" + a + "\n"
        tmp += unicode(accounts_end, "utf-8")
        print tmp
        return tmp
            
        
if __name__ == "__main__":
    import sys
    import sablonla

    accountsfile, filename, tmpl = "", "", ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:o:t:", ["accounts=", "outfile=", "template="])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == "-a" or opt == "--accounts":
            accountsfile = arg
        if opt == "-o" or opt == "--outfile":
            filename = arg
        if opt == "-t" or opt == "--template":
            tmpl = arg

    if accountsfile == "" or filename == "" or tmpl == "":
        usage()

    try:
        sablon = sablonla.Sablon(tmpl)
        a2h = AccountsToHtml(accountsfile)

        f = codecs.open(filename, "w", "utf-8")
        f.write(a2h.toHtml())
        f.close()
        
        sablon.modify_file(filename, False)
    except IndexError:
        print "Usage: %s accounts_file output_file" % sys.argv[0]

