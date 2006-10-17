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
import tempfile
import stat
import sys
import time

inittab_livecd = """# /etc/inittab:
#
# This file describes how the INIT process should set up
# the system in a certain run-level.

# Default runlevel.
id:3:initdefault:

# System initialization, mount local filesystems, etc.
si::sysinit:/sbin/mudur.py sysinit

# Further system initialization, brings up the boot runlevel.
rc::bootwait:/sbin/mudur.py boot

l0:0:wait:/sbin/mudur.py shutdown 
l1:S1:wait:/sbin/mudur.py single
l2:2:wait:/sbin/mudur.py nonetwork
l3:3:wait:/sbin/mudur.py default
l4:4:wait:/sbin/mudur.py default
l5:5:wait:/sbin/mudur.py default
l6:6:wait:/sbin/mudur.py reboot
#z6:6:respawn:/sbin/sulogin

c1:12345:respawn:/sbin/mingetty --noclear --autologin root tty1
c2:12345:respawn:/sbin/mingetty --noclear --autologin root tty2
c3:12345:respawn:/sbin/mingetty --noclear --autologin root tty3
c4:12345:respawn:/sbin/mingetty --noclear --autologin root tty4
c5:12345:respawn:/sbin/mingetty --noclear --autologin root tty5
c6:12345:respawn:/sbin/mingetty --noclear --autologin root tty6

# SERIAL CONSOLES
#s0:12345:respawn:/sbin/agetty 9600 ttyS0 vt100
#s1:12345:respawn:/sbin/agetty 9600 ttyS1 vt100

# What to do at the "Three Finger Salute".
ca:12345:ctrlaltdel:/sbin/shutdown -r now
"""

#
# Utilities
#

def run(cmd):
    print cmd
    os.system(cmd)

def chroot_comar(image_dir):
    if os.fork() == 0:
        os.chroot(image_dir)
        subprocess.call(["/usr/bin/comar"])
        sys.exit(0)
    #FIXME: lame, properly wait comar socket (inside chroot) here
    time.sleep(2)

def get_exclude_list(project):
    exc = project.exclude_list[:]
    image_dir = project.image_dir()
    path = image_dir + "/boot"
    for name in os.listdir(path):
        if name.startswith("kernel") or name.startswith("initramfs"):
            exc.append("boot/" + name)
    return exc

#
# Grub related stuff
#

def generate_grub_conf(project, kernel, initramfs):
    print "Generating grub.conf files..."
    image_dir = project.image_dir()
    iso_dir = project.iso_dir()
    
    dict = {}
    dict["kernel"] = kernel
    dict["initramfs"] = initramfs
    dict["title"] = "Pardus 16-10-2006"
    
    path = os.path.join(image_dir, "usr/share/grub/templates")
    dest = os.path.join(iso_dir, "boot/grub")
    for name in os.listdir(path):
        if name.startswith("menu"):
            data = file(os.path.join(path, name)).read()
            f = file(os.path.join(dest, name), "w")
            f.write(data % dict)
            f.close()

def setup_grub(project):
    image_dir = project.image_dir()
    iso_dir = project.iso_dir()
    kernel = ""
    initramfs = ""
    
    # Setup dir
    path = os.path.join(iso_dir, "boot/grub")
    if not os.path.exists(path):
        os.makedirs(path)
    
    def copy(src, dest):
        run('cp "%s" "%s"' % (src, os.path.join(iso_dir, dest)))
    
    # Copy the kernel and initramfs
    path = os.path.join(image_dir, "boot")
    for name in os.listdir(path):
        if name.startswith("kernel") or name.startswith("initramfs") or name.endswith(".bin"):
            if name.startswith("kernel"):
                kernel = name
            elif name.startswith("initramfs"):
                initramfs = name
            copy(os.path.join(path, name), "boot/" + name)
    
    # and the other files
    path = os.path.join(image_dir, "boot/grub")
    for name in os.listdir(path):
        copy(os.path.join(path, name), "boot/grub/" + name)
    
    # Generate the config file
    generate_grub_conf(project, kernel, initramfs)

#
# Image related stuff
#

