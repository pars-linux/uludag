# l10n

LABEL_OTHER = {
    "en": "Other",
    "tr": "Diğer",
}

FAIL_TIMEOUT = {
    "en": "Request timed out.",
    "tr": "Talep zaman aşımına uğradı.",
}

FAIL_NOENTRY = {
    "en": "No such entry.",
    "tr": "Böyle bir kayıt bulunmuyor.",
}

# Grub parser configuration

GRUB_CONF = "/boot/grub/grub.conf"

TIMEOUT = 3.0
MAX_ENTRIES = 3

# Supported operating systems and required fields for them

SYSTEMS = {
    "linux": "Linux,root,kernel,initrd,options",
    "windows": "Windows,root",
    "other": "%s,root,kernel,initrd,options" % _(LABEL_OTHER),
}

# Grub parser

class grubCommand:
    """Grub menu command"""
    
    def __init__(self, key, options=[], value=""):
        self.key = key
        self.options = options
        self.value = value
    
    def __str__(self):
        if self.options:
            return "%s %s %s" % (self.key, " ".join(self.options), self.value)
        else:
            return "%s %s" % (self.key, self.value)

class grubEntry:
    """Grub menu entry"""
    
    def __init__(self, title):
        self.title = title
        self.commands = []
    
    def copy(self):
        """Returns a copy of entry."""
        import copy
        return copy.deepcopy(self)
    
    def listCommands(self):
        """Returns list of commands used in entry"""
        return map(lambda x: x.key, self.commands)
    
    def setCommand(self, key, value, opts=[], append=False):
        """Adds a new command to entry. Optional append argument allows addition of multiple commands like 'map'."""
        if not append:
            self.unsetCommand(key)
        self.commands.append(grubCommand(key, opts, value))
    
    def getCommand(self, key, only_last=True):
        """Returns command object. If only_last is False, returns a list of commands named 'key'."""
        commands = filter(lambda x: x.key == key, self.commands)
        if only_last:
            try:
                return commands[-1]
            except IndexError:
                return None
        return commands
    
    def unsetCommand(self, key):
        """Removes 'key' from commands."""
        self.commands = filter(lambda x: x.key != key, self.commands)
    
    def __str__(self):
        conf = []
        conf.append("title %s" % self.title)
        for command in self.commands:
            conf.append(str(command))
        return "\n".join(conf)

class grubConf:
    """Grub configuration class."""
    
    def __init__(self):
        self.options = {}
        self.entries = []
        self.header = []
        self.index = 0
    
    def setHeader(self, header):
        """Sets grub.conf header"""
        self.header = header.split("\n")
    
    def __parseLine__(self, line):
        """Parses single grub.conf line and returns a tupple of key, value and options."""
        line = line.strip()
        try:
            key, data = line.split(" ", 1)
        except ValueError:
            key = line
            data = ""
        
        key = key.strip(" =")
        data = data.strip(" =")
        
        options = []
        values = []
        
        option = True
        for x in data.split():
            if option and x.startswith("--"):
                options.append(x)
            else:
                values.append(x)
                option = False
        
        return key, " ".join(values), options

    def parseConf(self, filename):
        """Parses a grub.conf file"""
        self.options = {}
        self.entries = []
        
        option = True
        entry = None
        
        for line in file(filename):
            if not line.strip():
                continue
            key, value, opts = self.__parseLine__(line)
            
            if key == "title":
                option = False
                if entry:
                    self.entries.append(entry)
                    entry = None
            
            if option:
                self.options[key] = value
            else:
                if key == "title":
                    entry = grubEntry(value)
                else:
                    entry.setCommand(key, value, opts, append=True)
        
        if entry:
            self.entries.append(entry)
        
        import os.path
        default = os.path.join(os.path.dirname(filename), "default")
        if os.path.exists(default):
            self.index = int(file(default).read().split("\0")[0])
    
    def getSavedIndex(self):
        """Return last booted entry index."""
        return self.index
    
    def __str__(self):
        conf = []
        if self.header:
            for h in self.header:
                conf.append("# %s" % h)
            conf.append("")
        if self.options:
            for key, value in self.options.iteritems():
                line = "%s %s" % (key, value)
                conf.append(line)
            conf.append("")
        for index, entry in enumerate(self.entries):
            if entry.getCommand("savedefault"):
                entry.setCommand("savedefault", str(index))
            conf.append(str(entry))
            conf.append("")
        return "\n".join(conf)
    
    def write(self, filename):
        """Writes grub configuration to file."""
        file(filename, "w").write(str(self))
    
    def listOptions(self):
        """Returns list of options."""
        return self.options.keys()
    
    def setOption(self, key, value):
        """Sets an option."""
        self.options[key] = value
    
    def unsetOption(self, key):
        """Unsets an option."""
        del self.options[key]
    
    def getOption(self, key, default=""):
        """Returns value of an option."""
        return self.options.get(key, default)
    
    def getAllOptions(self):
        """Returns all options."""
        return ["%s %s" % (key, value) for key, value in self.options.items()]
    
    def listEntries(self):
        """Returns a list of entries."""
        return map(lambda x: x.title, self.entries)
    
    def addEntry(self, entry, index=-1):
        """Adds an entry object."""
        if index == -1:
            self.entries.append(entry)
        else:
            self.entries.insert(index, entry)
    
    def getEntry(self, index):
        """Returns an entry object."""
        return self.entries[index]
    
    def indexOf(self, entry):
        """Returns index of an entry object."""
        return self.entries.index(entry)
    
    def removeEntry(self, entry):
        """Removes an entry object."""
        self.entries.remove(entry)

