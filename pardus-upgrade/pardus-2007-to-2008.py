#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess

import pisi

def get_pardus_cd_device():
    return os.popen("hal-get-property --udi /org/freedesktop/Hal/devices/volume_label_Pardus --key block.device 2> /dev/null").read().strip()

def is_pardus_cd_mounted():
    return os.popen("hal-get-property --udi /org/freedesktop/Hal/devices/volume_label_Pardus --key volume.is_mounted 2> /dev/null").read().strip()

def error(msg):
    print "\033[31m" + msg
    sys.exit(1)

def check_pardus_2008_cd():
    block = get_pardus_cd_device()
    if not block:
        error("Pardus 2008 CD not found!")

    # FIXME: mount if not mounted
    if is_pardus_cd_mounted() == "false":
        error("Pardus 2008 CD is not mounted!")

    device = os.path.basename(block)
    if not os.path.exists("/media/%s/boot/isolinux" % device):
        error("Pardus 2008 CD not found")

def install_2008_packages():
    pkgs = get_packages_to_install()
    subprocess.Popen('pisi it -y --ignore-comar --ignore-file-conflicts %s' % pisi.util.strlist(pkgs), shell=True).wait()

def get_packages_to_install():
    exclude = ['pisi-index.xml.bz2', 'pisi-index.xml.bz2.sha1sum', 'lzma-4.32.6-6-3.pisi',
               'ncurses-5.6_20071201-5-2.pisi', 'pisi-2.0-99-25.pisi', 'package-manager-1.3.7-45-13.pisi']
    pkgs = os.listdir('.')
    for e in exclude:
        pkgs.remove(e)
    return pkgs

def install_delayed_packages():
    try:
        pisi.api.install(['/media/%s/repo/pisi-2.0-99-25.pisi' % cddev,
                          '/media/%s/repo/package-manager-1.3.7-45-13.pisi' % cddev, 
                          '/media/%s/repo/lzma-4.32.6-6-3.pisi' % cddev])
    except SyntaxError:
        pass

def install_ncurses():
    os.system('pisi it -y --ignore-comar ncurses-5.6_20071201-5-2.pisi')

def pisi_upgrade():
    os.system('pisi up -y')

def configure_pending_packages():
    os.system('pisi cp baselayout')
    os.system('pisi cp')

def clean_old_comar():
    os.system('killall network-applet')
    os.system('killall comar')
    shutil.rmtree('/var/db/comar')

def add_new_repos():
    os.system('pisi ar -y pardus-2008 http://paketler.pardus.org.tr/pardus-2008/pisi-index.xml.bz2')
    os.system('pisi ar -y contrib-2008 http://paketler.pardus.org.tr/contrib-2008/pisi-index.xml.bz2')

def delete_old_xorg():
    os.unlink('/etc/X11/xorg.conf')

def start_dbus():
    os.system('service dbus start')

def _find_users():
    def is_user_home(user):
        uid = os.stat("/home/%s" % user)[4]
        return uid >= 1000 and uid <= 65000

    return filter(lambda x:is_user_home(x), os.listdir("/home"))

def delete_users_file(user_file):
    users = _find_users()
    for user in users:
        user_file = "/home/%s/%s" % (user, user_file)
        if os.path.exists(user_file):
            os.unlink(user_file)

def delete_users_dir(user_dir):
    users = _find_users()
    for user in users:
        user_dir = "/home/%s/%s" % (user, user_dir)
        if os.path.exists(user_dir):
            shutil.rmtree(user_dir)

def fix_dbus():
    delete_users_file(".dbus-session")
    delete_users_dir(".dbus")

def delete_old_splash():
    delete_users_dir(".kde3.5/share/apps/ksplash/cache/Moodin")

def fix_keyboard():
    # pc was directory with xorg-data
    # shutil.rmtree('/usr/share/X11/xkb/symbols/pc')
    os.system('pisi it --reinstall xkeyboard-config')

def update_fstab():
    root = get_device('/')
    home = get_device('/home')
    if root:
        os.system('sed -i -r s#%s#LABEL=%s# /etc/fstab' % (root, get_label("/", "PARDUS_ROOT")))
    if home:
        os.system('sed -i -r s#%s#LABEL=%s# /etc/fstab' % (home, get_label("/home", "PARDUS_HOME")))

