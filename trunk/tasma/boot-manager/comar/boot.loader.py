import os
import os.path

# l10n

LABEL_OTHER = _({
    "en": "Other",
    "tr": "Diğer",
})

FAIL_TIMEOUT = _({
    "en": "Request timed out.",
    "tr": "Talep zaman aşımına uğradı.",
})

FAIL_NOTITLE = _({
    "en": "Title must be given.",
    "tr": "Başlık belirtilmeli.",
})

FAIL_NOROOT = _({
    "en": "Root drive must be given.",
    "tr": "Kök sürücü belirtilmeli.",
})

FAIL_NOKERNEL = _({
    "en": "Kernel path must be given.",
    "tr": "Çekirdek adresi belirtilmeli.",
})

FAIL_NOENTRY = _({
    "en": "No such entry.",
    "tr": "Böyle bir kayıt bulunmuyor.",
})

FAIL_NODEVICE = _({
    "en": "No such device.",
    "tr": "Böyle bir aygıt bulunmuyor.",
})

FAIL_NOSYSTEM = _({
    "en": "No such system.",
    "tr": "Böyle bir sistem türü bulunmuyor.",
})

FAIL_NOGRUB = _({
    "en": "Unable to find Grub device map.",
    "tr": "Grub aygıt haritası bulunamadı.",
})

# Grub parser configuration

GRUB_CONF = "/boot/grub/grub.conf"

TIMEOUT = 3.0
MAX_ENTRIES = 3

# Supported operating systems and required fields for them

