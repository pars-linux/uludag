#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from zorg.parser import *
from zorg.utils import *

xorg_conf = "/etc/X11/xorg.conf"
activeCards = "/etc/X11/activeCards"
xorg_off = "/var/run/xorg_off"
xdriverlist = "/usr/lib/X11/xdriverlist"
MonitorsDB = "/usr/lib/X11/MonitorsDB"

driver_path = "/usr/lib/xorg/modules/drivers"
xkb_path = "/usr/share/X11/xkb/symbols/pc"

truecolor_cards = ["i810", "intel", "nv", "nvidia", "radeon", "fglrx"]
lcd_drivers = ["nv", "nvidia", "ati", "via", "i810", "intel", "sis", "savage", "neomagic"]
default_kmap = "trq"

PROBE, SINGLE_HEAD, DUAL_HEAD = 0, 1, 2
#DH_CLONE, DH_XINERAMA = 0, 1

synapticsOptions = {
    "Protocol" : "auto-dev",
    # "Device" : "/dev/input/mouse0",
    "LeftEdge" : "1700",
    "RightEdge" : "5300",
    "TopEdge" : "1700",
    "BottomEdge" : "4200",
    "FingerLow" : "25",
    "FingerHigh" : "30",
    "MaxTapTime" : "180",
    "MaxTapMove" : "220",
    "VertScrollDelta" : "100",
    "MinSpeed" : "0.09",
    "MaxSpeed" : "0.18",
    "AccelFactor" : "0.0015",
    "SHMConfig" : "true",
    # Option     "ClickTime" : "0"
}

alpsOptions = {
    "Protocol" : "auto-dev",
    "LeftEdge" : "130",
    "RightEdge" : "840",
    "TopEdge" : "130",
    "BottomEdge" : "640",
    "FingerLow" : "7",
    "FingerHigh" : "8",
    "MaxTapTime" : "300",
    "MaxTapMove" : "110",
    "EmulateMidButtonTime" : "75",
    "VertScrollDelta" : "20",
    "HorizScrollDelta" : "20",
    "MinSpeed" : "0.60",
    "MaxSpeed" : "1.10",
    "AccelFactor" : "0.030",
    "EdgeMotionMinSpeed" : "200",
    "EdgeMotionMaxSpeed" : "200",
    "UpDownScrolling" : "1",
    "CircularScrolling" : "1",
    "CircScrollDelta" : "0.1",
    "CircScrollTrigger" : "2",
    "SHMConfig" : "true",
    "Emulate3Buttons" : "true",
    # "ClickTime" : "0"
}

touchpadDevices = {"synaptics" : synapticsOptions,
                   "alps"      : alpsOptions}

class Device:
    def __init__(self, vendorId=None, deviceId=None):
        self.identifier = None
        self.vendorId = vendorId
        self.deviceId = deviceId

        self.busId = None
        self.pciId = "%s:%s" % (vendorId, deviceId)

        self.driver = None
        self.vendorName = "Unknown"
        self.boardName = "Unknown"

        self.monitors = None

    # not needed
    def __str__(self):
        return "%s@%s" % (self.pciId, self.busId)

    def query(self):
        self.vendorName, self.boardName = queryPCI(self.vendorId, self.deviceId)
        availableDrivers = listAvailableDrivers()

        for line in loadFile(xdriverlist):
            if line.startswith(self.vendorId + self.deviceId):
                drv = line.rstrip("\n").split(" ")[1]
                if drv in availableDrivers:
                    self.driver = drv

        # if could not find driver from driverlist try X -configure
        if not self.driver:
            ret = run("/usr/bin/X", ":1", "-configure", "-logfile", "/var/log/xlog")
            if ret == 0:
                home = os.getenv("HOME", "")
                #cfg = XorgConfig()
                #cfg.parse(home + "/xorg.conf.new")
                #unlink(home + "/xorg.conf.new")
                #devs = cfg.devices
                #if devs:
                #    self.driver = devs[0].driver
                p = XorgParser()
                p.parseFile(home + "/xorg.conf.new")
                unlink(home + "/xorg.conf.new")
                sec = p.getSections("Device")
                if sec:
                    self.driver = sec[0].value("Driver")

        # use nvidia if nv is found
        if (self.driver == "nv") and ("nvidia" in availableDrivers):
            self.driver = "nvidia"

        # In case we can't parse or find xorg.conf.new
        if not self.driver:
            self.driver = "vesa"