def get_device(mount_point):
    for mount in os.popen("/bin/mount").readlines():
        mount_items = mount.split()
        if mount_items[2] == mount_point:
            return mount_items[0]
    return None

def get_label(mount_point, label=None):
    for mount in os.popen("/bin/mount -l").readlines():
        mount_items = mount.split()
        if mount_items[0].startswith("/dev") and mount_items[2] == mount_point:
            if len(mount_items) > 6:
                return mount_items[6][1:-1]
            else:
                if label:
                    os.system("/sbin/e2label %s %s" % (mount_items[0], label))
                    return label
    return None

def write_new_grub():
    open('/boot/grub/grub.conf', 'w').write("""
default 0
gfxmenu /boot/grub/message
timeout 10
background 10333C

title Pardus 2008
root (hd0,0)
kernel /boot/kernel-2.6.25.9-101 root=LABEL=%s vga=791 mudur=language:tr quiet splash=silent
initrd /boot/initramfs-2.6.25.9-101
""" % get_label("/", "PARDUS_ROOT"))

def clean_old_pisi():
    if os.path.exists('/etc/pisi/pisi.conf.newconfig'):
        os.rename('/etc/pisi/pisi.conf.newconfig','/etc/pisi/pisi.conf')

    shutil.rmtree('/var/db/pisi')
    shutil.rmtree('/var/lib/pisi/index')

def init_old_pisi():
    options = pisi.config.Options()
    options.ignore_comar = True
    options.ignore_dependency = True
    options.yes_all = True
    pisi.api.init(options=options, comar=False)

def move_cp_to_new_db():
    cp = open('/var/lib/pisi/info/configpending', 'a')
    for pkg in pisi.context.installdb.list_pending().keys():
        cp.write('%s\n' % pkg)
    cp.close()

def write_grub_for_new_kernel():
    os.system("hav call Boot.Loader.updateKernelEntry version '2.6.25.9-101'")
    # Just ugly... would be great if updateKernelEntry should accept LABEL=XYZ as root param but
    # instead returns no such device
    os.system("sed -i -r 's#%s#LABEL=%s#g' /boot/grub/grub.conf" % (get_device("/"), get_label("/", "PARDUS_ROOT")))

def check_grub_release():
    # we need grub release > 40
    subprocess.Popen('pisi up -y --ignore-dependency --ignore-safety comar-api comar grub', shell=True).wait()

def check_and_upgrade_kernel():
    device = os.path.basename(get_pardus_cd_device())
    os.chdir('/media/%s/repo/' % device)

    # FIXME: actually these should be found by looking at PartOf. Hardcoded for now.
    drivers = ['accessrunner-firmware-1.0-1-1.pisi', 'acerhk-0.5.35-4-16.pisi', 'acx100-20080210-15-16.pisi', 'acx100-firmware-20060207-3-1.pisi', 'atl2-2.0.4-2-16.pisi', 'atmel-firmware-1.3-1-1.pisi', 'b43-firmware-4.150.10.5-1-1.pisi', 'bluez-firmware-1.2-2-1.pisi', 'eagle-firmware-1.1-1-1.pisi', 'et131x-1.2.3-3-15.pisi', 'gspca-0.0_20071224-14-15.pisi', 'ipw2100-firmware-1.3-2-1.pisi', 'ipw2200-firmware-3.0-4-1.pisi', 'iwlwifi3945-ucode-2.14.1.5-1-1.pisi', 'iwlwifi4965-ucode-4.44.1.20-1-1.pisi', 'linux-uvc-0.0_217-30-20.pisi', 'lirc-drivers-0.8.3-18-16.pisi', 'lmpcm_usb-0.5.6-4-16.pisi', 'ltmodem-8.31_alpha10-8-16.pisi', 'madwifi-ng-0.9.4_3698-17-15.pisi', 'microdia-0.0_20080621-1-2.pisi', 'ndiswrapper-1.52-39-15.pisi', 'ov511-2.32-4-16.pisi', 'pwc-10.0.12_20080322-13-15.pisi', 'qc-usb-0.6.6-3-15.pisi', 'ralink-firmware-0.0_20080409-1-1.pisi', 'slmodem-2.9.11_20080126-22-15.pisi', 'sn9c1xx-1.48-2-14.pisi', 'speedtouch-firmware-3.0.1-3-1.pisi', 'ungrab-winmodem-1_20080126-4-15.pisi', 'zd1201-firmware-0.4-1-1.pisi', 'zd1211-firmware-1.4-3-1.pisi']

    kernelnbootsplash = ["kernel-2.6.25.9-101-40.pisi", "kernel-headers-2.6.25.9-101-40.pisi", "bootsplash-3.3-1-2.pisi", "bootsplash-theme-pardus-0.4.1-6-13.pisi"]

    if os.popen("uname -r").read().strip() != "2.6.25.9-101":
        subprocess.Popen('pisi it -y --ignore-comar --ignore-safety --ignore-file-conflicts %s' % pisi.util.strlist(kernelnbootsplash), shell=True).wait()
        subprocess.Popen('pisi it -y --ignore-comar --ignore-safety --ignore-file-conflicts %s' % pisi.util.strlist(drivers), shell=True).wait()
        write_grub_for_new_kernel()
        update_fstab()
        error("Reboot needed!")

