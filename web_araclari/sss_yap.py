#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import sys

def load_sss(filename):
    f = file(filename)
    sss = []
    sorular = []
    soru = []
    for line in f:
        line = line.strip('\n')
        if line == "":
            pass
        elif line == "***":
            break
        elif line.startswith("@@"):
            sorular = []
            sss.append( (line[2:], sorular) )
        elif line.startswith("@"):
            soru = [ line[1:] ]
            sorular.append(soru)
        else:
                soru.append(line)
    f.close()
    return sss

def print_index(sss):
    for sorular in sss:
        print "<span class='baslik'><img src='./images/bullet-krm.png' width='11' height='11'>%s</span><br><br>" % (sorular[0])
        for soru in sorular[1]:
            print "<a href='./sss.html#%s'>%s</a><br>" % (soru[0], soru[1])
        print "<br><br>"
    print "<hr width='50%'>"

def print_body(sss):
    for sorular in sss:
        print "<span class='baslik'><img src='./images/bullet-krm.png' width='11' height='11'>%s</span><br><br><br>" % (sorular[0])
        for soru in sorular[1]:
            print "<a name='%s' href='./sss.html#top'><i>%s</i></a><br><br>" % (soru[0], soru[1])
            for line in soru[2:]:
                print "%s\n" % (line)
            print "<br><br>"
        print "<br><br>"

def print_head():
    print """<!-- SAYFA İÇERİK BAŞI -->
<table width="695" border="0" cellspacing="0" cellpadding="0">
<tr>
<td width="20" height="286" valign="top"><img src="./images/bullet6.png" width="20" height="20" hspace="0" vspace="0" align="top"></td>
<td width="10" valign="top">&nbsp;</td>
<td width="661" valign="top" class="metin">
<p><span class="baslik">
<font face="Verdana, Arial, Helvetica, sans-serif" name="top">Sıkça Sorulan Sorular</font></span><br>
<br>

<p class="metin">
Aşağıda, Uludağ projesi ve Pardus hakkında sıkça sorulan soruları bulabilirsiniz.
</p>
"""

def print_foot():
    print """</p>
</td>
</tr>
</table>
<!-- SAYFA İÇERİK SONU -->
"""

sss = load_sss(sys.argv[1])
print_head()
print_index(sss)
print_body(sss)
print_foot()
