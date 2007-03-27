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

# System.Boot

GRUB_CONF = "/boot/grub/grub.conf"
gc = grub.grubConf()
gc.parseConf(GRUB_CONF)

def listOptions():
    return "\n".join(gc.getAllOptions())

def getOption(key):
    return gc.getOption(key)

def setOption(key, value):
    gc.setOption(key, value)
    gc.write(GRUB_CONF)
    notify("System.Boot.changed", "")

def listEntries():
    return "\n".join(gc.listEntries())

def getEntry(index):
    entry = gc.getEntry(int(index))
    ret = []
    ret.append("title\n \n%s" % entry.title)
    for command in entry.commands:
        if not command.options:
            command.options = " "
        if not command.value:
            command.value = " "
        ret.append("%s\n%s\n%s" % (command.key, command.options, command.value))
    return "\n\n".join(ret)

def updateGrub(new_kernel, max_entries=3, make_default=True):
    new_version, new_suffix = parseVersion("kernel-%s" % new_kernel)
    root_dev = getRoot()
    root_grub = grubDevice(root_dev)
    
    entries = filter(lambda x: isPardusEntry(x, root_grub, new_suffix), gc.entries)
    
    action = None
    if not len(entries):
        action = "append"
    else:
        kernels = {}
        for entry in entries:
            kernel = entry.getCommand("kernel").value.split()[0]
            kernels[parseVersion(kernel)[0]] = entry
        if new_version in kernels:
            entry = kernels[new_version]
            if make_default:
                gc.setOption("default", gc.indexOf(entry))
        else:
            action = "insert"
    
    if action:
        release = open("/etc/pardus-release", "r").readline().strip()
        title = "%s [%s%s]" % (release, new_version, new_suffix)
        if action == "append":
            index = -1
        else:
            index = gc.indexOf(entries[0])
        new_entry = grubEntry(title)
        new_entry.setCommand("root", root_grub)
        new_entry.setCommand("kernel", "/boot/kernel-%s%s %s" % (new_version, new_suffix, bootParameters(root_dev)))
        new_entry.setCommand("initrd", "/boot/initrmfs-%s%s" % (new_version, new_suffix))
        gc.addEntry(new_entry, index)
        
        if max_entries > 0:
            for x in entries[max_entries - 1:]:
                gc.removeEntry(x)
        
        if make_default:
            gc.setOption("default", gc.indexOf(new_entry))
    
    gc.write(GRUB_CONF)
    notify("System.Boot.changed", "")