# Because build no's are started from 1 again and we can not reload or import new
# pisi modules to do this in python 2.4, must be run in python 2.5 interpreter.
def upgrade_2007_packages():
    f = open('/tmp/releaseup.py', 'w')
    f.write('''
import os
import pisi
installdb = pisi.db.installdb.InstallDB()
packagedb = pisi.db.packagedb.PackageDB()
ups = []
for pkg in installdb.list_installed():
    if installdb.get_package(pkg).distributionRelease != '2008' and packagedb.has_package(pkg):
        ups.append(pkg)
os.system('pisi it -y --reinstall %s' % pisi.util.strlist(ups))
''')
    f.close()
    subprocess.Popen('python /tmp/releaseup.py', shell=True).wait()
    os.unlink('/tmp/releaseup.py')

# copied from http://svn.pardus.org.tr/uludag/trunk/tasma/network-manager/utils/import_nw.py
def copy_network_data_to_new_comar_db():
    import piksemel
    import comar
    import struct

    class ComarLink(comar.Link):
        __DUMPPROFILE = 16
        def __pack(self, cmd, id, args):
            size = 0
            args2 = []
            # COMAR RPC is using network byte order (big endian)
            fmt = "!ii"
            for a in args:
                        a = str(a)      # for handling unicode
                        fmt += "h%dsB" % (len(a))
                        size += 2 + len(a) + 1
                        args2.append(len(a))
                        args2.append(a.encode("utf-8"))
                        args2.append(0)
            pak = struct.pack(fmt, (cmd << 24) | size, id, *args2)
            return pak

        def dump(self, id=0):
            """Dump profile database.
            """
            pak = self.__pack(self.__DUMPPROFILE, id, [])
            self.sock.send(pak)

    def run():
        try:
            os.makedirs('/etc/network')
        except:
            pass

        link = ComarLink()
        link.dump()
        reply = link.read_cmd()

        doc = piksemel.parseString(reply.data)
        for item in doc.tags():
            model, package, name = item.getTagData('key').split('/')
            if model == 'Net.Link':
                name = name.split('=')[1]
                config = {}
                for data in item.tags():
                    key = data.getAttribute('key')
                    value = data.getTagData('value')
                    if not value or key == 'name':
                        continue
                    config[key] = value
                fname = '/etc/network/%s' % package.replace('-', '_')
                f = file(fname, 'a')
                f.write('[%s]\n' % name)
                for key, value in config.iteritems():
                    f.write('%s = %s\n' % (key, value))
                f.write('\n')
                f.close()
                os.chmod(fname, 0600)
                print '%s - %s' % (package, name)

    run()

cddev = os.path.basename(get_pardus_cd_device())

def migrate_2007_to_2008():
    check_pardus_2008_cd()
    check_grub_release()
    check_and_upgrade_kernel()
    # reboot needed to run with 2.6.25 kernel.
    copy_network_data_to_new_comar_db()
    install_2008_packages()
    clean_old_comar()
    init_old_pisi()
    install_delayed_packages()
    delete_old_xorg()
    write_new_grub()
    clean_old_pisi()
    install_ncurses()
    add_new_repos()
    move_cp_to_new_db()
    start_dbus()
    configure_pending_packages()
    delete_old_splash()
    upgrade_2007_packages()
    pisi_upgrade()
    fix_keyboard()
    fix_dbus()

if __name__ == '__main__':
    migrate_2007_to_2008()
