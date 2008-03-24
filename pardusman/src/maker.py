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
import sha
import tempfile
import stat
import sys
import time

from utility import xterm_title, waitBus

#
# Utilities
#

def run(cmd, ignore_error=False):
    print cmd
    ret = os.system(cmd)
    if ret and not ignore_error:
        print "%s returned %s" % (cmd, ret)
        sys.exit(1)

def chroot_comar(image_dir):
    if os.fork() == 0:
        # Workaround for creating ISO's on 2007 with PiSi 2.*
        # Create non-existing /var/db directory before running COMAR
        try:
            os.makedirs(os.path.join(image_dir, "var/db"), 0700)
        except OSError:
            pass
        os.chroot(image_dir)
        subprocess.call(["/sbin/start-stop-daemon", "--start", "-b", "--pidfile", "/var/run/comar.pid", "--make-pidfile", "--exec", "/usr/bin/comar"])
        sys.exit(0)
    waitBus("%s/var/run/comar.socket" % image_dir)

def get_exclude_list(project):
    exc = project.exclude_list()[:]
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
    xterm_title("Generating grub.conf files")
    
    image_dir = project.image_dir()
    iso_dir = project.iso_dir()
    
    dict = {}
    dict["kernel"] = kernel
    dict["initramfs"] = initramfs
    dict["title"] = project.title
    dict["exparams"] = project.exparams

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
        run('cp -P "%s" "%s"' % (src, os.path.join(iso_dir, dest)))
    
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

def squash_image(project):
    image_dir = project.image_dir()
    image_file = project.image_file()
    
    if not image_dir.endswith("/"):
        image_dir += "/"
    temp = tempfile.NamedTemporaryFile()
    f = file(temp.name, "w")
    f.write("\n".join(get_exclude_list(project)))
    f.close()
    run('mksquashfs "%s" "%s" -noappend -ef "%s"' % (image_dir, image_file, temp.name))

#
# Operations
#

def make_repos(project):
    print "Preparing image repo..."
    xterm_title("Preparing image repo")
    
    try:
        repo = project.get_repo()
        repo_dir = project.image_repo_dir(clean=True)
        if project.type == "install":
            imagedeps = repo.full_deps("yali")
        else:
            imagedeps = project.all_packages
        repo.make_local_repo(repo_dir, imagedeps)
        
        if project.type == "install":
            xterm_title("Preparing installination repo")
            print "Preparing installation repository..."
            
            repo_dir = project.install_repo_dir(clean=True)
            repo.make_local_repo(repo_dir, project.all_packages)
    except KeyboardInterrupt:
        print "Keyboard Interrupt: make_repo() cancelled."
        sys.exit(1)

def check_file(repo_dir, name, hash):
    path = os.path.join(repo_dir, name)
    if not os.path.exists(path):
        print "\nPackage missing: %s" % path
        return
    data = file(path).read()
    cur_hash = sha.sha(data).hexdigest()
    if cur_hash != hash:
        print "\nWrong hash: %s" % path

def check_repo_files(project):
    print "Checking image repo..."
    xterm_title("Checking image repo")

    try:
        repo = project.get_repo()
        repo_dir = project.image_repo_dir()
        if project.type == "install":
            imagedeps = repo.full_deps("yali")
        else:
            imagedeps = project.all_packages
        i = 0
        for name in imagedeps:
            i += 1
            sys.stdout.write("\r%-70.70s" % "Checking %d of %s packages" % (i, len(imagedeps)))
            sys.stdout.flush()
            pak = repo.packages[name]
            check_file(repo_dir, pak.uri, pak.sha1sum)
        sys.stdout.write("\n")
        
        if project.type == "install":
            repo_dir = project.install_repo_dir()
            i = 0
            for name in project.all_packages:
                i += 1
                sys.stdout.write("\r%-70.70s" % "Checking %d of %s packages" % (i, len(project.all_packages)))
                sys.stdout.flush()
                pak = repo.packages[name]
                check_file(repo_dir, pak.uri, pak.sha1sum)
        sys.stdout.write("\n")
    except KeyboardInterrupt:
        print "Keyboard Interrupt: check_repo() cancelled."
        sys.exit(1)

def make_image(project):
    print "Preparing install image..."
    xterm_title("Preparing install image")
   
    try:
        repo = project.get_repo()
        repo_dir = project.image_repo_dir()
        image_file = project.image_file()
        
        image_dir = project.image_dir()
        run('umount %s/proc' % image_dir, ignore_error=True)
        run('umount %s/sys' % image_dir, ignore_error=True)
        image_dir = project.image_dir(clean=True)
        
        run('pisi --yes-all -D"%s" ar pardus-install %s' % (image_dir, repo_dir + "/pisi-index.xml.bz2"))
        if project.type == "install":
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
        if project.type != "install":
            chrun("hav call User.Manager.addUser uid 1000 name pars realname Pardus groups users,wheel,disk,removable,power,pnp,pnpadmin,video,audio password pardus")
        chrun("/usr/bin/comar --stop")
        
        chrun("/sbin/update-modules")
        chrun("/sbin/depmod -a %s-%s" % (repo.packages["kernel"].version, repo.packages["kernel"].release))
        
        path1 = os.path.join(image_dir, "usr/share/baselayout/inittab.live")
        path2 = os.path.join(image_dir, "etc/inittab")
        os.unlink(path2)
        run('mv "%s" "%s"' % (path1, path2))
        
        file(os.path.join(image_dir, "etc/pardus-release"), "w").write("%s\n" % project.title)
        
        if project.type != "install" and "kdebase" in project.all_packages:
            setup_live_kdm(project)
        
        run('umount %s/proc' % image_dir)
        run('umount %s/sys' % image_dir)
    except KeyboardInterrupt:
        print "Keyboard Interrupt: make_image() cancelled."
        sys.exit(1)

def make_iso(project):
    print "Preparing ISO..."
    xterm_title("Preparing ISO")
    
    try:
        iso_dir = project.iso_dir(clean=True)
        iso_file = project.iso_file(clean=True)
        image_dir = project.image_dir()
        image_file = project.image_file()
        
        os.link(image_file, os.path.join(iso_dir, "pardus.img"))
        
        def copy(src, dest):
            run('cp -PR "%s" "%s"' % (src, os.path.join(iso_dir, dest)))
        
        if project.release_files:
            path = project.release_files
            for name in os.listdir(path):
                if name != ".svn":
                    copy(os.path.join(path, name), name)
        
        setup_grub(project)
        
        if project.type == "install":
            run('ln -s "%s" "%s"' % (project.install_repo_dir(), os.path.join(iso_dir, "repo")))
        
        run('mkisofs -f -J -joliet-long -R -l -V "Pardus" -o "%s" -b boot/grub/stage2_eltorito -no-emul-boot -boot-load-size 4 -boot-info-table "%s"' % (
            iso_file,
            iso_dir,
        ))
    except KeyboardInterrupt:
        print "Keyboard Interrupt: make_iso() cancelled."
        sys.exit(1)


def make(project):
    make_image(project)
    if project.type == "install":
        make_install_repo(project)
    make_iso(project)
    print "ISO is ready!"
    xterm_title("ISO is ready")
