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
import subprocess
import stat
import sys

def run(cmd):
    print cmd
    os.system(cmd)

def chroot_comar(image_dir):
    if os.fork() == 0:
        os.chroot(image_dir)
        subprocess.call(["/usr/bin/comar"])
        sys.exit(0)

def make_live_image(project):
    pass

def make_install_image(project):
    print "Preparing install image..."
    
    repo = project.get_repo()
    repo_dir = project.image_repo_dir(clean=True)
    
    image_dir = project.image_dir()
    run('umount %s/proc' % image_dir)
    run('umount %s/sys' % image_dir)
    image_dir = project.image_dir(clean=True)
    
    yalideps = repo.full_deps("yali")
    repo.make_local_repo(repo_dir, yalideps)
    
    run('pisi --yes-all -D"%s" ar pardus-install %s' % (image_dir, repo_dir + "/pisi-index.xml.bz2"))
    run('pisi --yes-all --ignore-comar -D"%s" it yali' % image_dir)
    
    def chrun(cmd):
        run('chroot "%s" %s' % (image_dir, cmd))
    
    os.mknod("%s/dev/null" % image_dir, 0666 | stat.S_IFCHR, os.makedev(1, 3))
    os.mknod("%s/dev/console" % image_dir, 0666 | stat.S_IFCHR, os.makedev(5, 1))
    
    path = "%s/usr/share/baselayout/" % image_dir
    path2 = "%s/etc" % image_dir
    for name in os.listdir(path):
        run('cp -p "%s" "%s"' % (os.path.join(path, name), os.path.join(path2, name)))
    run('/bin/mount --bind /proc %s/proc' % image_dir)
    run('/bin/mount --bind /sys %s/sys' % image_dir)
    
    chrun("/sbin/ldconfig")
    chrun("/sbin/update-environment")
    chroot_comar(image_dir)
    chrun("/usr/bin/pisi configure-pending")
    
    run('umount %s/proc' % image_dir)
    run('umount %s/sys' % image_dir)
    
    run('mksquashfs "%s" image.iso' % image_dir)

def make_install_repo(project):
    print "Preparing installation repository..."
    
    repo = project.get_repo()
    repo_dir = project.install_repo_dir(clean=True)
    repo.make_local_repo(repo_dir, project.all_packages)

def make_iso(project):
    print "Preparing ISO..."
    
    iso_dir = project.iso_dir()
    # FIXME: copy kernel, boot image, release files and co into iso_dir
    run('mkisofs -J -joliet-long -R -l -V "Pardus" -o "Pardus.iso" -b boot/grub/stage2_eltorito -no-emul-boot -boot-load-size 4 -boot-info-table "%s"' % iso_dir)

def make(project):
    if project.media_type == "install":
        make_install_image(project)
        make_install_repo(project)
    else:
        make_live_image(project)
    make_iso(project)
