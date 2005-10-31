#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2004-2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import sys
import os
import re
import string
import getopt

class Sablon:
    def __init__(self, template):
        self.c_start = "<!-- SAYFA İÇERİK BAŞI -->"
        self.c_end = "<!-- SAYFA İÇERİK SONU -->"
        t = self.get_content(template)
        if t == None:
            print "'%s' şablon dosyası problemli!" % (template)
            sys.exit(1)
        self.tmpl_head = t[0]
        self.tmpl_foot = t[2]
        self.tmpl_file = template
    
    def get_content(self, filename):
        f = file(filename, "r")
        text = f.read()
        f.close()
        head = text.split(self.c_start, 1)
        if len(head) != 2:
            return None
        foot = head[1].split(self.c_end, 1)
        if len(foot) != 2:
            return None
        return [ head[0], foot[0], foot[1] ]
    
    def adjust_paths(self, filename, text):
        n = string.count(filename, "/")
        rp = "../" * (n - 1)
        return re.sub("\\$root\\$", rp, text)
    
    def modify_file(self, filename, fake):
        fc = self.get_content(filename)
        if fc == None:
            print "'%s' içerik baş/son belirteçleri yok." % (filename)
            return
        # make header and footer
        head = self.adjust_paths(filename, self.tmpl_head)
        foot = self.adjust_paths(filename, self.tmpl_foot)
        # check if file already has templated
        if fc[0] == head and fc[2] == foot:
            return
        # modify file according to the new template
        if fake:
            print "'%s' değiştirilecek." % filename
        else:
            f = file(filename, "w")
            f.write(head + self.c_start + fc[1] + self.c_end + foot)
            f.close()
            print "'%s' değiştirildi." % filename
    
    def modify_dir(self, dirname, fake):
        os.chdir(dirname)
        for root, dirs, files in os.walk("."):
            for fn in files:
                # dont touch template file or non-html files
                if fn.endswith(".html"):
                    t = os.path.join(root, fn)
                    if t != self.tmpl_file:
                        self.modify_file(t, fake)
            # dont visit subversion or language dirs
            if "eng" in dirs:
                dirs.remove("eng")
            if ".svn" in dirs:
                dirs.remove(".svn")


# command line driver

def usage():
    print "Kullanım: sablonla.py [SEÇENEKLER] [dizin] [şablon]"
    print "  -f, --fake    Sayfaları yalnızca listele, değiştirme."
    sys.exit(0)

if __name__ == "__main__":
        try:
                opts, args = getopt.gnu_getopt(sys.argv[1:], "hf", ["help", "fake"])
        except:
                usage()
    
        tmpl = "./template.html"
        dirname = "."
        opt_fake = 0
    
        for o, v in opts:
                if o in ("-h", "--help"):
                        usage()
                if o in ("-f", "--fake"):
                        opt_fake = 1
    
        if len(args) > 0:
                dirname = args[0]
        if len(args) > 1:
                tmpl = args[1]
    
        s = Sablon(tmpl)
        s.modify_dir(dirname, opt_fake)
