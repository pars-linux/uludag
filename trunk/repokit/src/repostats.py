#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import sys
import os
import codecs
import re
import getopt
import glob
import zipfile

import gettext
__trans = gettext.translation('repokit', fallback=True)
_ = __trans.ugettext

from svn import core, client

import piksemel

sys.path.append('.')
import pisi.specfile
import pisi.uri
import pisi.metadata
from pisi.cli import printu
from pisi.util import filter_latest_packages

# Main HTML template

html_header = """
<html><head>
    <title>%(title)s</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link href="%(root)sstil.css" rel="stylesheet" type="text/css">
</head><body>
<div id='header-bugzilla'>
</div>

<div class='menu'>
<a href='%(root)sindex.html'>%(menu1)s</a>
 | <a href='%(root)ssources.html'>%(menu2)s</a>
 | <a href='%(root)sbinaries.html'>%(menu3)s</a>
 | <a href='%(root)spackagers.html'>%(menu4)s</a>
</div>

<h1 align='center'>%(title)s</h1>

<div class='content'>
%(content)s
</div>

</body></html>
"""

css_template = """
body {
    margin-left:0;
    margin-top:0;
    margin-right:0;
    background-image:url('http://www.pardus.org.tr/styles/images/HeadTile.png');
    background-repeat:repeat-x;
    background-color: #FFF;
}

#header-bugzilla {
    background-image:url('http://www.pardus.org.tr/styles/images/HeadLogo.png');
    background-repeat:no-repeat;
    background-position: 0px 0px;
    height:119px;
    padding-bottom:5px;
}

a {
    color: #F55400;
    text-decoration: none;
}

a:hover {
    color: #444;
    background-color:#EEE;
}

.menu {
    padding-left: 1em;
    padding-top: 3px;
    padding-bottom: 3px;
    border-bottom: 1px solid #CCC;
    border-top: 1px solid #CCC;
}

.content {
    margin: 0.5em;
}
"""


def svn_uri(path):
    # init
    core.apr_initialize()
    pool = core.svn_pool_create(None)
    core.svn_config_ensure(None, pool)
    # get repo uri
    uri = client.svn_client_url_from_path(path, pool)
    # cleanup
    core.svn_pool_destroy(pool)
    core.apr_terminate()
    return uri


def find_pspecs(folder):
    paks = []
    for root, dirs, files in os.walk(folder):
        if "pspec.xml" in files:
            paks.append(root)
        # dont walk into the versioned stuff
        if ".svn" in dirs:
            dirs.remove(".svn")
    return paks

def write_html(filename, title, content):
    f = codecs.open(filename, "w", "utf-8")
    root = "./"
    if len(filename.split("/")) > 2:
        root = "../"
    dict = {
        "title": title,
        "content": content,
        "root": root,
        "menu1": _("Information"),
        "menu2": _("Source Packages"),
        "menu3": _("Binary Packages"),
        "menu4": _("Packagers")
    }
    f.write(html_header % dict)
    f.close()

def make_table(elements, titles=None):
    def make_row(element):
        return "<td>%s" % "<td>".join(map(str, element))
    
    title_html = ""
    if titles:
        title_html = """
            <thead><tr><th>%s</tr></thead>
        """ % "<th>".join(titles)
    
    html = """
        <table>%s<tbody>
        <tr>%s
        </tbody></table>
    """ % (title_html, "<tr>".join(map(make_row, elements)))
    
    return html

def make_url(name, path="./"):
    if not path.endswith("/"):
        path += "/"
    return "<a href='%s%s.html'>%s</a>" % (path, name, name)

def mangle_email(email):
    return re.sub("@", " [at] ", email)


class Histogram:
    def __init__(self):
        self.list = {}
    
    def add(self, name, value=None):
        if value:
            self.list[name] = value
        else:
            self.list[name] = self.list.get(name, 0) + 1
    
    def note(self, name):
        if not self.list.has_key(name):
            self.list[name] = 0
    
    def get_list(self, max=0):
        items = self.list.items()
        items.sort(key=lambda x: x[1], reverse=True)
        if max != 0:
            return items[:max]
        else:
            return items


# Dictionary of all source packages keyed by the source name
sources = {}

# Dictionary of all binary packages keyed by the package name
packages = {}

# Dictionary of all packagers keyed by the packager name
packagers = {}

# Dictionary of missing depended binary packages keyed by the package name
missing = {}