def setup_live_kdm(project):
    image_dir = project.image_dir()
    path = os.path.join(image_dir, "etc/X11/kdm/kdmrc")
    lines = []
    for line in file(path):
        if line.startswith("#AutoLoginEnable"):
            lines.append("AutoLoginEnable=true\n")
        elif line.startswith("#AutoLoginUser"):
            lines.append("AutoLoginUser=pars\n")
        else:
            lines.append(line)
    file(path, "w").write("".join(lines))

def install_packages(project):
    image_dir = project.image_dir()
    path = os.path.join(image_dir, "var/lib/pisi/package")
    for name in project.all_packages:
        flag = True
        if os.path.exists(path):
            for avail in os.listdir(path):
                if avail.startswith(name) and avail[len(name)] == "-":
                    flag = False
        if flag:
            run('pisi --yes-all --ignore-comar --ignore-file-conflicts -D"%s" it %s' % (image_dir, name))

#
# Operations
#

def make_image(project):
    print "Preparing install image..."
    
    repo = project.get_repo()
    repo_dir = project.image_repo_dir(clean=True)
    image_file = project.image_file()
    
    image_dir = project.image_dir()
    run('umount %s/proc' % image_dir)
    run('umount %s/sys' % image_dir)
    image_dir = project.image_dir(clean=True)
    
    if project.media_type == "install":
        yalideps = repo.full_deps("yali")
    else:
        yalideps = project.all_packages
    repo.make_local_repo(repo_dir, yalideps)
    
    run('pisi --yes-all -D"%s" ar pardus-install %s' % (image_dir, repo_dir + "/pisi-index.xml.bz2"))
    if project.media_type == "install":
        run('pisi --yes-all --ignore-comar -D"%s" it yali' % image_dir)
    else:
        install_packages(project)
    
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
    chrun("/usr/bin/hav call-package System.Package.postInstall baselayout")
    chrun("/usr/bin/pisi configure-pending")
    
    chrun("hav call User.Manager.setUser uid 0 password pardus")
    if project.media_type != "install":
        chrun("hav call User.Manager.addUser uid 1000 name pars realname Pardus groups users,wheel,disk,removable,power,pnp,video,audio password pardus")
    chrun("/usr/bin/comar --stop")
    
    if project.media_type != "install":
        path = os.path.join(image_dir, "etc/inittab")
        file(path, "w").write(inittab_livecd)
        setup_live_kdm(project)
    
    run('umount %s/proc' % image_dir)
    run('umount %s/sys' % image_dir)
    
    if not image_dir.endswith("/"):
        image_dir += "/"
    temp = tempfile.NamedTemporaryFile()
    f = file(temp.name, "w")
    f.write("\n".join(get_exclude_list(project)))
    f.close()
    run('mksquashfs "%s" "%s" -noappend -ef "%s"' % (image_dir, image_file, temp.name))

def make_install_repo(project):
    print "Preparing installation repository..."
    
    repo = project.get_repo()
    repo_dir = project.install_repo_dir(clean=True)
    repo.make_local_repo(repo_dir, project.all_packages)

def make_iso(project):
    print "Preparing ISO..."
    
    iso_dir = project.iso_dir(clean=True)
    iso_file = project.iso_file(clean=True)
    image_dir = project.image_dir()
    image_file = project.image_file()
    
    os.link(image_file, os.path.join(iso_dir, "pardus.img"))
    
    def copy(src, dest):
        run('cp "%s" "%s"' % (src, os.path.join(iso_dir, dest)))
    
    path = project.release_files
    for name in os.listdir(path):
        if name != ".svn":
            copy(os.path.join(path, name), name)
    
    setup_grub(project)
    
    if project.media_type == "install":
        run('ln -s "%s" "%s"' % (project.install_repo_dir(), os.path.join(iso_dir, "repo")))
    
    run('mkisofs -f -J -joliet-long -R -l -V "Pardus" -o "%s" -b boot/grub/stage2_eltorito -no-emul-boot -boot-load-size 4 -boot-info-table "%s"' % (
        iso_file,
        iso_dir,
    ))

def make(project):
    start = time.time()
    make_image(project)
    if project.media_type == "install":
        make_install_repo(project)
    make_iso(project)
    end = time.time()
    print "ISO is ready!"
    print "Total time is", end - start, "seconds."