class Monitor:
    def __init__(self):
        self.identifier = None
        self.wide = 0
        self.panel_w = 0
        self.panel_h = 0
        self.hsync_min = 0
        self.hsync_max = 0
        self.vref_min = 0
        self.vref_max = 0
        self.modelines = []
        self.res = []
        self.vendorname = "Unknown"
        self.modelname = "Unknown"
        self.eisaid = ""
        self.depth = "16"

class Screen:
    def __init__(self, number=0, device=None, monitor=None):
        self.identifier = None
        self.number = number
        self.device = device
        self.monitor = monitor
        self.depth = 16
        self.modes = ["800x600", "640x480"]
        self.res = "800x600"

    def setup(self):
        self.identifier = "Screen%d" % self.number
        self.monitor.identifier = "Monitor%d" % self.number
        self.device.identifier = "VideoCard%d" % self.number

        if self.device.driver in truecolor_cards:
            self.depth = 24

        if self.res in self.monitor.res:
            i = self.monitor.res.index(self.res)
            self.modes = self.monitor.res[i:]

def saveActiveCard(cards):
    f = file(activeCards, "w")
    for card in cards:
        f.write("%s\n" % card.PciId)
    f.close()

def queryTouchpad():
    try:
        a = file("/proc/bus/input/devices")
        for line in a.readlines():
            # Frequently check if kernel does not break anything
            if "SynPS/2" in line:
                return "synaptics"
            elif "AlpsPS/2" in line:
                return "alps"
        a.close()
    except:
        pass
    return ""

def getKeymapList():
    return os.listdir(xkb_path)

def queryKeymap():
    # Fallback is trq
    kmap = default_kmap
    keymap_file = "/etc/mudur/keymap"
    try:
        if os.path.exists(keymap_file):
            kmap = file(keymap_file).read().strip().rstrip("\n")
    except:
        pass

    # workaround for pt_BR and some latin1 variants
    if "-" in kmap:
        kmap = kmap.split("-", 1)[0]

    if not kmap in getKeymapList():
        kmap = default_kmap

    return kmap

def listAvailableDrivers(d = driver_path):
    a = []
    if os.path.exists(d):
        for drv in os.listdir(d):
            if drv.endswith("_drv.so"):
                if drv[:-7] not in a:
                    a.append(drv[:-7])
    return a

def queryPCI(vendor, device):
    f = file("/usr/share/misc/pci.ids")
    flag = 0
    company = ""
    for line in f.readlines():
        if flag == 0:
            if line.startswith(vendor):
                flag = 1
                company = line[5:].strip()
        else:
            if line.startswith("\t"):
                if line.startswith("\t" + device):
                    return company, line[6:].strip()
            elif not line.startswith("#"):
                flag = 0
    return None, None

def findVideoCards():
    """ Finds video cards. Result is a list of Device objects. """
    cards = []

    # read only PCI for now, follow sysfs changes
    for bus in ["pci"]:
        sysDir = os.path.join("/sys/bus", bus, "devices")
        if os.path.isdir(sysDir):
            for _dev in os.listdir(sysDir):
                #try:
                    if sysValue(sysDir, _dev, "class").startswith("0x03"):
                        vendorId = lremove(sysValue(sysDir, _dev, "vendor"), "0x")
                        deviceId = lremove(sysValue(sysDir, _dev, "device"), "0x")
                        busId = tuple(int(x, 16) for x in _dev.replace(".",":").split(":"))[1:4]

                        a = Device(vendorId, deviceId)
                        a.busId = "PCI:%d:%d:%d" % busId
                        cards.append(a)
                #except:
                #    pass

    #for i in xrange(len(cards)):
    #    cards[i].identifier = "VideoCard%d" % i

    if len(cards):
        return cards
    else:
        # This machine might be a terminal server with no video cards.
        # We start X and leave the decision to the user.
        #sys.exit(0)
        return None

