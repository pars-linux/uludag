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

def linuxDevice(dev):
    dev = dev[:-1].split("(hd")[1]
    disk, part = dev.split(",")
    return "/dev/hd%s%s" % (chr(97 + int(disk)), int(part) + 1)

def getRoot():
    import os
    for mount in os.popen("/bin/mount").readlines():
        mount_items = mount.split()
        if mount_items[0].startswith("/dev") and mount_items[2] == "/":
            return mount_items[0]

class grubConfLock:
    def __init__(self, _file, write=False, timeout=-1):
        import os.path
        from comar.utility import FileLock
        self.file = _file
        self.write = write
        lockfile = "%s/.%s.lock" % (os.path.dirname(_file), os.path.basename(_file))
        self.lock = FileLock(lockfile)
        self.lock.lock(write, timeout)
        self.config = grubConf()
        if os.path.exists(_file):
            self.config.parseConf(_file)
    
    def release(self, save=True):
        if save and self.write:
            self.config.write(self.file)
        self.lock.unlock()

def importGrubEntry(entry):
    os_entry = {
        "os_type": "other",
        "title": entry.title,
    }
    hidden = False
    for command in entry.commands:
        key = command.key
        value = command.value
        if key == "root":
            os_entry["root"] = linuxDevice(value)
        elif key == "rootnoverify" and not hidden:
            os_entry["root"] = linuxDevice(value)
        elif key == "hide":
            os_entry["root"] = linuxDevice(value)
            hidden = True
        elif key == "initrd":
            os_entry["initrd"] = value
        elif key == "kernel":
            try:
                kernel, options = value.split(" ", 1)
                os_entry["kernel"] = kernel
                os_entry["options"] = options
                if "root=" in options:
                    os_entry["os_type"] = "linux"
            except ValueError:
                os_entry["kernel"] = value
            if os_entry["kernel"].startswith("("):
                root, kernel = os_entry["kernel"].split(")", 1)
                os_entry["root"] = linuxDevice(root + ")")
                os_entry["kernel"] = kernel
        elif key in ["chainloader", "makeactive"]:
            os_entry["os_type"] = "windows"
    lst = []
    for k, v in os_entry.iteritems():
        lst.append("%s %s" % (k, v))
    return lst


# Boot.Loader
GRUB_CONF = "/boot/grub/grub.conf"
TIMEOUT = 3.0
MAX_ENTRIES = 3
OPTIONS = ["default", "timeout", "splash"]

def listOptions():
    return "\n".join(OPTIONS)

def getOption(key):
    try:
        grub = grubConfLock(GRUB_CONF, write=False, timeout=TIMEOUT)
    except IOError:
        fail("Timeout")
    if key in OPTIONS:
        if key == "splash":
            value = grub.config.getOption(key, "")
        else:
            value = grub.config.getOption(key, "0")
        grub.release()
        return "%s %s" % (key, value)
    else:
        grub.release()
        fail("No such option")

def setOption(key, value):
    try:
        grub = grubConfLock(GRUB_CONF, write=True, timeout=TIMEOUT)
    except IOError:
        fail("Timeout")
    if key not in OPTIONS:
        grub.release()
        fail("No such option")
    if value:
        grub.config.setOption(key, value)
    else:
        grub.config.unsetOption(key)
    grub.release()
    notify("Boot.Loader.changed", "option")
    return "%s %s" % (key, value)

def listEntries():
    try:
        grub = grubConfLock(GRUB_CONF, write=False, timeout=TIMEOUT)
    except IOError:
        fail("Timeout")
    entries = []
    for index, entry in enumerate(grub.config.entries):
        os_entry = importGrubEntry(entry)
        os_entry.insert(0, "index %s" % index)
        entries.append("\n".join(os_entry))
    grub.release()
    return "\n\n".join(entries)