class grubParser:
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
        elif key == "savedefault":
            os_entry["default"] = "saved"
    lst = []
    for k, v in os_entry.iteritems():
        lst.append("%s %s" % (k, v))
    return lst


# Boot.Loader methods

def listSystems():
    sys_list = []
    for key, values in SYSTEMS.iteritems():
        sys_list.append("%s %s" % (key, values))
    return "\n".join(sys_list)

def getOptions():
    try:
        grub = grubParser(GRUB_CONF, write=False, timeout=TIMEOUT)
    except IOError:
        fail(FAIL_TIMEOUT)
    options = [
        "default %s" % grub.config.getOption("default", "0"),
        "timeout %s" % grub.config.getOption("timeout", "0"),
    ]
    if "password" in grub.config.options:
        options.append("password yes")
    grub.release()
    return "\n".join(options)

def setOptions(default=None, timeout=None, password=None):
    try:
        grub = grubParser(GRUB_CONF, write=True, timeout=TIMEOUT)
    except IOError:
        fail(FAIL_TIMEOUT)
    if default != None:
        grub.config.setOption("default", default)
        for index, entry in enumerate(grub.config.entries):
            if default == "saved":
                entry.setCommand("savedefault", "")
            else:
                entry.unsetCommand("savedefault")
    if timeout != None:
        grub.config.setOption("timeout", timeout)
    if password != None:
        grub.config.setOption("password", md5crypt(password))
    grub.release()
    notify("Boot.Loader.changed", "option")

def listEntries():
    try:
        grub = grubParser(GRUB_CONF, write=False, timeout=TIMEOUT)
    except IOError:
        fail(FAIL_TIMEOUT)
    entries = []
    for index, entry in enumerate(grub.config.entries):
        os_entry = importGrubEntry(entry)
        os_entry.insert(0, "index %s" % index)
        if not entry.getCommand("savedefault"):
            default_index = grub.config.getOption("default", "0")
            if default_index != "saved" and int(default_index) == index:
                os_entry.insert(0, "default yes")
        entries.append("\n".join(os_entry))
    grub.release()
    return "\n\n".join(entries)

def removeEntry(index, title):
    try:
        grub = grubParser(GRUB_CONF, write=True, timeout=TIMEOUT)
    except IOError:
        fail(FAIL_TIMEOUT)
    index = int(index)
    if 0 <= index < len(grub.config.entries):
        entry = grub.config.entries[index]
        if entry.title != title:
            fail(FAIL_NOENTRY)
        grub.config.removeEntry(entry)
        default_index = grub.config.options.get("default", "0")
        if default_index == index:
            grub.config.setOption("default", "0")
        grub.release()
        notify("Boot.Loader.changed", "entry")
    else:
        fail(FAIL_NOENTRY)

def setEntry(title, os_type, root, kernel=None, initrd=None, options=None, default="no", index=None):
    try:
        grub = grubParser(GRUB_CONF, write=True, timeout=TIMEOUT)
    except IOError:
        fail(FAIL_TIMEOUT)
    
    entry = grubEntry(title)
    
    if os_type not in SYSTEMS:
        os_type = "other"
    if os_type == "windows":
        entry.setCommand("rootnoverify", grubDevice(root))
        entry.setCommand("makeactive", "")
        entry.setCommand("chainloader", "+1")
    else:
        entry.setCommand("root", grubDevice(root))
    if kernel and "kernel" in SYSTEMS[os_type]:
        if options and "options" in SYSTEMS[os_type]:
            entry.setCommand("kernel", "%s %s" % (kernel, options))
        else:
            entry.setCommand("kernel", kernel)
    if initrd and "initrd" in SYSTEMS[os_type]:
        entry.setCommand("initrd", initrd)
    
    if index == None:
        grub.config.addEntry(entry)
    else:
        index = int(index)
        grub.config.entries[index] = entry
    
    if default == "yes":
        grub.config.setOption("default", index)
    elif default == "saved":
        grub.config.setOption("default", "saved")
        for index, entry in enumerate(grub.config.entries):
            entry.setCommand("savedefault", "")
    elif default == "no" and index != None:
        default_index = grub.config.getOption("default", "0")
        if default_index != "saved" and int(default_index) == index:
            grub.config.setOption("default", "0")
    grub.release()
    notify("Boot.Loader.changed", "entry")

def updateKernelEntry(version, root=None):
    try:
        grub = grubParser(GRUB_CONF, write=True, timeout=TIMEOUT)
    except IOError:
        fail(FAIL_TIMEOUT)
    
    new_version, new_suffix = parseVersion("kernel-%s" % version)
    if not root:
        root = getRoot()
    root_grub = grubDevice(root)
    
    entries = []
    for x in grub.config.entries:
        if isPardusEntry(x, root_grub, new_suffix):
            entries.append(x)
    
    default = grub.config.options.get("default", 0)
    if default == "saved":
        default_index = grub.config.getSavedIndex()
    else:
        default_index = int(grub.config.options.get("default", 0))
    if default_index >= len(grub.config.entries):
        default_index = 0
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
        else:
            action = "insert"
    
    if action:
        release = open("/etc/pardus-release", "r").readline().strip()
        title = "%s [%s%s]" % (release, new_version, new_suffix)
        
        new_entry = grubEntry(title)
        new_entry.setCommand("root", root_grub)
        
        if action == "append":
            index = -1
            boot_parameters = bootParameters(root)
        else:
            if entries[0].getCommand("savedefault"):
                new_entry.setCommand("savedefault", "")
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
        if default != "saved":
            grub.config.setOption("default", updated_index)
    
    grub.release()
    notify("Boot.Loader.changed", "entry")