def queryDDC():
    mon = Monitor()

    ddc = capture("/usr/sbin/ddcxinfos")
    if ddc[1] != '':
        return mon

    for line in ddc[0].split("\n"):
        t = line.find("truly")
        if t != -1:
            mon.wide = atoi(line[t+6:])
        t = line.find("EISA ID=")
        if t != -1:
            mon.eisaid = line[line.find("EISA ID=")+8:].upper().strip()
        t = line.find("kHz HorizSync")
        if t != -1:
            mon.hsync_min = atoi(line)
            mon.hsync_max = atoi(line[line.find("-") + 1:])
        t = line.find("Hz VertRefresh")
        if t != -1:
            mon.vref_min = atoi(line)
            mon.vref_max = atoi(line[line.find("-") + 1:])
        if line[:8] == "ModeLine":
            mon.modelines.append("    %s\n" % line)

    if mon.hsync_max == 0 or mon.vref_max == 0:
        # in case those not probed separately, get them from modelines
        freqs = filter(lambda x: x.find("hfreq=") != -1, ddc[1])
        if len(freqs) > 1:
            line = freqs[0]
            mon.hsync_min = atoi(line[line.find("hfreq=") + 6:])
            mon.vref_min = atoi(line[line.find("vfreq=") + 6:])
            line = freqs[-1]
            mon.hsync_max = atoi(line[line.find("hfreq=") + 6:])
            mon.vref_max = atoi(line[line.find("vfreq=") + 6:])

    if mon.eisaid != "":
        for line in loadFile(MonitorsDB):
            l = line.split(";")
            if mon.eisaid == l[2].strip().upper():
                mon.vendorname = l[0].lstrip()
                mon.modelname = l[1].lstrip()
                mon.hsync_min, mon.hsync_max = map(float, l[3].strip().split("-"))
                mon.vref_min, mon.vref_max = map(float, l[4].strip().split("-"))

    for m in mon.modelines:
        t = m[m.find("ModeLine"):].split()[1].strip('"')
        if t not in mon.res:
            mon.res[:0] = [t] #= t + " " + mon.res

    if not mon.res:
        mon.res = ["800x600", "640x480"]

    return mon

def queryPanel(mon):
    #if xisrunning():
    #    return

    patterns = [
        "Panel size is",
        "Panel Size is",
        "Panel Size from BIOS:",
        "Panel size: ",
        "Panel Native Resolution is ",
        "Panel is a ",
        "Detected panel size via",
        "Detected panel size via BIOS: ",
        "Size of device LFP (local flat panel) is",
        "Size of device LFP",
        "Size of device DFP",
        "Virtual screen size determined to be ",
        "Detected LCD/plasma panel ("
    ]

    a = run("/usr/bin/X", ":1", "-probeonly", "-allowMouseOpenFail", "-logfile", "/var/log/xlog")
    if a != 0:
        return

    f = file("/var/log/xlog")
    for line in f.readlines():
        for p in patterns:
            if p in line:
                b = line[line.find(p)+len(p):]
                mon.panel_w = atoi(b)
                b = b[b.find("x")+1:]
                mon.panel_h = atoi(b)
                break
    f.close()

    # modelines stuff
    if not mon.eisaid:
        if mon.panel_h and mon_panel_w:
            #mon.modelines = calcModeLine(mon.panel_w, mon.panel_h, 60)
            mon.res[:0] = ["%dx%d" % (mon.panel_w, mon.panel_h)]

def findMonitors(cards):
    monitors = []
    # FIXME: modify ddcxinfos to probe for more monitors
    # probe monitor freqs, for the first monitor for now
    mon = queryDDC()

    # defaults for the case where ddc fails
    if mon.hsync_min == 0 or mon.vref_min == 0:
        mon.hsync_min = 31.5
        mon.hsync_max = 50
        mon.vref_min = 50
        mon.vref_max = 70

    # check lcd panel
    if cards[0].driver in lcd_drivers:
        p = XorgParser()
        sec = XorgSection("Device")
        sec.setValue("Identifier", "Card0")
        sec.setValue("Driver", "nv")
        p.sections.append(sec)

        sec = XorgSection("Monitor")
        sec.setValue("Identifier", "Monitor0")
        p.sections.append(sec)

        sec = XorgSection("Screen")
        sec.setValue("Identifier", "Screen0")
        sec.setValue("Device", "Card0")
        p.sections.append(sec)

        open(xorg_conf, "w").write(str(p))

        queryPanel(mon)

    mon.identifier = "Monitor0"
    monitors.append(mon)
    return monitors


def getActiveCards():
    if os.path.exists(activeCards):
        cards = []
        lines = file(activeCards,'r').readlines()
        for card in lines:
            pciId, busId = card.rstrip("\n").split("@")
            cards.append((pciId.split(":"), busId))
        return cards
    else:
        return None