def getEntry(index):
    try:
        grub = grubConfLock(GRUB_CONF, write=False, timeout=TIMEOUT)
    except IOError:
        fail("Timeout")
    entry = grub.config.getEntry(int(index))
    os_entry = importGrubEntry(entry)
    grub.release()
    return "\n".join(os_entry)

def removeEntry(index):
    try:
        grub = grubConfLock(GRUB_CONF, write=True, timeout=TIMEOUT)
    except IOError:
        fail("Timeout")
    index = int(index)
    grub.config.removeEntry(grub.config.entries[index])
    default_index = int(grub.config.options.get("default", 0))
    if default_index == index and default_index > 0:
        grub.config.setOption("default", default_index - 1)
    grub.release()
    notify("Boot.Loader.changed", "entry")

def addEntry(title, os_type, root, kernel=None, initrd=None, options=None):
    try:
        grub = grubConfLock(GRUB_CONF, write=True, timeout=TIMEOUT)
    except IOError:
        fail("Timeout")
    entry = grubEntry(title)
    if os_type == "windows":
        entry.setCommand("rootnoverify", grubDevice(root))
        entry.setCommand("makeactive", "")
        entry.setCommand("chainloader", "+1")
    else:
        entry.setCommand("root", grubDevice(root))
    if kernel:
        entry.setCommand("kernel", "%s %s" % (kernel, options))
    if initrd:
        entry.setCommand("initrd", initrd)
    grub.config.addEntry(entry)
    index = grub.config.indexOf(entry)
    grub.release()
    notify("Boot.Loader.changed", "entry")

def updateEntry(index, title, os_type, root, kernel=None, initrd=None, options=None):
    try:
        grub = grubConfLock(GRUB_CONF, write=True, timeout=TIMEOUT)
    except IOError:
        fail("Timeout")
    index = int(index)
    if index < len(grub.config.entries):
        entry = grub.config.getEntry(index)
        entry.title = title
        if os_type == "windows":
            entry.setCommand("rootnoverify", grubDevice(root))
            entry.setCommand("makeactive", "")
            entry.setCommand("chainloader", "+1")
        else:
            entry.setCommand("root", grubDevice(root))
        if kernel:
            entry.setCommand("kernel", "%s %s" % (kernel, options))
        if initrd:
            entry.setCommand("initrd", initrd)
        grub.release()
        notify("Boot.Loader.changed", "entry")
    else:
        fail("No such entry")

def updateKernelEntry(version):
    try:
        grub = grubConfLock(GRUB_CONF, write=True, timeout=TIMEOUT)
    except IOError:
        fail("Timeout")
    
    new_version, new_suffix = parseVersion("kernel-%s" % version)
    root_dev = getRoot()
    root_grub = grubDevice(root_dev)
    
    entries = []
    for x in grub.config.entries:
        if isPardusEntry(x, root_grub, new_suffix):
            entries.append(x)
    
    default_index = int(grub.config.options.get("default", 0))
    default_entry = None
    if len(grub.config.entries):
        default_entry = grub.config.entries[default_index]
    
    make_default = isPardusEntry(default_entry, root_grub, new_suffix)
    
    updated_index = None
    action = None
    if not len(entries):
        action = "append"
    else:
        kernels = {}
        for entry in entries:
            kernel = entry.getCommand("kernel").value.split()[0]
            kernels[parseVersion(kernel)[0]] = entry
        if new_version in kernels:
            if make_default:
                entry = kernels[new_version]
                updated_index = grub.config.indexOf(entry)
                grub.config.setOption("default", updated_index)
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
        
        if MAX_ENTRIES > 0:
            for x in entries[MAX_ENTRIES - 1:]:
                grub.config.removeEntry(x)
        
        if make_default:
            updated_index = grub.config.indexOf(new_entry)
        elif default_entry in grub.config.entries:
            updated_index = grub.config.indexOf(default_entry)
        else:
            updated_index = 0
        grub.config.setOption("default", updated_index)
    
    grub.release()
    notify("Boot.Loader.changed", "entry")
