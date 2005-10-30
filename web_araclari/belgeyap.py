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
import shutil
import codecs
import re
import time
from stat import ST_SIZE
import getopt
from svn import core, client

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

navigation_tmpl = u"""
<table class="navbar"><tbody><tr>
<td class='%(PREV_CLASS)s'>
%(PREV_LINK)s
<img src="%(IMG_PATH)s/nav_back.png" border=0> Önceki sayfa%(PREV_END)s
</td>
<td class='navbut'>
<a href='index.html'>
<img src="%(IMG_PATH)s/nav_home.png" border=0> Başlangıç</a>
</td>
<td class='%(NEXT_CLASS)s'>
%(NEXT_LINK)s
<img src="%(IMG_PATH)s/nav_back.png" border=0> Sonraki sayfa%(NEXT_END)s
</td>
</tr></tbody></table>
"""

entry_tmpl = """
<tr>
<td align="left"><b>%(NAME)s</b> (%(DATE)s)</td>
<td><a href="./%(DIR)s/index.html">HTML</a></td>
<td><a href="./%(DIR)s/%(DIR)s.html">HTML (tek sayfa)</a></td>
<td><a href="./%(DIR)s/%(DIR)s.pdf">PDF (%(PDFSIZE)s KB)</a></td>
</tr>
"""

hevea_fixes = """
\\newcommand{\\textless}{\\@print{&lt;}}
\\newcommand{\\textgreater}{\\@print{&gt;}}
\\newcommand{\\textbackslash}{\\@print{&#92;}}
\\newcommand{\\textasciitilde}{\\@print{&#126;}}
\\newcommand{\\LyX}{\\@print{LyX}}
"""


