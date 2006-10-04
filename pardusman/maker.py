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

def run(cmd):
    print cmd
    os.system(cmd)

def make_live_image(project):
    pass

def make_install_image(project):
    print "Preparing install image..."
    
    repo = project.get_repo()
    repo_dir = project.image_repo_dir()
    image_dir = project.image_dir()
    yalideps = repo.full_deps("yali")
    repo.make_local_repo(repo_dir, yalideps)
    
    run('pisi --yes-all -D"%s" ar pardus-install %s' % (image_dir, repo_dir + "/pisi-index.xml.bz2"))
    run('pisi --yes-all --ignore-comar -D"%s" it yali' % image_dir)
    
    # FIXME: create ld.so.conf, passwd, etc
    run('chroot "%d" ldconfig' % image_dir)
    run('chroot "%d" comar' % image_dir)
    run('chroot "%d" pisi configure-pending' % image_dir)
    
    # FIXME: make squashfs

def make_install_repo(project):
    print "Preparing installation repository..."
    
    repo = project.get_repo()
    repo_dir = project.install_repo_dir()
    repo.make_local_repo(repo_dir, project.all_packages)

def make_iso(project):
    print "Preparing ISO..."
    
    iso_dir = project.iso_dir()
    # FIXME: copy kernel, boot image, release files and co into iso_dir
    run('mkisofs -J -joliet-long -R -l -V "Pardus" -o "Pardus.iso" -b boot/grub/stage2_eltorito -no-emul-boot -boot-load-size 4 -boot-info-table "%s"' % iso_dir)

def make(project):
    if project.type == "install":
        make_install_image(project)
        make_install_repo(project)
    else:
        make_live_image(project)
    make_iso(project)
