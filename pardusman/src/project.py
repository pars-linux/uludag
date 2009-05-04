#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import piksemel

import packages

# no i18n yet
def _(x):
    return x

default_live_exclude_list = """
lib/rcscripts/
usr/include/
usr/lib/python2.5/lib-tk/
usr/lib/python2.5/idlelib/
usr/lib/python2.5/bsddb/test/
usr/lib/python2.5/lib-old/
usr/lib/python2.5/test/
usr/lib/klibc/include/
usr/qt/4/include/
usr/share/aclocal/
usr/share/doc/
usr/share/info/
usr/share/sip/
usr/share/man/
usr/share/groff/
usr/share/dict/
var/db/pisi/
var/cache/pisi/
var/tmp/pisi/
var/pisi/
tmp/pisi-root/
var/log/comar.log
var/log/pisi.log
root/.bash_history
"""

default_install_exclude_list = """
lib/rcscripts/
usr/include/
usr/lib/cups/
usr/lib/python2.5/lib-tk/
usr/lib/python2.5/idlelib/
usr/lib/python2.5/distutils/
usr/lib/python2.5/bsddb/test/
usr/lib/python2.5/lib-old/
usr/lib/python2.5/test/
usr/lib/klibc/include/
usr/qt/4/include/
usr/qt/4/mkspecs/
usr/qt/4/bin/
usr/qt/4/templates/
usr/share/aclocal/
usr/share/cups/
usr/share/doc/
usr/share/info/
usr/share/sip/
usr/share/man/
usr/share/groff/
usr/share/dict/
var/db/pisi/
var/lib/pisi/
var/cache/pisi/
var/tmp/pisi/
var/pisi/
tmp/pisi-root/
var/log/comar.log
var/log/pisi.log
root/.bash_history
"""

default_install_glob_excludes = (
    ( "usr/lib/python2.5/", "*.pyc" ),
    ( "usr/lib/python2.5/", "*.pyo" ),
    ( "usr/lib/python2.6/", "*.pyc" ),
    ( "usr/lib/python2.6/", "*.pyo" ),
    ( "usr/lib/pardus/", "*.pyc" ),
    ( "usr/lib/pardus/", "*.pyo" ),
    ( "usr/lib/", "*.a" ),
    ( "usr/lib/", "*.la" ),
    ( "lib/", "*.a" ),
    ( "lib/", "*.la" ),
    ( "var/db/comar/", "__db*" ),
    ( "var/db/comar/", "log.*" ),
)

default_live_glob_excludes = (
    ( "usr/lib/python2.5/", "*.pyc" ),
    ( "usr/lib/python2.5/", "*.pyo" ),
    ( "usr/lib/python2.6/", "*.pyc" ),
    ( "usr/lib/python2.6/", "*.pyo" ),
    ( "usr/lib/pardus/", "*.pyc" ),
    ( "usr/lib/pardus/", "*.pyo" ),
    ( "usr/lib/", "*.a" ),
    ( "usr/lib/", "*.la" ),
    ( "lib/", "*.a" ),
    ( "lib/", "*.la" ),
    ( "var/db/comar/", "__db*" ),
    ( "var/db/comar/", "log.*" ),
    ( "var/lib/pisi/index", "*" ),
    ( "var/lib/pisi/info", "*" ),
    ( "var/lib/pisi/package", "*" ),
)