class XorgConfig:
    def __init__(self):
        self.devices = []
        self.monitors = []
        self.screens = []

        #self.layoutType = 0 # Simple layout. Others: Clone, Xinerama, etc ...
        self.layout = PROBE
        self.dual = False

        self.extensions = {}
        self.serverFlags = {
            "AllowMouseOpenFail" : "true",
            "BlankTime" : "0",
            "StandbyTime" : "0",
            "SuspendTime" : "0",
            "OffTime" : "0"
        }

        self.touchpad = None
        self.keyboardLayout = "trq"
        self.mouse = {
            "ZAxisMapping" : "4 5 6 7",
            "Buttons" : "5"
        }

        self.parser = XorgParser()
        #self.parser = None

    def parse(self, fileName):
        """ Parses the Xorg configuration file """
        #self.reset()
        self.parser.parseFile(fileName)

        # Extensions
        sec = self.parser.getSections("Extensions")[0]

        composite = sec.options.get("Composite")
        if composite:
            self.extensions["Composite"] = xBool[composite.lower() in trueList]

        # Server flags
        sec = self.parser.getSections("ServerFlags")[0]
        self.serverFlags.update(sec.options)

        # Input devices
        for sec in self.parser.getSections("InputDevice"):
            drv = sec.value("Driver")
            if drv == "kbd":
                kbd = sec
            elif drv == "mouse":
                mouse = sec

        if kbd:
            self.keyboardLayout = kbd.options.get("XkbLayout", "trq")

        if mouse:
            self.mouse.update(mouse.options)

        # Devices
        devsecs = self.parser.getSections("Device")
        if not devsecs:
            return

        self.devices = []
        #cards = getActiveCards()
        cards = None

        for sec in devsecs:
            if cards:
                (vendorId, deviceId), busId = cards.pop(0)
            else:
                vendorId, deviceId = None, None
                busId = None

            dev = Device(vendorId, deviceId)
            dev.identifier = sec.value("Identifier")
            dev.number = sec.value("Screen")
            dev.busId = busId
            dev.driver = sec.value("Driver")
            dev.vendorName = sec.value("VendorName")
            dev.boardName = sec.value("BoardName")
            self.devices.append(dev)

        # Monitors
        monsecs = self.parser.getSections("Monitor")
        if not monsecs:
            return

        self.monitors = []
        for sec in monsecs:
            mon = Monitor()
            mon.identifier = sec.value("Identifier")
            mon.vendorname = sec.value("VendorName")
            mon.modelname = sec.value("ModelName")

            def getRange(values):
                r = "".join(map(str, values))
                return map(float, r.split("-"))

            horizSync = sec.entry("HorizSync")
            vertRefresh = sec.entry("VertRefresh")
            if horizSync and vertRefresh:
                mon.hsync_min, mon.hsync_max = getRange(horizSync.values)
                mon.vref_min, mon.vref_max = getRange(vertRefresh.values)

            self.monitors.append(mon)

        def fromId(lst, identifier):
            for item in lst:
                if item.identifier == identifier:
                    return item

        # Screens
        scrsecs = self.parser.getSections("Screen")
        self.screens = []
        for sec in scrsecs:
            scr = Screen()
            scr.identifier = sec.value("Identifier")
            scr.device = fromId(self.devices, sec.value("Device"))
            scr.monitor = fromId(self.monitors, sec.value("Monitor"))

            scr.depth = sec.value("DefaultDepth")
            modes = sec.getSections("Display")[0].entry("Modes")
            if modes:
                scr.modes = modes.values
            #scr.modes = [map(int, x.split("x")) for x in modes]

            self.screens.append(scr)

        # Layouts
        secLayouts = self.parser.getSections("ServerLayout")
        for sec in secLayouts:
            identifier = sec.value("Identifier")
            if identifier == "SingleHead":
                self.layout = SINGLE_HEAD
                self.dual = False
            else:
                pass # Not implemented yet

    def update(self):
        if not self.parser:
            self.parser = XorgParser()
        parser = self.parser

        # Extensions
        secs = parser.getSections("Extensions")
        if secs:
            secs[0].options.update(self.extensions)

        # Server flags
        secFlags = parser.getSections("ServerFlags")
        if secFlags:
            secFlags[0].options.update(self.serverFlags)

        # Keyboard and mouse
        for sec in parser.getSections("InputDevice"):
            if sec.value("Driver") == "kbd":
                sec.options["XkbLayout"] = self.keyboardLayout
            elif sec.value("Driver") == "mouse":
                sec.options.update(self.mouse)

        # Clean first
        for sec in parser.getSections("Device", "Monitor", "Screen", "ServerLayout"):
            parser.sections.remove(sec)

        # Devices
        index = 0
        for dev in self.devices:
            sec = XorgSection("Device")
            sec.setValue("Screen", index)
            sec.setValue("Identifier", dev.identifier)
            sec.setValue("Driver", dev.driver)
            sec.setValue("VendorName", dev.vendorName)
            sec.setValue("BoardName", dev.boardName)

            if index: # This is for Vmware ?
                sec.setValue("BusID", dev.busId)

            parser.sections.append(sec)
            index += 1

        # Monitors
        for mon in self.monitors:
            sec = XorgSection("Monitor")
            sec.setValue("Identifier", mon.identifier)
            sec.setValue("VendorName", mon.vendorname)
            sec.setValue("ModelName", mon.modelname)
            sec.setValue("HorizSync", mon.hsync_min, unquoted("-"), mon.hsync_max)
            sec.setValue("VertRefresh", mon.vref_min, unquoted("-"), mon.vref_max)

            parser.sections.append(sec)

        # Screen
        for scr in self.screens:
            sec = XorgSection("Screen")
            sec.setValue("Identifier", scr.identifier)
            sec.setValue("Device", scr.device.identifier)
            sec.setValue("Monitor", scr.monitor.identifier)
            sec.setValue("DefaultDepth", scr.depth)

            subsec = XorgSection("Display")
            subsec.setValue("Depth", scr.depth)
            #modes = ["%sx%s" % (x, y) for x, y in scr.modes]
            subsec.setValue("Modes", *scr.modes)

            sec.sections = [subsec]
            parser.sections.append(sec)

    def save(self, fileName, update=True):
        if update:
            self.update()

        self.addLayouts()
        open(fileName, "w").write(str(self.parser))

    def reset(self):
        """ Resets configuration to default values.
        All the manual configuration made by user will be lost! """

        self.parser = XorgParser()

        secModule = XorgSection("Module")

        modules = ["dbe", "type1", "freetype", "record", "xtrap", "glx", "dri", "v4l", "extmod"]
        if self.touchpad in touchpadDevices:
            modules.append("synaptics")

        for module in modules:
            e = XorgEntry()
            e.key, e.values = "Load", [module]
            secModule.entries.append(e)

        extmod = XorgSection("extmod")
        extmod.options = {"omit xfree86-dga" : unquoted()}
        secModule.sections = [extmod]

        secdri = XorgSection("dri")
        secdri.setValue("Mode", unquoted("0666"))

        secFiles = XorgSection("Files")
        secFiles.setValue("RgbPath", "/usr/lib/X11/rgb")
        fontPaths = (
            "/usr/share/fonts/misc/",
            "/usr/share/fonts/dejavu/",
            "/usr/share/fonts/TTF/",
            "/usr/share/fonts/freefont/",
            "/usr/share/fonts/TrueType/",
            "/usr/share/fonts/corefonts",
            "/usr/share/fonts/Speedo/",
            "/usr/share/fonts/Type1/",
            "/usr/share/fonts/100dpi/",
            "/usr/share/fonts/75dpi/",
            "/usr/share/fonts/encodings/",
        )
        for fontPath in fontPaths:
            e = XorgEntry()
            e.key, e.values = "FontPath", [fontPath]
            secFiles.entries.append(e)

        secFlags = XorgSection("ServerFlags")
        secFlags.options = {
            "AllowMouseOpenFail" : "true",
            "BlankTime" : "0",
            "StandbyTime" : "0",
            "SuspendTime" : "0",
            "OffTime" : "0"
        }

        secKeyboard = XorgSection("InputDevice")
        secKeyboard.setValue("Identifier", "Keyboard0")
        secKeyboard.setValue("Driver", "kbd")
        secKeyboard.options = {
            "AutoRepeat" : "500 30",
            "XkbModel" : "pc105",
            "XkbLayout" : "trq" # FIXME: query this
        }

        secMouse = XorgSection("InputDevice")
        secMouse.setValue("Identifier", "Mouse0")
        secMouse.setValue("Driver", "mouse")
        secMouse.options = {
            "Protocol" : "ExplorerPS/2",
            "Device" : "/dev/input/mice",
            "ZAxisMapping" : "4 5 6 7",
            "Buttons" :  "5"
        }

        if self.touchpad:
            secTouchpad = XorgSection("InputDevice")
            secTouchpad.setValue("Identifier", "Touchpad")
            secTouchpad.setValue("Driver", "synaptics")
            secTouchpad.options = touchpadDevices[self.touchpad]

        self.parser.sections = [
            secModule,
            XorgSection("Extensions"),
            secdri,
            secFiles,
            secFlags,
            secKeyboard,
            secMouse
        ]

    def addLayouts(self):
        sec = XorgSection("ServerLayout")

        if self.layout == PROBE:
            sec.setValue("Identifier", "Configured by zorg for probe")
            e = XorgEntry()
            e.key = "Screen"
            e.values = [0, "Screen0", 0, 0]
            sec.entries.append(e)

        elif self.layout == SINGLE_HEAD:
            sec.setValue("Identifier", "SingleHead")
            sec.setValue("Screen", self.screens[0].identifier)

            inputDevices = {
                "Mouse0" : "CorePointer",
                "Keyboard0" : "CoreKeyboard"
            }
            if self.touchpad:
                inputDevices["Touchpad"] = "SendCoreEvents"

            for x, y in inputDevices.items():
                e = XorgEntry()
                e.key = "InputDevice"
                e.values = (x, y)
                sec.entries.append(e)

            sec.options = {
                "Xinerama" : "off",
                "Clone" : "off"
            }

        self.parser.sections.append(sec)