# List of all repository problems
errors = []


class Missing:
    def __init__(self, name):
        missing[name] = self
        self.name = name
        self.revBuildDeps = []
        self.revRuntimeDeps = []


class Package:
    def __init__(self, source, pakspec):
        name = pakspec.name
        if packages.has_key(name):
            errors.append(_("Duplicate binary packages:\n%s\n%s\n") % (
                source.name, packages[name].source.name))
            return
        packages[name] = self
        self.name = name
        self.source = source
        self.pakspec = pakspec
        self.revBuildDeps = []
        self.revRuntimeDeps = []
        self.installedSize = 0
        self.size = 0
    
    def markDeps(self):
        # mark reverse build dependencies
        for d in self.source.spec.source.buildDependencies:
            p = d.package
            if packages.has_key(p):
                packages[p].revBuildDeps.append(self.name)
            else:
                if not missing.has_key(p):
                    Missing(p)
                missing[p].revBuildDeps.append(self.name)
        # mark reverse runtime dependencies
        for d in self.pakspec.packageDependencies:
            p = d.package
            if packages.has_key(p):
                packages[p].revRuntimeDeps.append(self.name)
            else:
                if not missing.has_key(p):
                    Missing(p)
                missing[p].revRuntimeDeps.append(self.name)
    
    def report_html(self):
        source = self.source.spec.source
        bDeps = map(lambda x: "<a href='./%s.html'>%s</a>" % (x, x),
            (map(lambda x: x.package, source.buildDependencies)))
        rDeps = map(lambda x: "<a href='./%s.html'>%s</a>" % (x, x),
            (map(lambda x: x.package, self.pakspec.packageDependencies)))
        rbDeps = map(lambda x: "<a href='./%s.html'>%s</a>" % (x, x), self.revBuildDeps)
        rrDeps = map(lambda x: "<a href='./%s.html'>%s</a>" % (x, x), self.revRuntimeDeps)
        
        sizehtml = ""
        if self.size > 0:
            sizehtml = "<p>%s: %s<br>%s: %s</p>" % (
                _("Package size"), self.size,
                _("Installed size"), self.installedSize,
            )
        
        html = """
            <h3>%s <em>%s</em></h3>
            
            %s
            
            <p>%s: %s</p>
            
            <h3>%s</h3>
            <p>%s</p>
            
            <h3>%s</h3>
            <p>%s</p>
            
            <h3>%s</h3>
            <p>%s</p>
            
            <h3>%s</h3>
            <p>%s</p>
        """ % (
            self.name,
            self.source.spec.getSourceVersion(),
            sizehtml,
            _("Source package"),
            make_url(source.name, "../source/"),
            _("Build dependencies"),
            ", ".join(bDeps),
            _("Runtime dependencies"),
            ", ".join(rDeps),
            _("Required by (for building)"),
            ", ".join(rbDeps),
            _("Required by (for runtime)"),
            ", ".join(rrDeps),
        )
        
        write_html("paksite/binary/%s.html" % self.name, self.name, html)


class Source:
    def __init__(self, path, spec):
        name = spec.source.name
        if sources.has_key(name):
            errors.append(_("Duplicate source packages:\n%s\n%s\n") % (
                path, sources[name].path))
            return
        sources[name] = self
        self.spec = spec
        self.name = name
        self.path = path
        self.uri = svn_uri(path)
        for p in spec.packages:
            Package(self, p)
    
    def report_html(self):
        source = self.spec.source
        paks = map(lambda x: "<a href='../binary/%s.html'>%s</a>" % (x, x),
            (map(lambda x: x.name, self.spec.packages)))
        histdata = map(lambda x: (x.release, x.date, x.version, make_url(x.name, "../packager/"), x.comment), self.spec.history)
        ptch = map(lambda x: "<a href='%s/files/%s'>%s</a>" % (self.uri,
            x.filename, x.filename), source.patches)
        
        titles = _("Release"), _("Release date"), _("Version"), _("Updater"), _("Comment")
        hist = make_table(histdata, titles)
        
        html = """
            <h3>%s <em>%s</em></h3>
            <p>%s</p>
            <p><a href='%s'>%s</a></p>
            <p>%s: %s</p>
            <h3>%s</h3>
            <p><a href="%s">%s</a></p>
            <p><a href="http://bugs.pardus.org.tr/buglist.cgi?product=Paketler&component=%s&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED">%s</a></p>
            
            <h3>%s</h3>
            <p>%s</p>
            
            <h3>%s</h3>
            %s
            
            <h3>%s</h3>
            %s
        """ % (
            self.name,
            self.spec.getSourceVersion(),
            source.summary,
            source.homepage,
            source.homepage,
            _("License"),
            ", ".join(source.license),
            _("Actions"),
            self.uri,
            _("Build files"),
            self.name,
            _("Bug reports"),
            _("Binary packages"),
            "<br>".join(paks),
            _("Release history"),
            "".join(hist),
            _("Patches"),
            "<br>".join(ptch),
        )
        
        write_html("paksite/source/%s.html" % self.name, self.name, html)