class Project:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.title = None
        self.work_dir = None
        self.release_files = None
        self.repo_uri = None
        self.type = "install"
        self.media = "cd"
        self.selected_components = []
        self.selected_packages = []
        self.all_packages = []
        self.selected_languages = []
        self.default_language = None
        self.exparams = ''
        self.plugin_package = ''
    
    def open(self, filename):
        try:
            doc = piksemel.parse(filename)
        except OSError, e:
            if e.errno == 2:
                return _("Project file '%s' does not exists!" % filename)
            raise
        except piksemel.ParseError:
            return _("Not a Pardusman project file, invalid xml!")
        if doc.name() != "PardusmanProject":
            return _("Not a Pardusman project file")
        
        self.reset()
        
        self.title = doc.getTagData("Title")
        self.type = doc.getAttribute("type")
        self.media = doc.getAttribute("media")
        self.work_dir = doc.getTagData("WorkDir")
        self.release_files = doc.getTagData("ReleaseFiles")
        self.exparams = doc.getTagData("ExtraParameters")
        self.plugin_package = doc.getTagData("PluginPackage")
        
        paksel = doc.getTag("PackageSelection")
        if paksel:
            self.repo_uri = paksel.getAttribute("repo_uri")
            for tag in paksel.tags("SelectedComponent"):
                self.selected_components.append(tag.firstChild().data())
            for tag in paksel.tags("SelectedPackage"):
                self.selected_packages.append(tag.firstChild().data())
            for tag in paksel.tags("Package"):
                self.all_packages.append(tag.firstChild().data())

        langsel = doc.getTag("LanguageSelection")
        if langsel:
            self.default_language = langsel.getAttribute("default_language")
            for tag in langsel.tags("Language"):
                self.selected_languages.append(tag.firstChild().data())

            if self.default_language not in self.selected_languages:
                self.selected_languages.append(self.default_language)
        
        return None
    
    def save(self, filename):
        doc = piksemel.newDocument("PardusmanProject")
        doc.setAttribute("type", self.type)
        doc.setAttribute("media", str(self.media))
        if self.title:
            doc.insertTag("Title").insertData(self.title)
        if self.work_dir:
            doc.insertTag("WorkDir").insertData(self.work_dir)
        if self.release_files:
            doc.insertTag("ReleaseFiles").insertData(self.release_files)
        if self.exparams:
            doc.insertTag("ExtraParameters").insertData(self.exparams)
        if self.plugin_package:
            doc.insertTag("PluginPackage").insertData(self.plugin_package)
        if self.repo_uri:
            paks = doc.insertTag("PackageSelection")
            paks.setAttribute("repo_uri", self.repo_uri)
            self.selected_components.sort()
            for item in self.selected_components:
                paks.insertTag("SelectedComponent").insertData(item)
            self.selected_packages.sort()
            for item in self.selected_packages:
                paks.insertTag("SelectedPackage").insertData(item)
            self.all_packages.sort()
            for item in self.all_packages:
                paks.insertTag("Package").insertData(item)
        if self.default_language:
            langs = doc.insertTag("LanguageSelection")
            langs.setAttribute("default_language", self.default_language)
            self.selected_languages.sort()
            for item in self.selected_languages:
                langs.insertTag("Language").insertData(item)
        data = doc.toPrettyString()
        f = file(filename, "w")
        f.write(data)
        f.close()
    
    def exclude_list(self):
        import fnmatch
        
        def _glob_exclude(lst, excludes):
            image_dir = self.image_dir()
            for exc in excludes:
                path = os.path.join(image_dir, exc[0])
                for root, dirs, files in os.walk(path):
                    for name in files:
                        if fnmatch.fnmatch(name, exc[1]):
                            lst.append(os.path.join(root[len(image_dir)+1:], name))
        
        if self.type == "install":
            temp = default_install_exclude_list.split()
            _glob_exclude(temp, default_install_glob_excludes)
        else:
            temp = default_live_exclude_list.split()
            _glob_exclude(temp, default_live_glob_excludes)
        return temp
    
    def _get_dir(self, name, clean=False):
        dirname = os.path.join(self.work_dir, name)
        if os.path.exists(dirname):
            if clean:
                os.system('rm -rf "%s"' % dirname)
                os.makedirs(dirname)
        else:
            os.makedirs(dirname)
        return dirname
    
    def get_repo(self, console=None, update_repo=False):
        cache_dir = self._get_dir("repo_cache")
        repo = packages.Repository(self.repo_uri, cache_dir)
        repo.parse_index(console, update_repo)
        self.find_all_packages(repo)
        return repo
    
    def find_all_packages(self, repo):
        packages = []
        def collect(name):
            p = repo.packages[name]
            if name in packages:
                return
            packages.append(name)
            for dep in p.depends:
                collect(dep)
        for component in self.selected_components:
            for package in repo.components[component]:
                collect(package)

        for package in self.selected_packages:
            collect(package)
        packages.sort()
        self.all_packages = packages
    
    def image_repo_dir(self, clean=False):
        return self._get_dir("image_repo", clean)
    
    def image_dir(self, clean=False):
        return self._get_dir("image", clean)
    
    def image_file(self):
        return os.path.join(self.work_dir, "pardus.img")
    
    def install_repo_dir(self, clean=False):
        return self._get_dir("install_repo", clean)
    
    def iso_dir(self, clean=False):
        return self._get_dir("iso", clean)
    
    def iso_file(self, clean=True):
        path = os.path.join(self.work_dir, "%s.iso" % self.title.replace(" ", "_"))
        if clean and os.path.exists(path):
            os.unlink(path)
        return path