def autoConfigure():
    config = XorgConfig()
    config.reset()

    # detect graphic card and find monitor of first card
    devices = findVideoCards()
    for card in devices:
        card.query()

    if len(devices) == 1:
        import copy
        card = copy.deepcopy(devices[0])
        card.identifier = "VideoCard1"
        devices.append(card)

    #elif len(devices) > 2:
    #    devs = []
    #    for card in devices:
    #        function = atoi(card.busId.split(":")[-1])
    #        if function == 0:
    #            devs.append(card)


    # save active cards for checking next boots.
    #saveActiveCard(cards)

    # we need card data to check for lcd displays
    monitors = findMonitors(devices)

    index = len(monitors)
    while len(devices) > len(monitors):
        mon = Monitor()
        mon.identifier = "Monitor%d" % index
        mon.hsync_min = 31.5
        mon.hsync_max = 50
        mon.vref_min = 50
        mon.vref_max = 70
        mon.res = ["800x600", "640x480"]
        monitors.append(mon)
        index += 1

    for i in xrange(index):
        screen = Screen(i, devices[i], monitors[i])
        screen.res = monitors[i].res[0]
        screen.setup()

        config.screens.append(screen)

    config.devices = devices
    config.monitors = monitors

    config.keyboardLayout = queryKeymap()
    config.touchpad = queryTouchpad()

    config.layout = SINGLE_HEAD
    config.save(xorg_conf)

