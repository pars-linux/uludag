#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from zorg.parser import *
from zorg.utils import *
from zorg import ddc
from zorg import modeline

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
        self.probed = False
        self.wide = False
        self.digital = False
        self.panel_w = 0
        self.panel_h = 0
        self.hsync_min = 0
        self.hsync_max = 0
        self.vref_min = 0
        self.vref_max = 0
        self.modelines = []
        self.res = ["800x600", "640x480"]
        self.vendorname = "Unknown"
        self.modelname = "Unknown"
        self.eisaid = ""
        self.depth = "16"

class Screen:
    def __init__(self, device=None, monitor=None):
        self.identifier = None
        self.number = None
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

def queryDDC(adapter=0):
    mon = Monitor()

    edid = ddc.query(adapter)

    if not edid:
        mon.probed = False
        return mon
    else:
        mon.probed = True

    mon.eisaid = edid["eisa_id"]
    mon.digital = edid["input_digital"]

    if edid["version"] != 1 and edid["revision"] != 3:
        return mon

    detailed = edid["detailed_timing"]

    mon.hsync_min, mon.hsync_max = detailed["hsync_range"]
    mon.vref_min, mon.vref_max = detailed["vref_range"]

    mon.modelines = "" # TODO: Write modelines if needed

    # FIXME: When subsystem is ready, review these.

    #modes = edid["standard_timings"] + edid["established_timings"]

    m = modeline.calcFromEdid(edid)
    dtmode = m["mode"] + (m["vfreq"],)

    modes = edid["standard_timings"] + (dtmode,)

    res = set((x, y) for x, y, z in modes if x > 800 and y > 600)
    res = list(res)

    res.sort(reverse=True)

    mon.res[:0] = ["%dx%d" % (x, y) for x, y in res]

    if mon.hsync_max == 0 or mon.vref_max == 0:
        hfreqs = vfreqs = []
        for w, h, vfreq in modes:
            vals = {
                "hPix" : w,
                "vPix" : h,
                "vFreq" : vfreq
            }
            m = modeline.ModeLine(vals)
            hfreqs.append(m["hFreq"] / 1000.0) # in kHz
            vfreqs.append(m["vFreq"])

        if len(hfreqs) > 2 and len(vfreqs) > 2:
            hfreqs.sort()
            vfreqs.sort()
            mon.hsync_min, mon.hsync_max = hfreqs[0], hfreqs[-1]
            mon.vref_min, mon.vref_max = vfreqs[0], vfreqs[-1]


    for m in mon.modelines:
        t = m[m.find("ModeLine"):].split()[1].strip('"')
        if t not in mon.res:
            mon.res[:0] = [t]

    return mon

def queryPanel(mon, card):
    #if xisrunning():
    #    return

    p = XorgParser()
    sec = XorgSection("Device")
    sec.setValue("Identifier", "Card0")
    sec.setValue("Driver", card.driver)
    p.sections.append(sec)

    sec = XorgSection("Monitor")
    sec.setValue("Identifier", "Monitor0")
    p.sections.append(sec)

    sec = XorgSection("Screen")
    sec.setValue("Identifier", "Screen0")
    sec.setValue("Device", "Card0")
    p.sections.append(sec)

    open(xorg_conf, "w").write(str(p))

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
    #if not mon.eisaid:
    #    if mon.panel_h and mon_panel_w:
    #        #mon.modelines = calcModeLine(mon.panel_w, mon.panel_h, 60)
    #        mon.res[:0] = ["%dx%d" % (mon.panel_w, mon.panel_h)]

    if mon.panel_w > 800 and mon.panel_h > 600:
        panel_res = "%dx%d" % (mon.panel_w, mon.panel_h)
        if mon.res[0] != panel_res:
            mon.res[:0] = ["%dx%d" % (mon.panel_w, mon.panel_h)]
        #if not mon.eisaid:
            # FIXME: add modelines here

def findMonitors(cards):
    monitors = []

    # vbeInfo = ddc.vbeInfo()
    # Maybe we can learn the maximum resolution from vbeInfo["mode_list"] ?

    for adapter in xrange(len(cards)):
        mon = queryDDC(adapter)

        # defaults for the case where ddc fails
        if mon.hsync_min == 0 or mon.vref_min == 0:
            mon.hsync_min = 31.5
            mon.hsync_max = 50
            mon.vref_min = 50
            mon.vref_max = 70

        if mon.eisaid:
            for line in loadFile(MonitorsDB):
                l = line.split(";")
                if mon.eisaid == l[2].strip().upper():
                    mon.vendorname = l[0].lstrip()
                    mon.modelname = l[1].lstrip()
                    mon.hsync_min, mon.hsync_max = map(float, l[3].strip().split("-"))
                    mon.vref_min, mon.vref_max = map(float, l[4].strip().split("-"))

        # check lcd panel
        if mon.digital and (cards[adapter].driver in lcd_drivers):
            queryPanel(mon, cards[adapter])

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

