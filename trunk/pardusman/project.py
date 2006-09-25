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


class Project:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.work_dir = None
        self.release_files = None
        self.repo_uri = None
        self.media_type = "install"
        self.media_size = 700 * 1024 * 1024
        self.selected_components = []
        self.selected_packages = []
        self.all_packages = []
    
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
        
        self.media_type = doc.getAttribute("type")
        self.media_size = doc.getAttribute("size")
        self.work_dir = doc.getTagData("WorkDir")
        self.release_files = doc.getTagData("ReleaseFiles")
        
        paksel = doc.getTag("PackageSelection")
        if paksel:
            self.repo_uri = paksel.getAttribute("repo_uri")
            for tag in paksel.tags("SelectedComponent"):
                self.selected_components.append(tag.firstChild().data())
            for tag in paksel.tags("SelectedPackage"):
                self.selected_packages.append(tag.firstChild().data())
            for tag in paksel.tags("Package"):
                self.all_packages.append(tag.firstChild().data())
        
        return None
    
    def save(self, filename):
        doc = piksemel.newDocument("PardusmanProject")
        doc.setAttribute("type", self.media_type)
        doc.setAttribute("size", str(self.media_size))
        if self.work_dir:
            doc.insertTag("WorkDir").insertData(self.work_dir)
        if self.release_files:
            doc.insertTag("ReleaseFiles").insertData(self.release_files)
        if self.repo_uri:
            paks = doc.insertTag("PackageSelection")
            paks.setAttribute("repo_uri", self.repo_uri)
            for item in self.selected_components:
                paks.insertTag("SelectedComponent").insertData(item)
            for item in self.selected_packages:
                paks.insertTag("SelectedPackage").insertData(item)
            for item in self.all_packages:
                paks.insertTag("Package").insertData(item)
        data = doc.toPrettyString()
        f = file(filename, "w")
        f.write(data)
        f.close()
    
    def _get_dir(self, name):
        dirname = os.path.join(self.work_dir, name)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        return dirname
    
    def get_repo(self, console):
        cache_dir = self._get_dir("repo_cache")
        repo = packages.Repository(self.repo_uri, cache_dir)
        repo.parse_index(console)
        return repo
    
    def make(self, console):
        console.state("\n==> Preparing distribution media\n")
        image_dir = self._get_dir("image_dir")
        
        repo = self.get_repo(console)
        print repo.make_index(["comar"])
        return
        
        console.state("Installing boot image packages...")
        if self.media_type == "install":
            paks = "yali"
        else:
            paks = " ".join(self.all_packages)
        console.run("pisi -D%s install %s" % (image_dir, paks))
        
        console.state("Configuring boot image packages...")
        #FIXME: chroot comar, and do the config
        
        console.state("Squashing boot image...")
        #FIXME: call mksquashfs
        
        console.state("Preparing cd contents...")
        #FIXME: copy release files, boot image, kernel
        
        if self.media_type == "install":
            console.state("Preparing installation packages...")
            #FIXME: copy packages into repo/ and generate index
        
        console.state("Making ISO image...")
        #FIXME: mkisofs, grub
        
        console.state("Finished succesfully!")


"""
        repodir = os.path.join(self.workdir, "repo") 
        os.mkdir(repodir)
        for path in packagelist:
            os.link(path, os.path.join(repodir, os.path.basename(path)))

        shutil.copytree(os.path.join(imgdir, "boot"), os.path.join(self.workdir, "boot"), True)

        ret = self.run('mkisofs -J -joliet-long -R -l -V "%s" -o "%s" -b boot/grub/stage2_eltorito -no-emul-boot -boot-load-size 4 -boot-info-table "%s"' %
            (name, os.path.join(self.tmpdir, "%s.iso" % name), self.workdir))

    def updateStatus(self):
        if self.pak_selection and len(self.pak_selection[2]) > 0:
            self.paklabel.setText(_("(%d packages, %s size, %s installed)") % 
                (len(self.pak_selection[2]), utility.size_fmt(self.pak_size), utility.size_fmt(self.pak_inst_size)))
        else:
            self.paklabel.setText(_("(no packages selected yet)"))        
"""
