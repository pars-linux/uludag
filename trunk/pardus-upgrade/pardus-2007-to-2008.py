#!/usr/bin/python
# -*- coding: utf-8 -*-

import bz2
import os
import re
import sys
import shutil
import subprocess

import piksemel
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

def get_drivers_list():
    drivers = []
    for pkg in repodoc.tags("Package"):
        if pkg.getTagData("PartOf") == "kernel.drivers":
            drivers.append(pkg.getTagData("PackageURI"))
    return drivers

def get_package_version(name):
    for p in repodoc.tags("Package"):
        if p.getTagData("Name") == name:
            version = p.getTag("History").getTag("Update").getTagData("Version")
            release = p.getTag("History").getTag("Update").getAttribute("release")
            return "%s-%s" % (version, release)
    return None

def get_package(name):
    for node in repodoc.tags("Package"):
        if node.getTagData("Name") == name:
            return node.getTagData("PackageURI")

def get_packages_to_install():
    excludes = ["pisi", "package-manager", "lzma", "ncurses"]
    pkgs = []
    for node in repodoc.tags("Package"):
        if node.getTagData("Name") not in excludes:
            pkgs.append(node.getTagData("PackageURI"))
    return pkgs

def install_delayed_packages():
    try:
        pisi.api.install(['/media/%s/repo/%s' % (cddev, get_package("pisi")),
                          '/media/%s/repo/%s' % (cddev, get_package("package-manager")),
                          '/media/%s/repo/%s' % (cddev, get_package("lzma"))])
    except SyntaxError:
        pass

def install_ncurses():
    os.system('pisi it -y --ignore-comar %s' % get_package("ncurses"))

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
        file_path = "/home/%s/%s" % (user, user_file)
        if os.path.exists(file_path):
            os.unlink(file_path)

def delete_users_dir(user_dir):
    users = _find_users()
    for user in users:
        dir_path = "/home/%s/%s" % (user, user_dir)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

def migrate_users_bashrc(bashrc):
    bashrcLinesToAdd = """
alias grep="grep --color"
alias egrep="egrep --color"
alias fgrep="fgrep --color"

alias scp-resume="rsync --compress-level=3 --partial --progress --rsh=ssh"

for sh in /etc/profile.d/*.sh ; do
    if [ -r "$sh" ] ; then
        . "$sh"
    fi
done
unset sh

"""

    bashrcLinesToRemove = ["source /etc/profile",
                           "source /etc/bashrc",
                           "export GTK2_RC_FILES=",
                           "alias svn="]

    bashrc_backup = "%s-pardus_2007_backup" % bashrc
    shutil.move(bashrc, bashrc_backup)

    src = file(bashrc_backup).readlines()

    targetData = ""
    for line in src:
        found = 0
        for i in bashrcLinesToRemove:
            if line.startswith(i):
                found = 1

        if not found:
            targetData += line

    targetData += bashrcLinesToAdd

    ftarget = file(bashrc, "w")
    ftarget.write(targetData)
    ftarget.close()

def fix_bashrc():
    users = _find_users()
    for user in users:
        bashrcFile = "/home/%s/.bashrc" % user
        if os.path.exists(bashrcFile):
            migrate_users_bashrc(bashrcFile)

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

def get_boot_device():
    dev = get_device("/")
    m = re.match("(.*)(\d{1,3})", dev)
    dev, part = m.groups()[0], m.groups()[1]
    for line in open("/boot/grub/device.map").readlines():
        if line.split()[1] == dev:
            grub_dev = line.split()[0].strip()
            return grub_dev[:-1] + ",%d)" % (int(part) - 1)
    return ""

def write_new_grub():
    version = get_package_version("kernel")
    open('/boot/grub/grub.conf', 'w').write("""
default 0
gfxmenu /boot/grub/message
timeout 10
background 10333C

title Pardus 2008
root %s
kernel /boot/kernel-%s root=LABEL=%s vga=791 mudur=language:tr quiet splash=silent
initrd /boot/initramfs-%s
""" % (get_boot_device(), version, get_label("/", "PARDUS_ROOT"), version))

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
    os.system("hav call Boot.Loader.updateKernelEntry version '%s'" % get_package_version("kernel"))
    # Just ugly... would be great if updateKernelEntry should accept LABEL=XYZ as root param but
    # instead returns no such device
    os.system("sed -i -r 's#%s#LABEL=%s#g' /boot/grub/grub.conf" % (get_device("/"), get_label("/", "PARDUS_ROOT")))

def check_grub_release():
    # we need grub release > 40
    subprocess.Popen('pisi up -y --ignore-dependency --ignore-safety comar-api comar grub', shell=True).wait()

def check_and_upgrade_kernel():
    device = os.path.basename(get_pardus_cd_device())
    os.chdir('/media/%s/repo/' % device)

    kernelnbootsplash = [get_package("kernel"),
                         get_package("kernel-headers"),
                         get_package("bootsplash"),
                         get_package("bootsplash-theme-pardus")]

    if os.popen("uname -r").read().strip() != get_package_version("kernel"):
        subprocess.Popen('pisi it -y --ignore-comar --ignore-safety --ignore-file-conflicts %s' % pisi.util.strlist(kernelnbootsplash), shell=True).wait()
        subprocess.Popen('pisi it -y --ignore-comar --ignore-safety --ignore-file-conflicts %s' % pisi.util.strlist(get_drivers_list()), shell=True).wait()
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

def parse_repo():
    index = "/media/%s/repo/pisi-index.xml.bz2" % cddev
    return piksemel.parseString(bz2.decompress(open(index, "r").read()))

check_pardus_2008_cd()
cddev = os.path.basename(get_pardus_cd_device())
repodoc = parse_repo()

def migrate_2007_to_2008():
    check_grub_release()
    check_and_upgrade_kernel()
    # reboot needed to run with the new kernel.
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
    fix_bashrc()

if __name__ == '__main__':
    migrate_2007_to_2008()
