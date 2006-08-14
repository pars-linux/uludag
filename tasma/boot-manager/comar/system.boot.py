def rootDevice():
    """Returns root device address."""
    root = ""
    for i in [i.split() for i in open("/etc/mtab", "r").read().split("\n")]:
        if i[1] == "/":
            root = i[0].split("/")[-1]
            break
    return root

def toGrubDevice(dev):
    """Converts /dev address to grub address."""
    return "(%s%s,%s)" % (dev[0:2], ord(dev[2]) - 97, int(dev[3:]) - 1)

def bootParams():
    """Gets boot parameters from cmdline."""
    s = []
    for i in [x for x in open("/proc/cmdline", "r").read().split() if not x.startswith("cdroot") if not x.startswith("init=")]:
        if i.startswith("root="):
            s.append("root=/dev/%s" % rootDevice())
        elif i.startswith("mudur="):
            mudur = "mudur="
            for p in i[len("mudur="):].split(','):
                if p == "livecd": continue
                mudur += p
            if not len(mudur) == len("mudur="):
                s.append(mudur)
        else:
            s.append(i)
    return " ".join(s).strip()

def parseGrubConfig(filename):
    """Parses given Grub configuration file and returns options and entries."""
    lines = [i.strip() for i in file(filename) if not i.startswith("#") and i.strip()]

    options = {}
    entries = []
    entry = []

    for i in lines:
        if i.find(" ") == -1:
            label = i
            data = ""
        else:
            label = i[0:i.find(" ")].rstrip(" =")
            data = i[i.find(" ") + 1:].lstrip(" =")

        if label == "title":
            if entry:
                entries.append(entry)
                entry = []
            entry.append("title %s" % data)
        elif not entry:
            options[label] = data
        elif entry:
            if data:
                entry.append("%s %s" % (label, data))
            else:
                entry.append("%s" % label)

    if entry:
        entries.append(entry)

    return options, entries

def saveGrubConfig(filename, opts={}, entries=[]):
    """Produces Grub configuration from given options and entries."""
    s = ""

    for label, data in opts.iteritems():
        if data:
            s += "%s %s\n" % (label, data)
        else:
            s += "%s\n" % label

    s += "\n"

    for entry in entries:
        s += "\n".join(entry)
        s += "\n\n"

    f = file(filename, "w")
    f.write(s)
    f.close()

grubconf = "/boot/grub/grub.test.conf"

def listOptions():
    """Returns list of options."""
    options, entries = parseGrubConfig(grubconf)
    return "\n".join(options.keys())

def getOption(key):
    """Returns value of an option."""
    options, entries = parseGrubConfig(grubconf)
    if key in options:
        return "%s\n%s" % (key, options[key])

def setOption(key, value=None):
    """Sets or unsets an option."""
    options, entries = parseGrubConfig(grubconf)

    if value:
        options[key] = value
    else:
        del options[key]

    saveGrubConfig(grubconf, options, entries)

    if value:
        notify("System.Boot.changed", "option_changed %s" % key)
    else:
        notify("System.Boot.changed", "option_removed %s" % key)

def listEntries():
    """Returns list of entries."""
    options, entries = parseGrubConfig(grubconf)

    return "\n".join([i[0][6:] for i in entries])

def getEntry(index):
    """Returns details of an entry."""
    index = int(index)
    options, entries = parseGrubConfig(grubconf)

    if index < len(entries):
        entries[index].insert(0, str(index))
        return "\n".join(entries[index])
    else:
        fail("No such entry")

def addEntry(title, commands, index=-1):
    """Adds new entry"""
    index = int(index)
    options, entries = parseGrubConfig(grubconf)

    entry = ["title %s" % title]
    entry += commands.split("\n")

    if entry in entries:
        fail("Duplicate entry.")
        return

    if index == -1:
        entries.append(entry)
        index = len(entries) - 1
    else:
        entries.insert(index, entry)

    saveGrubConfig(grubconf, options, entries)

    notify("System.Boot.changed", "entry_added %s" % index)
    return index

def updateEntry(index, title="", commands=""):
    """Adds new entry"""
    index = int(index)
    options, entries = parseGrubConfig(grubconf)

    if index < len(entries):
        if title:
            entry = ["title %s" % title]
        else:
            entry = [entries[index][0]]

        if commands:
            entry += commands.split("\n")
        else:
            entry += entries[index][1:]

        entries[index] = entry
        saveGrubConfig(grubconf, options, entries)

        notify("System.Boot.changed", "entry_changed %s" % index)
    else:
        fail("No such entry.")

def addKernel(release):
    """Adds new kernel."""
    options, entries = parseGrubConfig(grubconf)

    root = rootDevice()
    root_g = toGrubDevice(root)

    try:
        name = open("/etc/pardus-release", "r").read().strip()
    except:
        name = "Linux"

    title = "%s (kernel-%s)" % (name, release)

    entry = ["title %s " % title,
             "kernel %s/boot/kernel-%s %s" % (root_g, release, bootParams()),
             "root %s" % root_g,
             "initrd /boot/initramfs-%s" % release]
    entries.append(entry)
    index = len(entries) - 1

    saveGrubConfig(grubconf, options, entries)
    notify("System.Boot.changed", "entry_added %s" % index)
    return entries.index(entry)

def removeEntry(index):
    """Removes entry at index."""
    index = int(index)
    options, entries = parseGrubConfig(grubconf)

    if index < len(entries):
        del entries[index]
        saveGrubConfig(grubconf, options, entries)
        notify("System.Boot.changed", "entry_removed %s" % index)
    else:
        fail("No such entry")