class XConfig:
    def __init__(self):
        self._parser = XorgParser()

        self._priScreen = None
        self._secScreen = None

        self.layout = None
        self.defaultScreen = None

    def new(self):
        secModule = XorgSection("Module")
        secdri = XorgSection("dri")
        secFiles = XorgSection("Files")
        secFlags = XorgSection("ServerFlags")
        secKeyboard = XorgSection("InputDevice")
        secMouse = XorgSection("InputDevice")

        self._parser.sections = [
            secModule,
            XorgSection("Extensions"),
            secdri,
            secFiles,
            secFlags,
            secKeyboard,
            secMouse
        ]

        modules = ("dbe", "type1", "freetype", "record", "xtrap", "glx", "dri", "v4l", "extmod")

        for module in modules:
            self.addModule(module)

        extmod = XorgSection("extmod")
        extmod.options = {"omit xfree86-dga" : unquoted()}
        secModule.sections = [extmod]

        secdri.set("Mode", unquoted("0666"))

        secFiles.set("RgbPath", "/usr/lib/X11/rgb")
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
            secFiles.add("FontPath", fontPath)

        secFlags.options = {
            "AllowMouseOpenFail" : "true",
            "BlankTime" : "0",
            "StandbyTime" : "0",
            "SuspendTime" : "0",
            "OffTime" : "0"
        }

        secKeyboard.set("Identifier", "Keyboard0")
        secKeyboard.set("Driver", "kbd")
        secKeyboard.options = {
            "AutoRepeat" : "500 30",
            "XkbModel" : "pc105",
            "XkbLayout" : "trq" # FIXME: query this
        }

        secMouse.set("Identifier", "Mouse0")
        secMouse.set("Driver", "mouse")
        secMouse.options = {
            "Protocol" : "ExplorerPS/2",
            "Device" : "/dev/input/mice",
            "ZAxisMapping" : "4 5 6 7",
            "Buttons" :  "5"
        }

    def load(self):
        self._parser.parseFile(xorg_conf)

    def save(self):
        f = open(xorg_conf, "w")
        f.write(self._parser.toString())
        f.close()

    def addModule(self, moduleName):
        p = self._parser.getSections("Module")[0]
        p.add("Load", moduleName)

    def modules(self):
        p = self._parser.getSections("Module")[0]
        return [e.values[0] for e in p.entries]

    def setFlag(self, flag, value):
        p = self._parser.getSections("ServerFlags")[0]
        p.options[flag] = value

    def flags(self):
        p = self._parser.getSections("ServerFlags")[0]
        return p.options

    def setKeyboard(self, **options):
        s = self._parser.getSections("InputDevice")
        for p in s:
            if p.get("Driver") == "kbd":
                p.options.update(options)
                return

    def keyboardOptions(self):
        s = self._parser.getSections("InputDevice")
        for p in s:
            if p.get("Driver") == "kbd":
                return p.options

    def setMouse(self, **options):
        s = self._parser.getSections("InputDevice")
        for p in s:
            if p.get("Driver") == "mouse":
                p.options.update(options)
                return

    def mouseOptions(self):
        s = self._parser.getSections("InputDevice")
        for p in s:
            if p.get("Driver") == "mouse":
                return p.options

    def addTouchpad(self, dev_type):
        if dev_type in touchpadDevices:
            secTouchpad = XorgSection("InputDevice")
            secTouchpad.set("Identifier", "Touchpad")
            secTouchpad.set("Driver", "synaptics")
            secTouchpad.options = touchpadDevices[dev_type]

            self._parser.sections.append(secTouchpad)

    def setTouchpad(self, dev_type):
        s = self._parser.getSections("InputDevice")
        for p in s:
            if p.get("Driver") == "synaptics":
                p.options.update(touchpadDevices[dev_type])
                return

        self.addTouchpad(dev_type)

    def touchpadOptions(self):
        s = self._parser.getSections("InputDevice")
        for p in s:
            if p.get("Driver") == "synaptics":
                return p.options

    def _addDevice(self, dev):
        sec = XorgSection("Device")
        sec.set("Screen", 0)
        sec.set("Identifier", dev.identifier)
        sec.set("Driver", dev.driver)
        sec.set("VendorName", dev.vendorName)
        sec.set("BoardName", dev.boardName)

        self._parser.sections.append(sec)
        return sec

    def _addMonitor(self, mon):
        sec = XorgSection("Monitor")
        sec.set("Identifier", mon.identifier)
        sec.set("VendorName", mon.vendorname)
        sec.set("ModelName", mon.modelname)
        sec.set("HorizSync", mon.hsync_min, unquoted("-"), mon.hsync_max)
        sec.set("VertRefresh", mon.vref_min, unquoted("-"), mon.vref_max)

        self._parser.sections.append(sec)
        return sec

    def _addScreen(self, scr):
        sec = XorgSection("Screen")
        sec.set("Identifier", scr.identifier)
        sec.set("Device", scr.device.identifier)
        sec.set("Monitor", scr.monitor.identifier)
        sec.set("DefaultDepth", scr.depth)

        subsec = XorgSection("Display")
        subsec.set("Depth", scr.depth)
        #modes = ["%sx%s" % (x, y) for x, y in scr.modes]
        subsec.set("Modes", *scr.modes)

        sec.sections = [subsec]
        self._parser.sections.append(sec)
        return sec

    def setPrimaryScreen(self, screen):
        dev = screen.device
        mon = screen.monitor

        screen.number = 0
        screen.setup()

        secDev = self._addDevice(dev)
        secMon = self._addMonitor(mon)
        secScr = self._addScreen(screen)

        self._priScreen = screen

    def setSecondaryScreen(self, screen):
        pass

    def getPrimaryScreen(self):
        pass

    def getSecondaryScreen(self):
        pass

    def finalize(self):
        sec = XorgSection("ServerLayout")

        if self.layout == PROBE:
            sec.set("Identifier", "Configured by zorg for probe")
            e = XorgEntry()
            e.key = "Screen"
            e.values = [0, "Screen0", 0, 0]
            sec.entries.append(e)

        elif self.layout == SINGLE_HEAD:
            if self._priScreen:
                self.defaultScreen = self._priScreen
            else:
                self.defaultScreen = self._secScreen

            sec.set("Identifier", "SingleHead")
            sec.set("Screen", self.defaultScreen.identifier)

            inputDevices = {
                "Mouse0" : "CorePointer",
                "Keyboard0" : "CoreKeyboard"
            }
            if self.touchpadOptions():
                self.addModule("synaptics")
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

        self._parser.sections.append(sec)

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

        self.parser.sections = [
            secModule,
            XorgSection("Extensions"),
            secdri,
            secFiles,
            secFlags,
            secKeyboard,
            secMouse
        ]

        if self.touchpad in touchpadDevices:
            secTouchpad = XorgSection("InputDevice")
            secTouchpad.setValue("Identifier", "Touchpad")
            secTouchpad.setValue("Driver", "synaptics")
            secTouchpad.options = touchpadDevices[self.touchpad]

            self.parser.sections.append(secTouchpad)

    def setupScreens(self):
        mon0 = self.screens[0].monitor
        mon1 = self.screens[1].monitor

        if not mon0.probed and mon1.probed:
            self.screens.reverse()

        i = 0
        self.devices = []
        self.monitors = []
        for scr in self.screens:
            scr.number = i
            scr.setup()

            self.devices.append(scr.device)
            self.monitors.append(scr.monitor)

            i += 1

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
    # detect graphic card and find monitor of first card
    devices = findVideoCards()
    if devices:
        device = devices[0]
        device.query()
    else:
        return

    # save active cards for checking next boots.
    #saveActiveCard(cards)

    # we need card data to check for lcd displays
    monitors = findMonitors((device, device))

    if len(monitors) > 1 and \
        not monitors[0].probed and monitors[1].probed:
        monitor = monitors[1]
    else:
        monitor = monitors[0]

    screen = Screen(device, monitor)
    screen.res = monitor.res[0]

    config = XConfig()
    config.new()
    config.setKeyboard(XkbLayout=queryKeymap())
    config.setTouchpad(queryTouchpad())
    config.setPrimaryScreen(screen)

    config.layout = SINGLE_HEAD
    config.finalize()
    config.save()

def safeConfigure(driver = "vesa"):
    safedrv = driver.upper()

    dev = Device()
    dev.boardName = "%s Configured Board" % safedrv
    dev.vendorName = "%s Configured Vendor" % safedrv
    dev.driver = driver

    # set failsafe monitor stuff
    mon = Monitor()
    mon.vendorname = "%s Configured Vendor" % safedrv
    mon.modelname = "%s Configured Model" % safedrv

    mon.hsync_min = 31.5
    mon.hsync_max = 50
    mon.vref_min = 50
    mon.vref_max = 70

    screen = Screen(dev, mon)
    screen.depth = 16
    screen.modes = ["800x600", "640x480"]

    config = XConfig()
    config.new()
    config.setKeyboard(XkbLayout=queryKeymap())
    config.setPrimaryScreen(screen)

    config.layout = SINGLE_HEAD
    config.finalize()
    config.save()

if __name__ == "__main__":
    #safeConfigure()
    autoConfigure()