SYSTEMS = {
    "linux": "Linux,*root,*kernel,initrd,options",
    "xen": "Xen,*root,*kernel,initrd,options",
    "windows": "Windows,*root",
    "memtest": "Memtest,",
    "other": "%s,*root,kernel,initrd,options" % LABEL_OTHER,
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
        
        default = os.path.join(os.path.dirname(filename), "default")
        if os.path.exists(default):
            try:
                self.index = int(file(default).read().split("\0")[0])
            except ValueError:
                self.index = 0
    
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
        device_map = os.path.join(os.path.dirname(_file), "device.map")
        if not os.path.exists(device_map):
            fail(FAIL_NOGRUB)
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


class ParseError(Exception):
    pass

def parseVersion(version):
    """Parses a kernel filename and returns kernel version and suffix. Raises ParseError"""
    import re
    try:
        k_version, x, x, k_suffix = re.findall("kernel-(([0-9\.]+)-([0-9]+))(-.*)?", version)[0]
    except IndexError:
        raise ParseError
    return k_version, k_suffix

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
    device_map = os.path.join(os.path.dirname(GRUB_CONF), "device.map")
    try:
        for device in file(device_map):
            grub_dev, linux_dev = device.strip().split("\t")
            if dev.startswith(linux_dev):
                part = dev.replace(linux_dev, "", 1)
                if part.startswith("p"):
                    part = int(part[1:]) - 1
                else:
                    part = int(part) - 1
                return grub_dev.replace(")", ",%s)" % part)
    except ValueError:
        return

def linuxDevice(dev):
    device_map = os.path.join(os.path.dirname(GRUB_CONF), "device.map")
    try:
        dev, part = dev.split(",")
    except ValueError:
        return
    dev = "%s)" % dev
    part = int(part.replace(")", "")) + 1
    for device in file(device_map):
        grub_dev, linux_dev = device.strip().split("\t")
        if dev == grub_dev:
            if linux_dev[-1].isdigit():
                part = "p%s" % part
            return "%s%s" % (linux_dev, part)

def getRoot():
    for mount in os.popen("/bin/mount").readlines():
        mount_items = mount.split()
        if mount_items[0].startswith("/dev") and mount_items[2] == "/":
            return mount_items[0]

def md5crypt(password):
    import random
    import md5
    des_salt = list('./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    salt, magic = str(random.random())[-8:], '$1$'
    
    ctx = md5.new(password)
    ctx.update(magic)
    ctx.update(salt)
    
    ctx1 = md5.new(password)
    ctx1.update(salt)
    ctx1.update(password)
    
    final = ctx1.digest()
    
    for i in range(len(password), 0 , -16):
        if i > 16:
            ctx.update(final)
        else:
            ctx.update(final[:i])
    
    i = len(password)
    
    while i:
        if i & 1:
            ctx.update('\0')
        else:
            ctx.update(password[:1])
        i = i >> 1
    final = ctx.digest()
    
    for i in range(1000):
        ctx1 = md5.new()
        if i & 1:
            ctx1.update(password)
        else:
            ctx1.update(final)
        if i % 3: ctx1.update(salt)
        if i % 7: ctx1.update(password)
        if i & 1:
            ctx1.update(final)
        else:
            ctx1.update(password)
        final = ctx1.digest()
    
    def _to64(v, n):
        r = ''
        while (n-1 >= 0):
            r = r + des_salt[v & 0x3F]
            v = v >> 6
            n = n - 1
        return r
    
    rv = magic + salt + '$'
    final = map(ord, final)
    l = (final[0] << 16) + (final[6] << 8) + final[12]
    rv = rv + _to64(l, 4)
    l = (final[1] << 16) + (final[7] << 8) + final[13]
    rv = rv + _to64(l, 4)
    l = (final[2] << 16) + (final[8] << 8) + final[14]
    rv = rv + _to64(l, 4)
    l = (final[3] << 16) + (final[9] << 8) + final[15]
    rv = rv + _to64(l, 4)
    l = (final[4] << 16) + (final[10] << 8) + final[5]
    rv = rv + _to64(l, 4)
    l = final[11]
    rv = rv + _to64(l, 2)
    
    return rv

def parseGrubEntry(entry):
    os_entry = {
        "os_type": "other",
        "title": entry.title,
    }
    for command in entry.commands:
        key = command.key
        value = command.value
        if key in ["root", "rootnoverify"]:
            os_entry["root"] = linuxDevice(value)
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
            if os_entry["kernel"] == "/boot/xen.gz":
                os_entry["os_type"] = "xen"
            elif os_entry["kernel"] == "/boot/memtest.bin":
                os_entry["os_type"] = "memtest"
                del os_entry["kernel"]
        elif key in ["chainloader", "makeactive"]:
            os_entry["os_type"] = "windows"
        elif key == "savedefault":
            os_entry["default"] = "saved"
        elif key == "module" and os_entry["os_type"] == "xen":
            if value.startswith("("):
                value = value.split(")", 1)[1]
            if value.startswith("/boot/kernel"):
                if " " in value:
                    os_entry["kernel"], os_entry["options"] = value.split(" ", 1)
                else:
                    os_entry["kernel"] = value
            elif value.startswith("/boot/init"):
                os_entry["initrd"] = value
    return os_entry

def makeGrubEntry(title, os_type, root=None, kernel=None, initrd=None, options=None):
    if os_type not in SYSTEMS:
        fail(FAIL_NOSYSTEM)
    
    required = []
    for field in SYSTEMS[os_type].split(",")[1:]:
        if field.startswith("*"):
            required.append(field[1:])
    
    if "root" in required:
        if not root:
            fail(FAIL_NOROOT)
    else:
        root = getRoot()
    grub_device = grubDevice(root)
    if not grub_device:
        fail(FAIL_NODEVICE)
    
    if "kernel" in required and not kernel:
        fail(FAIL_NOKERNEL)
    
    entry = grubEntry(title)
    
    if os_type == "windows":
        # If Windows is not on first disk...
        disk = grub_device.split(",", 1)[0] + ")"
        if disk != "(hd0)":
            entry.setCommand("map", "%s (hd0)" % disk)
            entry.setCommand("map", "(hd0) %s" % disk, append=True)
        entry.setCommand("rootnoverify", grub_device)
        entry.setCommand("makeactive", "")
        entry.setCommand("chainloader", "+1")
    else:
        entry.setCommand("root", grub_device)
    if os_type == "xen":
        entry.setCommand("kernel", "/boot/xen.gz")
        if kernel and "kernel" in SYSTEMS[os_type]:
            if options and "options" in SYSTEMS[os_type]:
                entry.setCommand("module", "%s %s" % (kernel, options))
            else:
                entry.setCommand("module", kernel)
        if initrd and "initrd" in SYSTEMS[os_type]:
            entry.setCommand("module", initrd, append=True)
    elif os_type == "memtest":
        entry.setCommand("root", grub_device)
        entry.setCommand("kernel", "/boot/memtest.bin")
    else: # linux, other
        if kernel and "kernel" in SYSTEMS[os_type]:
            if options and "options" in SYSTEMS[os_type]:
                entry.setCommand("kernel", "%s %s" % (kernel, options))
            else:
                entry.setCommand("kernel", kernel)
        if initrd and "initrd" in SYSTEMS[os_type]:
            entry.setCommand("initrd", initrd)
    return entry

# Boot.Loader methods

def listSystems():
    sys_list = []
    for key, values in SYSTEMS.iteritems():
        values = values.replace("*", "")
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
    if "background" in grub.config.options:
        options.append("background %s" % grub.config.getOption("background"))
    if "splashimage" in grub.config.options:
        splash = grub.config.getOption("splashimage")
        if ")" in splash:
            splash = splash.split(")")[1]
        options.append("splash %s" % splash)
    grub.release()
    return "\n".join(options)

def setOptions(default=None, timeout=None, password=None, background=None, splash=None):
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
        grub.config.setOption("password", "--md5 %s" % md5crypt(password))
    if background != None:
        grub.config.setOption("background", background)
    if splash != None:
        root = getRoot()
        root_grub = grubDevice(root)
        grub.config.setOption("splashimage", "%s%s" % (root_grub, splash))
    grub.release()
    notify("Boot.Loader.changed", "option")

def listEntries():
    try:
        grub = grubParser(GRUB_CONF, write=False, timeout=TIMEOUT)
    except IOError:
        fail(FAIL_TIMEOUT)
    entries = []
    for index, entry in enumerate(grub.config.entries):
        os_entry = []
        for k, v in parseGrubEntry(entry).iteritems():
            os_entry.append("%s %s" % (k, v))
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

def setEntry(title, os_type, root=None, kernel=None, initrd=None, options=None, default="no", index=None):
    try:
        grub = grubParser(GRUB_CONF, write=True, timeout=TIMEOUT)
    except IOError:
        fail(FAIL_TIMEOUT)
    
    if not len(title):
        fail(FAIL_NOTITLE)
    
    entry = makeGrubEntry(title, os_type, root, kernel, initrd, options)
    
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
    if not root_grub:
        fail(FAIL_NODEVICE)
    
    entries = []
    versions = {}
    for x in grub.config.entries:
        entry = parseGrubEntry(x)
        if entry["root"] == root:
            if entry["os_type"] in ["linux", "xen"]:
                kernel = entry["kernel"].split("/")[-1]
                try:
                    k_version, k_suffix = parseVersion(kernel)
                except ParseError:
                    continue
                if k_suffix == new_suffix:
                    versions[k_version] = x
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
    
    make_default = False
    if default_entry in entries:
        make_default = True
    
    updated_index = None
    action = None
    if not len(entries):
        action = "append"
    else:
        if new_version in versions:
            if make_default:
                updated_index = grub.config.indexOf(versions[new_version])
        else:
            action = "insert"
    
    if action:
        release = open("/etc/pardus-release", "r").readline().strip()
        title = "%s [%s%s]" % (release, new_version, new_suffix)
        
        os_type = "linux"
        if new_suffix == "-dom0":
            os_type = "xen"
        
        if action == "append":
            index = -1
            boot_parameters = bootParameters(root)
        else:
            index = grub.config.indexOf(entries[0])
            boot_parameters = parseGrubEntry(entries[0])["options"]
        
        kernel = "/boot/kernel-%s%s" % (new_version, new_suffix)
        initrd = "/boot/initrmfs-%s%s" % (new_version, new_suffix)
        new_entry = makeGrubEntry(title, os_type, root, kernel, initrd, boot_parameters)
        
        if grub.config.getOption("default", "0") == "saved":
            new_entry.setCommand("savedefault", "")
        
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
