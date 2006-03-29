#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2004-2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import sys
import os
import subprocess
import shutil
import codecs
import re
import time
from stat import ST_SIZE
import getopt

#
# Utilities
#

def capture(*cmd):
    """Capture output of the command without running a shell"""
    a = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return a.communicate()

def run(*cmd):
    """Run the command without running a shell"""
    return subprocess.call(cmd)

#
# SVN
#

def svn_fetch(path, filename):
    print "'%s' çekiliyor..." % path
    # fetch last revision
    data = capture("/usr/bin/svn", "cat", path)
    f = file(filename, "w")
    f.write(data[0])
    f.close()
    # get last changed date
    data = capture("/usr/bin/svn", "info", path)
    date = None
    for tmp in data[0].split("\n"):
        if tmp.startswith("Last Changed Date: "):
            date = tmp[19:29]
    return date

#
# LyX
#

def retouch_lyx(lyxname):
    # FIXME: fix regexps, handle hyperref package, and other minor probs
    print "'%s' düzeltiliyor..." % self.lyxname
    # lyx dosyasini okuyalim
    f = file(self.lyxfile, "r")
    lyx = f.read()
    f.close()
    # paragraf aralari bosluk olmali
    #re.sub("\\paragraph_separation .*?\n", "\\paragraph_separation skip\n", lyx)
    # kaliteli pdf cikti icin font secimi
    #re.sub("\\fontscheme .*?\n", "\\fontscheme pslatex\n", lyx)
    f = file(self.lyxfile, "w")
    f.write(lyx)
    f.close()

#
# PDF
#

def export_pdf(lyxname, pdfname):
    print "'%s' oluşturuluyor..." % pdfname
    run("/usr/bin/lyx", "-e", "pdf2", lyxname)
    shutil.move(lyxname + ".pdf", pdfname)
    return str(os.stat(pdfname)[ST_SIZE] / 1024)

#
# HTML
#

hevea_fixes = """
\\newcommand{\\textless}{\\@print{&lt;}}
\\newcommand{\\textgreater}{\\@print{&gt;}}
\\newcommand{\\textbackslash}{\\@print{&#92;}}
\\newcommand{\\textasciitilde}{\\@print{&#126;}}
\\newcommand{\\LyX}{\\@print{LyX}}
"""

html_tmpl = u"""<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body>
<!-- SAYFA İÇERİK BAŞI -->
<div class="belge">
%s
</div>
<!-- SAYFA İÇERİK SONU -->
</body>
</html>
"""

def fix_html(htmlname):
    f = codecs.open(htmlname, "r", "iso-8859-9")
    doc = f.read()
    f.close()
    # fix translations
    doc = re.sub("Table of Contents", u"İçindekiler", doc)
    doc = re.sub("Abstract", u"Özet", doc)
    # cut unneeded header and footer
    m1 = re.search("\<\!--CUT.*--\>\n", doc)
    m2 = re.search("\<\!--HTMLFOOT--\>", doc)
    c1 = 0
    c2 = -1
    if m1: c1 = m1.end()
    if m2: c2 = m2.start()
    doc = doc[c1:c2]
    # save
    f = codecs.open(htmlname, "w", "utf-8")
    f.write(html_tmpl % doc)
    f.close()

def export_html(lyxname, texname, htmlname):
    f = file("duzeltmeler.hva", "w")
    f.write(hevea_fixes)
    f.close()
    print "'%s' oluşturuluyor..." % texname
    run("/usr/bin/lyx", "-e", "latex", lyxname)
    print "'%s' oluşturuluyor..." % htmlname
    run("/usr/bin/hevea", "-fix", "duzeltmeler.hva", texname, "-o", htmlname)
    fix_html(htmlname)

#
# Main
#

entry_tmpl = """
<tr>
<td align="left"><b>%(NAME)s</b> (%(DATE)s)</td>
<td><a href="./%(DIR)s/index.html">HTML</a></td>
<td><a href="./%(DIR)s/%(DIR)s.html">HTML (tek sayfa)</a></td>
<td><a href="./%(DIR)s/%(DIR)s.pdf">PDF (%(PDFSIZE)s KB)</a></td>
</tr>
"""

def make_document(repo_uri, name, do_fetch=True):
    path = os.path.dirname(repo_uri)
    filename = os.path.basename(repo_uri)
    basename = filename[:]
    if basename.endswith(".lyx"):
        basename = basename[:-4]
    pdfname = basename + ".pdf"
    htmlname = basename + ".html"

def usage():
    print "Kullanım: belgeyap.py [seçenekler] <svn_repo_adresi> <belge_adı>"
    print " -h, --help        Yardım"
    print " -f, --no-fetch   Dosyaları yeniden çekme"

def main(args):
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hf", ["help", "no-fetch"])
    except:
        usage()
        return
    
    if not os.path.exists("/usr/bin/hevea"):
        print "Hata: Belgeleri HTML'e çevirebilmek için 'hevea' paketini kurmalısınız."
        return
    
    if not os.path.exists("/usr/bin/lyx"):
        print "Hata: Belgeleri PDF ve HTML'e çevirebilmek için 'lyx' paketini kurmalısınız."
        return
    
    do_fetch = True

    for o, v in opts:
        if o in ("-h", "--help"):
            usage()
            return
        if o in ("-f", "--no-fetch"):
            do_fetch = False
    
    if len(args) != 2:
        usage()
        return
    
    make_document(args[0], args[1], do_fetch)

#
#
#

class Exporter:
    def __init__(self, lyxfile, basename, img_path):

def generate_doc(docfile, do_fetch=True):
    # defaults
    ikonlar = "../../images"
    dosyalar = []
    # open document template and get information
    f = file(docfile)
    exec(f)
    f.close()
    # cd into document directory
    enter_dir(dizin)
    # fetch files
    date = ""
    if do_fetch:
        if do_fetch:
            date = svn_fetch(depo, belge)
        # extra files, images, etc
        for t in dosyalar:
            ensure_path(t)
            svn_fetch(depo, t)
    # do the export
    a = Exporter(belge, dizin, ikonlar)
    a.export()
    # add to svn
    # FIXME: handle svn
    # output information
    dict = {
        "NAME": isim,
        "DATE": date,
        "DIR": dizin,
        "PDFSIZE": str(os.stat(dizin + ".pdf")[ST_SIZE] / 1024)
    }
    print entry_tmpl % dict
    # leave directory
    os.chdir("..")




if __name__ == "__main__":
    main(sys.argv[1:])
