#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import commands

#DEPENDS: syslinux package
exclude_list = ["mnt/*", "tmp/*", "proc/*", "sys/*", "media/*"]

include_list = ["/bin","/boot","/dev","/lib","/proc", "/sys", "/lost+found", "/media", "/mnt", "/opt", "/root", "/sbin", "/tmp", "/usr", "/var", "/swap"]


def run(cmd, ignore_error=False):
    print cmd
    ret = os.system(cmd)
    if ret and not ignore_error:
        print "%s returned %s" % (cmd, ret)
        sys.exit(1)




def generate_configs(cache_dir=None):

    ''' Files required by the livecd to perform Default login as pars, inittab, PolicyKit'''

    ROOT = os.path.join(cache_dir,"ROOT")

    run("rm -rf %s" %ROOT, True)
    run("mkdir %s" %ROOT, True)

    run("cp -Rp /etc %s" %ROOT)

    run("cp conf_files/inittab conf_files/fstab %s/etc" %ROOT)
    run("cp conf_files/kdmrc %s/etc/X11/kdm/kdmrc" %ROOT)
    run("cp conf_files/PolicyKit.conf %s/etc/PolicyKit/PolicyKit.conf" %ROOT)
    run("mkdir -p %s/home" %ROOT)


    f = open("exclude.list","w")
    f.write("\n".join(exclude_list))
    f.close()

    run("/sbin/adduser pars")

    run("cp -Rp /home/pars %s/home/" %ROOT)

    user_list = []


    #Remove additional users and keep only pars, which is the default user
    user_re = re.compile("/home/([a-zA-Z0-9]+):/bin/bash")
    passwd_fd = open("/etc/passwd","r")
    passwd_write_fd = open(os.path.join(cache_dir,"ROOT/etc/passwd"),"w+")

    shadow_fd = open("/etc/shadow","r")
    shadow_write_fd = open(os.path.join(cache_dir,"ROOT/etc/shadow"),"w+")

    for entry in passwd_fd.readlines():
        match = user_re.findall(entry)
        if len(match) == 1:
            if match[0] == "pars":
                passwd_write_fd.write(entry)
            else:
                user_list.insert(0,match[0])
        else:
                passwd_write_fd.write(entry)


    passwd_write_fd.close()
    passwd_fd.close()


    shadow_re = re.compile("^%s:" % "|".join(user_list))

    for entry in shadow_fd.readlines():
        match = shadow_re.findall(entry)
        if len(match) == 0:
            shadow_write_fd.write(entry)

    shadow_write_fd.close()
    shadow_fd.close()

    run("/sbin/deluser pars -r")

    run("/bin/chown root.root %s" %os.path.join(cache_dir,"ROOT/etc/shadow"))
    run("/bin/chown root.root %s" %os.path.join(cache_dir,"ROOT/etc/passwd"))




def build_squash(cache_dir=None):
    '''
	Build squashfs image of root filesystem to be used as pardus.img
    '''
    run("/usr/bin/mksquashfs %s %s/* %s/pardus.img -ef exclude.list -noappend -wildcards" %(" ".join(include_list),os.path.join(cache_dir,"ROOT"),cache_dir))


