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
import shutil


class ISO:
    def __init__(self, console, tmpdir):
        self.run = console.run
        self.state = console.state
        self.tmpdir = tmpdir
        self.workdir = os.path.join(tmpdir, "pardusman_cd_work_dir")
        if os.path.exists(self.workdir):
            os.system("rm -rf %s" % self.workdir)
        try:
            os.makedirs(self.tmpdir)
        except:
            pass
    
    def setup_contents(self, contentdir):
        self.state("Copying media content...")
        shutil.copytree(contentdir, self.workdir)
    
    def setup_cdroot(self, cdroot):
        self.state("Copying boot image...")
        os.link(cdroot, os.path.join(self.workdir, "pardus"))
    
    def setup_packages(self, packagelist):
        self.state("Copying packages...")
        repodir = os.path.join(self.workdir, "repo") 
        os.mkdir(repodir)
        for path in packagelist:
            os.link(path, os.path.join(repodir, os.path.basename(path)))
    
    def setup_boot(self, ):
        pass
    
    def make(self, name):
        self.state("Making the ISO...")
        self.run('mkisofs -J -joliet-long -R -l -V "%s" -o "%s" -b boot/grub/stage2_eltorito -no-emul-boot -boot-load-size 4 -boot-info-table %s' %
            (name, os.path.join(self.tmpdir, "%s.iso" % name), self.workdir))