class Packager:
    def __init__(self, spec, update=None):
        if update:
            name = update.name
            email = update.email
        else:
            name = spec.source.packager.name
            email = spec.source.packager.email
        
        if not packagers.has_key(name):
            self.sources = []
            self.updates = []
            self.name = name
            self.email = email
            packagers[name] = self
        
        if update:
            packagers[name].updates.append((spec.source.name, update.release, update.comment))
        else:
            packagers[name].sources.append(spec.source.name)
            for update in spec.history:
                Packager(spec, update)
    
    def report_html(self):
        srcs = map(lambda x: ("<a href='../source/%s.html'>%s</a>" % (x, x), ), self.sources)
        srcs.sort()
        upds = map(lambda x: (u"<b><a href='../source/%s.html'>%s</a> (%s)</b><br>%s<br>" % (
            x[0], x[0], x[1], x[2]), ), self.updates)
        
        html = """
            <p>%s: %s (%s)</p>
        """ % (_("Packager"), self.name, mangle_email(self.email))
        
        html += """
            <div class='statstat'>
            <h3>%s</h3><p>
            %s
            </p></div>
        """ % (_("Maintained packages:"), make_table(srcs))
        
        html += """
            <div class='statstat'>
            <h3>%s</h3><p>
            %s
            </p></div>
        """ % (_("Package updates:"), make_table(upds))
        
        write_html("paksite/packager/%s.html" % self.name, self.name, html)


