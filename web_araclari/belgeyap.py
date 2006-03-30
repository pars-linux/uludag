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

def operation(msg):
    print "\x1b[34;01m* %s\x1b[0m" % msg

def error(msg):
    print "\x1b[35;01m* %s\x1b[0m" % msg

#
# SVN
#

def svn_fetch(repo_uri, filename):
    operation("'%s' çekiliyor..." % repo_uri)
    # fetch last revision
    data = capture("/usr/bin/svn", "cat", repo_uri)
    f = file(filename, "w")
    f.write(data[0])
    f.close()
    # get last changed date
    data = capture("/usr/bin/svn", "info", repo_uri)
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
    operation("'%s' düzeltiliyor..." % lyxname)
    # lyx dosyasini okuyalim
    f = file(lyxname)
    lyx = f.read()
    f.close()
    # paragraf aralari bosluk olmali
    #re.sub("\\paragraph_separation .*?\n", "\\paragraph_separation skip\n", lyx)
    # kaliteli pdf cikti icin font secimi
    #re.sub("\\fontscheme .*?\n", "\\fontscheme pslatex\n", lyx)
    f = file(lyxname, "w")
    f.write(lyx)
    f.close()

def collect_files(lyxname):
    flag = 0
    files = []
    for line in file(lyxname):
        if flag == 0:
            if line.startswith("\\begin_inset Graphics"):
                flag = 1
        else:
            parts = line.strip().split()
            if parts[0] == "filename":
                files.append(parts[1])
                flag = 0
    return files

#
# PDF
#

def export_pdf(lyxname, pdfname):
    operation("'%s' oluşturuluyor..." % pdfname)
    run("/usr/bin/lyx", "-e", "pdf2", lyxname)
    shutil.move(lyxname[:-4] + ".pdf", pdfname)
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

def export_html(lyxname, htmlname):
    f = file("duzeltmeler.hva", "w")
    f.write(hevea_fixes)
    f.close()
    texname = lyxname[:-4] + ".tex"
    operation("'%s' oluşturuluyor..." % texname)
    run("/usr/bin/lyx", "-e", "latex", lyxname)
    operation("'%s' oluşturuluyor..." % htmlname)
    run("/usr/bin/hevea", "-fix", "duzeltmeler.hva", texname, "-o", htmlname)
    os.unlink("duzeltmeler.hva")
    os.unlink(texname)
    fix_html(htmlname)

#
# Document converter
#

entry_tmpl = """
<tr>
<td align="left"><b>%(NAME)s</b> (%(DATE)s)</td>
<td><a href="./%(HTMLNAME)s">HTML</a></td>
<td><a href="./%(PDFNAME)s">PDF (%(PDFSIZE)s KB)</a></td>
</tr>
"""

def make_document(repo_uri, do_fetch=True):
    path = os.path.dirname(repo_uri)
    filename = os.path.basename(repo_uri)
    basename = filename[:]
    if basename.endswith(".lyx"):
        basename = basename[:-4]
    pdfname = basename + ".pdf"
    htmlname = basename + ".html"
    
    if do_fetch:
        last_edit = svn_fetch(repo_uri, filename)
        files = collect_files(filename)
        for name in files:
            try:
                os.makedirs(os.path.dirname(name))
            except OSError, e:
                if e.errno != 17:
                    raise
            svn_fetch(os.path.join(path, name), name)
    else:
        last_edit = "depodan çekmeden bilemem"
    
    retouch_lyx(filename)
    pdf_size = export_pdf(filename, pdfname)
    export_html(filename, htmlname)
    # FIXME: html resim linklerini düzelt
    
    operation("İşlem tamam, belge bilgileri:")
    
    # FIXME: belge adını dosyadan çekmeye çalış
    dict = {
        "NAME": basename,
        "HTMLNAME": htmlname,
        "PDFNAME": pdfname,
        "DATE": last_edit,
        "PDFSIZE": pdf_size,
    }
    print entry_tmpl % dict

#
# Command line driver
#

def usage():
    print "Kullanım: belgeyap.py [seçenekler] <svn_belge_adresi>..."
    print " -h, --help        Yardım"
    print " -f, --no-fetch   Dosyaları yeniden çekme"

def main(args):
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hf", ["help", "no-fetch"])
    except:
        usage()
        return
    
    if not os.path.exists("/usr/bin/hevea"):
        error("Hata: Belgeleri HTML'e çevirebilmek için 'hevea' paketini kurmalısınız.")
        return
    
    if not os.path.exists("/usr/bin/lyx"):
        error("Hata: Belgeleri PDF ve HTML'e çevirebilmek için 'lyx' paketini kurmalısınız.")
        return
    
    do_fetch = True

    for o, v in opts:
        if o in ("-h", "--help"):
            usage()
            return
        if o in ("-f", "--no-fetch"):
            do_fetch = False
    
    if len(args) < 1:
        usage()
        return
    
    for arg in args:
        make_document(arg, do_fetch)

if __name__ == "__main__":
    main(sys.argv[1:])
