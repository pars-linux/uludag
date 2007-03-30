from grub import *

def parseVersion(version):
    """Parses a kernel filename and returns kernel version and suffix. Returns False on failure."""
    import re
    try:
        k_version, x, x, k_suffix = re.findall("kernel-(([0-9\.]+)-([0-9]+))(-.*)?", version)[0]
    except IndexError:
        return False
    return k_version, k_suffix

def isPardusEntry(entry, root, suffix="", version=None):
    """Returns if entry is a Pardus kernel on specified root device."""
    commands = entry.listCommands()
    if "kernel" not in commands:
        return False
    kernel = entry.getCommand("kernel").value.split()[0]
    
    if "root" in commands:
        k_root = entry.getCommand("root").value
    if kernel.startswith("("):
        k_root = kernel.split(")")[0] + ")"
    if not k_root or k_root != root:
        return False
    
    try:
        k_version, k_suffix = parseVersion(kernel)
    except TypeError:
        return False
    
    if k_suffix == suffix:
        if version:
            if k_version == version:
                return True
        else:
            return True
    
    return False

def bootParameters(root):
    s = []
    for i in [x for x in open("/proc/cmdline", "r").read().split() if not x.startswith("init=") and not x.startswith("xorg=")]:
        if i.startswith("root="):
            s.append("root=%s" % root)
        elif i.startswith("mudur="):
            mudur = "mudur="
            for p in i[len("mudur="):].split(','):
                if p == "livecd" or p == "livedisk": continue
                mudur += p
            if not len(mudur) == len("mudur="):
                s.append(mudur)
        else:
            s.append(i)
    return " ".join(s).strip()

def grubDevice(dev):
    dev = dev.split("/")[2]
    return "(hd%s,%s)" % (ord(dev[2:3]) - ord("a"), int(dev[3:]) - 1)

def getRoot():
    import os
    for mount in os.popen("/bin/mount").readlines():
        mount_items = mount.split()
        if mount_items[2] == "/":
            return mount_items[0]

class grubConfLock:
    def __init__(self, _file, write=False, timeout=-1):
        from comar.utility import FileLock
        self.file = _file
        self.write = write
        self.lock = FileLock("%s.lock" % _file)
        self.lock.lock(write, timeout)
        self.config = grubConf()
        self.config.parseConf(_file)

    def release(self, save=True):
        if save and self.write:
            self.config.write(self.file)
        self.lock.unlock()

# System.Boot

GRUB_CONF = "/boot/grub/grub.conf"

def listOptions():
    try:
        grub = grubConfLock(GRUB_CONF, write=False, timeout=3.0)
    except IOError:
        fail("Timeout")
    options = "\n".join(grub.config.getAllOptions())
    grub.release()
    return options

def getOption(key):
    try:
        grub = grubConfLock(GRUB_CONF, write=False, timeout=3.0)
    except IOError:
        fail("Timeout")
    option = grub.config.getOption(key)
    grub.release()
    return option

def setOption(key, value):
    try:
        grub = grubConfLock(GRUB_CONF, write=True, timeout=3.0)
    except IOError:
        fail("Timeout")
    grub.config.setOption(key, value)
    grub.release()
    notify("System.Boot.changed", "")

def listEntries():
    try:
        grub = grubConfLock(GRUB_CONF, write=False, timeout=3.0)
    except IOError:
        fail("Timeout")
    entries = "\n".join(grub.config.listEntries())
    grub.release()
    return entries

def getEntry(index):
    try:
        grub = grubConfLock(GRUB_CONF, write=False, timeout=3.0)
    except IOError:
        fail("Timeout")
    entry = grub.config.getEntry(int(index))
    ret = []
    ret.append("index\n \n%s" % index)
    ret.append("title\n \n%s" % entry.title)
    for command in entry.commands:
        if not command.options:
            command.options = " "
        if not command.value:
            command.value = " "
        ret.append("%s\n%s\n%s" % (command.key, command.options, command.value))
    grub.release()
    return "\n\n".join(ret)

def updateKernelEntry(version, max_entries=3, make_default="on"):
    try:
        grub = grubConfLock(GRUB_CONF, write=True, timeout=3.0)
    except IOError:
        fail("Timeout")
        
    max_entries = int(max_entries)
    
    new_version, new_suffix = parseVersion("kernel-%s" % version)
    root_dev = getRoot()
    root_grub = grubDevice(root_dev)
    
    entries = filter(lambda x: isPardusEntry(x, root_grub, new_suffix), grub.config.entries)
    
    action = None
    if not len(entries):
        action = "append"
    else:
        kernels = {}
        for entry in entries:
            kernel = entry.getCommand("kernel").value.split()[0]
            kernels[parseVersion(kernel)[0]] = entry
        if new_version in kernels:
            if make_default == "on":
                entry = kernels[new_version]
                grub.config.setOption("default", grub.config.indexOf(entry))
        else:
            action = "insert"
    
    if action:
        release = open("/etc/pardus-release", "r").readline().strip()
        title = "%s [%s%s]" % (release, new_version, new_suffix)
        
        new_entry = grubEntry(title)
        new_entry.setCommand("root", root_grub)
        
        if action == "append":
            index = -1
            boot_parameters = bootParameters(root_dev)
        else:
            index = grub.config.indexOf(entries[0])
            kernel = entries[0].getCommand("kernel").value
            boot_parameters = kernel.split(" ", 1)[1]
        
        new_entry.setCommand("kernel", "/boot/kernel-%s%s %s" % (new_version, new_suffix, boot_parameters))
        new_entry.setCommand("initrd", "/boot/initrmfs-%s%s" % (new_version, new_suffix))
        grub.config.addEntry(new_entry, index)
        
        if max_entries > 0:
            for x in entries[max_entries - 1:]:
                grub.config.removeEntry(x)
        
        if make_default == "on":
            grub.config.setOption("default", grub.config.indexOf(new_entry))
    
    grub.release()
    notify("System.Boot.changed", "")