def safeConfigure(driver = "vesa"):
    safedrv = driver.upper()

    config = XorgConfig()
    config.reset()

    dev = Device()
    dev.identifier = "VideoCard0"
    dev.boardName = "%s Configured Board" % safedrv
    dev.vendorName = "%s Configured Vendor" % safedrv
    dev.driver = driver
    config.devices = [dev]

    # set failsafe monitor stuff
    mon = Monitor()
    mon.identifier = "Monitor0"

    mon.vendorname = "%s Configured Vendor" % safedrv
    mon.modelname = "%s Configured Model" % safedrv

    mon.hsync_min = 31.5
    mon.hsync_max = 50
    mon.vref_min = 50
    mon.vref_max = 70
    mon.res = ["800x600", "640x480"]
    config.monitors = [mon]

    screen = Screen(0, dev, mon)
    screen.identifier = "Screen0"
    screen.depth = 16
    screen.modes = ["800x600", "640x480"]
    config.screens = [screen]

    config.keyboardLayout = queryKeymap()
    config.layout = SINGLE_HEAD

    config.save(xorg_conf)

if __name__ == "__main__":
    #import pycallgraph
    #pycallgraph.start_trace()

    #from pyaspects.weaver import *
    #from pyaspects.debuggeraspect import DebuggerAspect
    #da = DebuggerAspect()
    #weave_all_class_methods(da, XorgParser)
    #weave_all_class_methods(da, XorgSection)
    #weave_all_class_methods(da, XorgEntry)

    #safeConfigure()
    autoConfigure()

    #pycallgraph.stop_trace()
    #pycallgraph.make_dot_graph("xman.png")


