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

grub_template = """default 0
timeout 10
splashimage (cd)/boot/grub/splash.xpm.gz

title=%(title)s
root (cd)
kernel (cd)/boot/%(kernel)s root=/dev/ram0 video=vesafb:nomtrr,pmipal,ywrap,1024x768-32@60 splash=silent,theme:pardus console=tty2 mudur=livecd,language:tr quiet
initrd (cd)/boot/%(initramfs)s

title=%(title-standart)s
root (cd)
kernel (cd)/boot/%(kernel)s root=/dev/ram0 video=vesafb:off mudur=livecd,language:tr quiet
initrd (cd)/boot/%(initramfs)s

title=%(title-safe)s
root (cd)
kernel (cd)/boot/%(kernel)s root=/dev/ram0 video=vesafb:off acpi=off apm=off nolapic noapic mudur=livecd,language:tr
initrd (cd)/boot/%(initramfs)s

"""

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

def generate_grub_conf(project, kernel, initramfs):
    print "Generating grub.conf files..."
    iso_dir = project.iso_dir()
    # FIXME: take name from /etc/pardus-release
    tr = {
        "suffix": "",
        "language": "Turkish",
        "title": "Pardus 1.1 Alfa N",
        "title-standart": "Pardus 1.1 Alfa 3 (Standard Ekran Modu)",
        "title-safe": "Pardus 1.1 Alfa 3 (Minimum Ayarlar)",
    }
    en = {
        "suffix": "-en",
        "language": "English",
        "title": "Pardus 1.1 Alfa N",
        "title-standart": "Pardus 1.1 Alfa 3 (Standard Graphics Mode)",
        "title-safe": "Pardus 1.1 Alfa 3 (Minimum Options)",
    }
    nl = {
        "suffix": "-nl",
        "language": "Nederlands",
        "title": "Pardus 1.1 Alfa N",
        "title-standart": "Pardus 1.1 Alfa 3 (Standaard Grafische Modus)",
        "title-safe": "Pardus 1.1 Alfa 3 (Minimale Opties)",
    }
    for lang in (tr, en, nl):
        lang["kernel"] = kernel
        lang["initramfs"] = initramfs
        path = os.path.join(iso_dir, "boot/grub", "menu" + lang["suffix"] + ".lst")
        f = file(path, "w")
        f.write(grub_template % lang)
        for lang2 in (tr, en, nl):
            if lang2["suffix"] != lang["suffix"]:
                f.write("title=%(language)s\nconfigfile (cd)/boot/grub/menu%(suffix)s.lst\n\n" % lang2)
        f.close()

def make_live_image(project):
    pass

def make_install_image(project):
    print "Preparing install image..."
    
    repo = project.get_repo()
    repo_dir = project.image_repo_dir(clean=True)
    image_file = project.image_file()
    
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
    chrun("/usr/bin/hav call-package System.Package.postInstall baselayout")
    chrun("/usr/bin/pisi configure-pending")
    chrun("/usr/bin/comar --stop")
    
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
    
    path = os.path.join(iso_dir, "boot")
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(iso_dir, "boot/grub")
    if not os.path.exists(path):
        os.makedirs(path)
    
    path = os.path.join(image_dir, "boot")
    kernel = ""
    initramfs = ""
    for name in os.listdir(path):
        if name.startswith("kernel") or name.startswith("initramfs"):
            if name.startswith("kernel"):
                kernel = name
            else:
                initramfs = name
            copy(os.path.join(path, name), "boot/" + name)
    path = os.path.join(image_dir, "boot/grub")
    for name in os.listdir(path):
        copy(os.path.join(path, name), "boot/grub/" + name)
    
    generate_grub_conf(project, kernel, initramfs)
    
    #FIXME: link install repo
    
    run('mkisofs -J -joliet-long -R -l -V "Pardus" -o "%s" -b boot/grub/stage2_eltorito -no-emul-boot -boot-load-size 4 -boot-info-table "%s"' % (
        iso_file,
        iso_dir,
    ))

def make(project):
    start = time.time()
    if project.media_type == "install":
        make_install_image(project)
        make_install_repo(project)
    else:
        make_live_image(project)
    make_iso(project)
    end = time.time()
    print "ISO is ready!"
    print "Total time is", end - start, "seconds."