class Cutter:
    levels = {
        "section": 1,
        "subsection": 2,
        "subsubsection": 3,
        "subsubsubsection": 4,
        "paragraph": 5,
        "subparagraph": 6
    }
    
    class Node:
        def __init__(self):
            self.name = ""
            self.level = 0
            self.head = ""
            self.text = ""
            self.nodes = []
            self.parent = None
    
    def __init__(self, filename):
        self.load_doc(filename)
    
    def load_doc(self, filename):
        self.filename = filename
        # hevea is generating 8859-9 output, convert to utf-8
        f = codecs.open(filename, "r", "iso-8859-9")
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
        # done
        self.doc = doc
    
    def save_html(self, filename, text):
        f = codecs.open(filename, "w", "utf-8")
        f.write(html_tmpl % text)
        f.close()
    
    def make_nodes_tree(self):
        # parse nodes and generate a tree structure of the document
        nodes = self.doc.split("<!--TOC ")
        self.header = nodes[0]
        self.nodes = []
        self.level = 0
        last_node = self
        for node in nodes[1:]:
            info, data = node.split("-->", 1)
            level, name = info.split(" ", 1)
            head, text = data.split("<!--SEC END -->", 1)
            n = self.Node()
            n.name = name
            n.level = self.levels[level]
            n.head = head
            n.text = text
            while n.level <= last_node.level:
                last_node = last_node.parent
            n.parent = last_node
            last_node.nodes.append(n)
            last_node = n
    
    def nr_lines(self, node):
        # how many lines long a particular node is
        return node.head.count("\n") + node.text.count("\n")
    
    def nr_total_lines(self, node):
        # total number of lines of node and its chillun
        return (
            self.nr_lines(node) +
            reduce(lambda x, y: x + self.nr_total_lines(y), node.nodes, 0)
        )
    
    def fold_node(self, node):
        node.text = reduce(lambda x, y: x + y.head + y.text, node.nodes, node.text)
        node.nodes = []
    
    def make_pages(self, parent=None):
        # fold small nodes into a single page
        if parent == None:
            for node in self.nodes:
                self.make_pages(node)
                if self.nr_total_lines(node) < 60:
                    self.fold_node(node)
            return
        for node in parent.nodes:
            self.make_pages(node)
            if self.nr_total_lines(node) < 60:
                self.fold_node(node)
    
    def name_pages(self, parent=None, prefix=""):
        if parent == None:
            i = 1
            for node in self.nodes:
                if i == 1:
                    node.filename = "index.html"
                else:
                    node.filename = "node-%d.html" % i
                self.name_pages(node, str(i))
                i += 1
            return
        i = 1
        for node in parent.nodes:
            node.filename = "node-%s-%d.html" % (prefix, i)
            self.name_pages(node, "%s-%d" % (prefix, i))
            i += 1
    
    def append_toc(self, parent):
        # FIXME: full toc tree
        if parent.nodes:
            parent.text += "\n<UL>"
            for node in parent.nodes:
                parent.text += "\n<LI><A HREF='./%s'>%s</A></LI>" % (node.filename, node.name)
                self.append_toc(node)
            parent.text += "\n</UL>"
    
    dest_pat = re.compile('NAME="(.*?)"')
    link_pat = re.compile('HREF="(.*?)"')
    
    def collect_links(self, node, dict):
        for m in re.findall(self.dest_pat, node.head):
            dict[m] = node.filename
        for m in re.findall(self.dest_pat, node.text):
            dict[m] = node.filename
        for n in node.nodes:
            self.collect_links(n, dict)
    
    def change_link(self, m):
        key = m.group(1)
        if key.startswith("#"):
            key = key.lstrip("#")
        if self.url_dict.has_key(key):
            return 'HREF="%s#%s"' % (self.url_dict[key], key)
        if key.startswith("http://") or key.startswith("ftp://"):
            return key
        print "Warning: unknown link %s" % key
        return "HREF='%s'" % key
    
    def change_links(self, node):
        node.head = self.link_pat.sub(self.change_link, node.head)
        node.text = self.link_pat.sub(self.change_link, node.text)
        for n in node.nodes:
            self.change_links(n)
    
    def fix_links(self):
        dict = {}
        for node in self.nodes:
            self.collect_links(node, dict)
        self.url_dict = dict
        for node in self.nodes:
            self.change_links(node)
    
    def nav_code(self, prevnode, nextnode):
        dict = {
            "IMG_PATH": self.img_path,
            "PREV_CLASS": "navhide",
            "PREV_LINK": "",
            "PREV_END": "",
            "NEXT_CLASS": "navhide",
            "NEXT_LINK": "",
            "NEXT_END": ""
        }
        if prevnode:
            dict["PREV_CLASS"] = "navbut"
            dict["PREV_LINK"] = "<a href='%s'>" % prevnode.filename
            dict["PREV_END"] = "</a>"
        if nextnode:
            dict["NEXT_CLASS"] = "navbut"
            dict["NEXT_LINK"] = "<a href='%s'>" % nextnode.filename
            dict["NEXT_END"] = "</a>"
        return navigation_tmpl % dict
    
    def collect_pages(self, parent, dict):
        dict.append(parent)
        for node in parent.nodes:
            self.collect_pages(node, dict)
    
    def make_navigation(self):
        dict = [ None ]
        for node in self.nodes:
            self.collect_pages(node,dict)
        dict.append(None)
        for i in range(len(dict) - 2):
            dict[i+1].nav = self.nav_code(dict[i],dict[i+2])
    
    def write_node(self, node):
        self.save_html(node.filename, node.nav + self.header + node.head + node.text + node.nav)
        for n in node.nodes:
            self.write_node(n)
    
    def cut(self):
        self.make_nodes_tree()
        self.make_pages()
        self.name_pages()
        for node in self.nodes:
            self.append_toc(node)
        self.fix_links()
        self.make_navigation()
        # FIXME: fix image links
        # output one page version
        self.save_html(self.filename, self.doc)
        # output multiple pages version
        for node in self.nodes:
            self.write_node(node)