class Repository:
    def __init__(self, path):
        self.path = path
        self.nr_sources = 0
        self.nr_packages = 0
        self.nr_patches = 0
        self.people = Histogram()
        self.licenses = Histogram()
        self.mostpatched = Histogram()
        self.longpy = Histogram()
        self.cscripts = Histogram()
        self.total_installed_size = 0
        self.total_size = 0
        self.installed_sizes = {}
    
    def processPspec(self, path, spec):
        # new classes
        Packager(spec)
        Source(path, spec)
        # update global stats
        self.nr_sources += 1
        self.nr_packages += len(spec.packages)
        self.nr_patches += len(spec.source.patches)
        # update top fives
        self.people.add(spec.source.packager.name)
        for u in spec.history:
            self.people.note(u.name)
        for p in spec.packages:
            for cs in p.providesComar:
                self.cscripts.add(cs.om)
        for L in spec.source.license:
            self.licenses.add(L)
        self.mostpatched.add(spec.source.name, len(spec.source.patches))
        try:
            f = file(os.path.join(path, "actions.py"))
            L = len(f.readlines())
            self.longpy.add(spec.source.name, L)
            f.close()
        except:
            pass
    
    def scan(self):
        for pak in find_pspecs(self.path):
            spec = pisi.specfile.SpecFile()
            try:
                spec.read(os.path.join(pak, "pspec.xml"))
            except Exception, inst:
                errors.append(_("Cannot parse '%s':\n%s\n") % (pak, inst.args[0]))
                continue
            self.processPspec(pak, spec)
        for p in packages.values():
            p.markDeps()
    
    def processPisi(self, path):
        zip = zipfile.ZipFile(path, "r")
        
        size = os.stat(path).st_size
        self.total_size += size
        
        doc = piksemel.parseString(zip.read("metadata.xml"))
        p = doc.getTag("Package")
        name = p.getTagData("Name")
        inst_size = int(p.getTagData("InstalledSize"))
        self.total_installed_size += inst_size
        
        doc = piksemel.parseString(zip.read("files.xml"))
        for item in doc.tags("File"):
            tname = item.getTagData("Type")
            sz = item.getTagData("Size")
            try:
                sz = int(sz)
            except:
                sz = 0
            if self.installed_sizes.has_key(tname):
                self.installed_sizes[tname] += sz
            else:
                self.installed_sizes[tname] = sz
        
        pak = packages.get(name, None)
        if not pak:
            return
        
        pak.size = size
        pak.installedSize = inst_size
    
    def scan_bins(self, binpath):
        binpaks = filter_latest_packages(glob.glob(binpath + "/*.pisi"))
        for pak in binpaks:
            self.processPisi(pak)
    
    def report_html(self):
        table = (
            (_("Number of source packages"), self.nr_sources),
            (_("Number of binary packages"), self.nr_packages),
            (_("Number of patches"), self.nr_patches),
            (_("Number of packagers"), len(self.people.list)),
        )
        if self.total_installed_size > 0:
            table += (
                (_("Archived size of packages"), self.total_size),
                (_("Installed size of packages"), self.total_installed_size),
            )
        
        html = make_table(table)
        
        html += """
            <div class='statstat'>
            <h3>%s</h3><p>
            %s
            </p></div>
        """ % (
            _("Most patched:"),
            make_table(map(lambda x: (make_url(x[0], "./source/"), x[1]), self.mostpatched.get_list(5)))
        )
        
        html += """
            <div class='statstat'>
            <h3>%s</h3><p>
            %s
            </p></div>
        """ % (
            _("Longest build scripts:"),
            make_table(map(lambda x: (make_url(x[0], "./source/"), x[1]), self.longpy.get_list(5)))
        )
        
        if self.total_installed_size > 0:
            html += """
                <h3>%s</h3><p>
                %s
                </p></div>
            """ % (
                _("Total file sizes by file type:"),
                make_table(self.installed_sizes.items())
            )
        
        write_html("paksite/index.html", _("Information"), html)
        
        titles = (
            "<a href='packagers_by_name.html'>%s</a>" % _("Packager"),
            "<a href='packagers.html'>%s</a>" % _("Package count")
        )
        
        people = self.people.get_list()
        people = map(lambda x: ("<a href='./packager/%s.html'>%s</a>" % (x[0], x[0]), x[1]), people)
        write_html("paksite/packagers.html", _("Packagers (by package count)"), make_table(people, titles))
        
        people.sort(key=lambda x: x[0])
        write_html("paksite/packagers_by_name.html", _("Packagers (by name)"), make_table(people, titles))
        
        titles = _("Package name"), _("Version"), _("Summary")
        
        srclist = map(lambda x: (make_url(x.name, "source/"), x.spec.getSourceVersion(), x.spec.source.summary), sources.values())
        srclist.sort(key=lambda x: x[0])
        html = make_table(srclist, titles)
        write_html("paksite/sources.html", _("Source Packages"), html)
        
        binlist = map(lambda x: (make_url(x.name, "binary/"), x.source.spec.getSourceVersion(), x.source.spec.source.summary), packages.values())
        binlist.sort(key=lambda x: x[0])
        html = make_table(binlist, titles)
        write_html("paksite/binaries.html", _("Binary Packages"), html)


# command line driver

def usage():
    printu(_("Usage: repostats.py [OPTIONS] source-repo-path [binary-repo-path]\n"))
    printu("  -t, --test-only:    %s" % _("Dont generate the web site.\n"))
    sys.exit(0)

def main(args):
    try:
        opts, args = getopt.gnu_getopt(args, "ht", ["help", "test-only"])
    except:
        usage()
    
    if args == []:
        usage()
    
    do_web = True
    
    for o, v in opts:
        if o in ("-h", "--help"):
            usage()
        if o in ("-t", "--test-only"):
            do_web = False
    
    repo = Repository(args[0])
    printu(_("Scanning source repository...\n"))
    repo.scan()
    
    if len(args) > 1:
        printu(_("Scanning binary packages...\n"))
        repo.scan_bins(args[1])
    
    if do_web:
        if not os.path.exists("paksite/packager"):
            os.makedirs("paksite/packager")
        if not os.path.exists("paksite/binary"):
            os.makedirs("paksite/binary")
        if not os.path.exists("paksite/source"):
            os.makedirs("paksite/source")
        
        file("paksite/stil.css", "w").write(css_template)
        
        repo.report_html()
        for p in packagers.values():
            p.report_html()
        for p in packages.values():
            p.report_html()
        for p in sources.values():
            p.report_html()

if __name__ == "__main__":
    main(sys.argv[1:])