def build_iso(cache_dir):


    iso_dir = os.path.join(cache_dir,"iso_dir")
    iso_file = os.path.join(cache_dir,"pardus.iso")

    def copy(src, dest):
        run('cp -P "%s" "%s"' % (src, os.path.join(iso_dir, dest)))

    path = os.path.join(cache_dir, "iso_dir/boot/isolinux")
    if not os.path.exists(path):
        os.makedirs(path)
	
    #Copy kernel and initramfs
    for name in os.listdir("/boot"):
        if name.startswith("kernel") or name.startswith("initramfs") or name.endswith(".bin"):
            if name.startswith("kernel"):
                copy(os.path.join("/boot",name), "boot/kernel")

    run("cp /etc/initramfs.conf /tmp/initrd.config")
    f=open("/etc/initramfs.conf","w+")
    f.write("liveroot=LABEL=PardusLiveImage\n")
    f.close()
    
    run("/sbin/mkinitramfs -o /tmp/initrd")
    run("cp /tmp/initrd.config /etc/initramfs.conf")

    for name in os.listdir("/tmp/initrd"):
            if name.startswith("initramfs"):
                  copy(os.path.join("/tmp/initrd/",name), "boot/initrd")



    tmplpath = os.path.join("/usr/share/gfxtheme/pardus/boot")

    for name in os.listdir(tmplpath):
        if name != "gfxboot.cfg":
            copy(os.path.join(tmplpath, name), "boot/isolinux")


    generate_isolinux_conf(cache_dir)



    dest = "boot/isolinux"

    copy(os.path.join("/usr/lib/syslinux/isolinux.bin"), "%s/isolinux.bin" % dest)
    copy(os.path.join("/usr/lib/syslinux/hdt.c32"), dest)
    copy(os.path.join("/usr/lib/syslinux/gfxboot.com"), dest)
    copy(os.path.join("/usr/share/misc/pci.ids"), dest)
    copy(os.path.join("/lib/modules/%s/modules.pcimap" %commands.getoutput("uname -r")), dest)
    copy(os.path.join("/boot/memtest"), "boot")



    os.link(os.path.join(cache_dir,"pardus.img"), os.path.join(iso_dir,"pardus.img"))
    run('mkisofs -f -J -joliet-long -R -l -V "PardusLiveImage" -o "%s" -b boot/isolinux/isolinux.bin -c boot/isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table "%s"' % (iso_file, iso_dir,))



def generate_isolinux_conf(cache_dir):
   ''' 
       Create isolinux configs
   '''

    #TODO: Change all hard coding to custom 
    dict = {}
    dict["title"] = "Pardus Live (Install2Live)"
    dict["exparams"] = '' #project.extra_params or ''
    #dict["rescue_template"] = ""

    image_dir = "/"
    iso_dir = os.path.join(cache_dir,"iso_dir")


    #TODO: 
    #lang_default = project.default_language
    #lang_all = project.selected_languages

    isolinux_tmpl = """
prompt 1
timeout 200

ui gfxboot.com /boot/isolinux/init

label pardus
    kernel /boot/kernel
    append initrd=/boot/initrd splash=silent quiet %(exparams)s

label harddisk
    localboot 0x80

label memtest
    kernel /boot/memtest

label hardware
    kernel hdt.c32
"""

    # write isolinux.cfg
    dest = os.path.join(iso_dir, "boot/isolinux/isolinux.cfg")
    data = isolinux_tmpl % dict

    f = file(dest, "w")
    f.write(data % dict)
    f.close()

    # write gfxboot config for title
    data = file(os.path.join(image_dir, "usr/share/gfxtheme/pardus/boot/gfxboot.cfg")).read()
    f = file(os.path.join(iso_dir, "boot/isolinux/gfxboot.cfg"), "w")
    f.write(data % dict)
    f.close()

    '''if len(lang_all) and lang_default != "":
        langdata = ""

        if not lang_default in lang_all:
            lang_all.append(lang_default)

        lang_all.sort()

        for i in lang_all:
            langdata += "%s\n" % i
    '''

    lang_data = "en_US"

    # write default language
    f = file(os.path.join(iso_dir, "boot/isolinux/lang"), "w")
    f.write("%s\n" % lang_data)
    f.close()

    # write available languages
    f = file(os.path.join(iso_dir, "boot/isolinux/languages"), "w")
    f.write("%s\n" % lang_data)
    f.close()




def make(cache_dir=None):
    run("rm -rf %s" %os.path.join(cache_dir,"iso_dir"), True)
    generate_configs(cache_dir)
    build_squash(cache_dir)
    build_iso(cache_dir)


if __name__== "__main__":
    make(".")