class Exporter:
    def __init__(self, lyxfile, basename, img_path):
        self.lyxfile = lyxfile
        self.lyxname = lyxfile[:]
        if self.lyxname.endswith(".lyx"):
            self.lyxname = self.lyxname[:-4]
        self.img_path = img_path
        self.basename = basename
    
    def retouch_lyx(self):
        return
        # FIXME: fix regexps, handle hyperref package, and other minor probs
        print "'%s' düzeltiliyor..." % self.lyxfile
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
    
    def export_pdf(self):
        print "'%s.pdf' oluşturuluyor..." % self.basename
        os.spawnlp(os.P_WAIT, "lyx", "lyx", "-e", "pdf2", self.lyxfile);
        shutil.move(self.lyxname + ".pdf", self.basename + ".pdf")
    
    def export_html(self):
        f = file("duzeltmeler.hva", "w")
        f.write(hevea_fixes)
        f.close()
        print "'%s.tex' oluşturuluyor..." % self.basename
        os.spawnlp(os.P_WAIT, "lyx", "lyx", "-e", "latex", self.lyxfile)
        print "'%s.html' oluşturuluyor..." % self.basename
        os.spawnlp(os.P_WAIT, "hevea", "hevea", "-fix", "duzeltmeler.hva",
            self.lyxname + ".tex", "-o", self.basename + ".html")
        c = Cutter(self.basename + ".html")
        c.img_path = self.img_path
        c.cut()
    
    def export(self):
        self.retouch_lyx()
        self.export_pdf()
        self.export_html()


def enter_dir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname, 0755)
        # FIXME: add to svn
    os.chdir(dirname)

def ensure_path(fname):
    if fname.find("/") != -1:
        t = fname.split("/")
        if not os.path.exists(t[0]):
            os.mkdir(t[0], 0755)

def svn_fetch(repo, filename):
    print "'%s' getiriliyor..." % (repo + filename)
    # init
    core.apr_initialize()
    pool = core.svn_pool_create(None)
    core.svn_config_ensure(None, pool)
    # client context for auth
    ctx = client.svn_client_ctx_t()
    provs = []
    provs.append(client.svn_client_get_simple_provider(pool))
    provs.append(client.svn_client_get_username_provider(pool))
    provs.append(client.svn_client_get_ssl_server_trust_file_provider(pool))
    provs.append(client.svn_client_get_ssl_client_cert_file_provider(pool))
    provs.append(client.svn_client_get_ssl_client_cert_pw_file_provider(pool))
    ctx.auth_baton = core.svn_auth_open(provs, pool)
    ctx.config = core.svn_config_get_config(None, pool)
    # fetch last revision
    rt = core.svn_opt_revision_t()
    rt.kind = core.svn_opt_revision_head
    # stream
    f = file(filename, "w")
    st = core.svn_stream_from_aprfile(f, pool)
    # get commit date
    de = client.svn_client_ls(repo + filename, rt, 0, ctx, pool)
    for a,b in de.iteritems():
        ret = time.strftime("%d/%m/%Y", time.gmtime(b.time / 1000000))
    # fetch
    client.svn_client_cat(st, repo + filename, rt, ctx, pool)
    # cleanup
    f.close()
    core.svn_pool_destroy(pool)
    core.apr_terminate()
    return ret

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

def usage():
    print "Kullanım: belgeyap.py <belgeşablonu>..."
    sys.exit(0)


if __name__ == "__main__":
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hf", ["help", "no-fetch"])
    except:
        usage()
    
    if not os.path.exists("/usr/bin/hevea"):
        print "Hata: Belgeleri HTML'e çevirebilmek için 'hevea' pakedini kurmalısınız."
        sys.exit(1)
    
    do_fetch = True

    for o, v in opts:
        if o in ("-h", "--help"):
            usage()
        if o in ("-f", "--no-fetch"):
            do_fetch = False
    
    for name in args:
        generate_doc(name, do_fetch)
    else:
        usage()
    
    generate_doc(sys.argv[1])
