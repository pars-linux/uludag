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
    def __init__(self, vendorId="", deviceId=""):
        self.identifier = None
        self.vendorId = vendorId
        self.deviceId = deviceId

        self.busId = ""
        self.pciId = "%s:%s" % (vendorId, deviceId)
        self.cardId = ""

        self.driver = None
        self.vendorName = "Unknown Vendor"
        self.boardName = "Unknown Board"

        self.monitors = []

    def query(self):
        self.cardId = "%s:%s@%s" % (self.vendorId, self.deviceId, self.busId)
        self.vendorName, self.boardName = queryPCI(self.vendorId, self.deviceId)
        availableDrivers = listAvailableDrivers()

        for line in loadFile(xdriverlist):
            if line.startswith(self.vendorId + self.deviceId):
                drv = line.rstrip("\n").split(" ")[1]
                if drv in availableDrivers:
                    self.driver = drv

        # if could not find driver from driverlist try X -configure
        if not self.driver:
            print "Running X server to query driver..."
            ret = run("/usr/bin/X", ":1", "-configure", "-logfile", "/var/log/xlog")
            if ret == 0:
                home = os.getenv("HOME", "")
                p = XorgParser()
                p.parseFile(home + "/xorg.conf.new")
                unlink(home + "/xorg.conf.new")
                sec = p.getSections("Device")
                if sec:
                    self.driver = sec[0].get("Driver")
                    print "Driver reported by X server is %s." % self.driver

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
        self.vendorname = "Unknown Vendor"
        self.modelname = "Unknown Model"
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
    modes = list(edid["standard_timings"])

    m = modeline.calcFromEdid(edid)
    if m:
        dtmode = m["mode"] + (m["vfreq"],)
        modes.append(dtmode)

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
    sec.set("Identifier", "Card0")
    sec.set("Driver", card.driver)
    p.sections.append(sec)

    sec = XorgSection("Monitor")
    sec.set("Identifier", "Monitor0")
    p.sections.append(sec)

    sec = XorgSection("Screen")
    sec.set("Identifier", "Screen0")
    sec.set("Device", "Card0")
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

    print "Running X server to query panel..."
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

    if mon.panel_w or mon.panel_h:
        print "Panel size reported by X server is %dx%d." % (mon.panel_w, mon.panel_h)

    if mon.panel_w > 800 and mon.panel_h > 600:
        panel_res = "%dx%d" % (mon.panel_w, mon.panel_h)
        if mon.res[0] != panel_res:
            mon.res[:0] = ["%dx%d" % (mon.panel_w, mon.panel_h)]
        #if not mon.eisaid:
            # FIXME: add modelines here

def findMonitors(card, *adapters):
    monitors = []

    for adapter in adapters:
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
        if mon.digital and (card.driver in lcd_drivers):
            queryPanel(mon, card)

        card.monitors.append(mon)
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

    def removeScreens(self):
        sections = self._parser.getSections("Device", "Monitor", "Screen")
        for sec in sections:
            self._parser.sections.remove(sec)

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

    def _addDevice(self, dev, screenNumber):
        sec = XorgSection("Device")
        sec.set("Screen", screenNumber)
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

        secDev = self._addDevice(dev, screen.number)
        secMon = self._addMonitor(mon)
        secScr = self._addScreen(screen)

        self._priScreen = screen

    def setSecondaryScreen(self, screen):
        #TODO: If nvidia module is used, use its own options to set 2nd screen.
        dev = screen.device
        mon = screen.monitor

        screen.number = 1
        screen.setup()

        secDev = self._addDevice(dev, screen.number)
        secMon = self._addMonitor(mon)
        secScr = self._addScreen(screen)

        self._secScreen = screen

    def finalize(self):
        sec = XorgSection("ServerLayout")

        def addInputDevices():
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

        if self.layout == "singleHead":
            sec.set("Identifier", "SingleHead")
            sec.set("Screen", self._priScreen.identifier)

            addInputDevices()

            sec.options = {
                "Xinerama" : "off",
                "Clone" : "off"
            }

        elif self.layout == "dualHead":
            pass

        self._parser.sections.append(sec)

def saveConfig(cfg, cards=[]):
    zconfig = ZorgConfig()

    zconfig.set("serverLayout", cfg.layout)

    for scr in cfg._priScreen, cfg._secScreen:
        if not scr:
            continue

        sec = scr.identifier
        zconfig.setSection(sec)

        zconfig.set("card", scr.device.cardId)
        zconfig.set("monitor", scr.monitor.identifier)
        zconfig.set("resolution", scr.res)
        zconfig.set("depth", scr.depth)

    if cards:
        cardNames = [x.cardId for x in cards]
        zconfig.set("cards", ",".join(cardNames), "General")

    for card in cards:
        sec = card.cardId
        zconfig.setSection(sec)

        zconfig.set("pciId", card.pciId)
        zconfig.set("busId", card.busId)
        zconfig.set("vendorName", card.vendorName)
        zconfig.set("boardName", card.boardName)
        zconfig.set("driver", card.driver)
        monitorNames = [x.identifier for x in card.monitors]
        zconfig.set("monitors", ",".join(monitorNames))

        for mon in card.monitors:
            sec = mon.identifier
            zconfig.setSection(sec)

            zconfig.set("probed", mon.probed)
            zconfig.set("digital", mon.digital)
            zconfig.set("hsync_min", mon.hsync_min)
            zconfig.set("hsync_max", mon.hsync_max)
            zconfig.set("vref_min", mon.vref_min)
            zconfig.set("vref_max", mon.vref_max)
            zconfig.set("resolutions", ",".join(mon.res))
            zconfig.set("eisaid", mon.eisaid)
            zconfig.set("vendorName", mon.vendorname)
            zconfig.set("modelName", mon.modelname)

    zconfig.write()

def autoConfigure():
    # detect graphic card and find monitor of first card
    devices = findVideoCards()
    if devices:
        device = devices[0]
        device.query()
    else:
        return

    # we need card data to check for lcd displays
    monitor = findMonitors(device, 0)[0]

    if not monitor.probed:
        device.monitors = []
        monitor = findMonitors(device, 1)[0]

    screen = Screen(device, monitor)
    screen.res = monitor.res[0]

    config = XConfig()
    config.new()
    config.setKeyboard(XkbLayout=queryKeymap())
    config.setTouchpad(queryTouchpad())
    config.setPrimaryScreen(screen)

    config.layout = "singleHead"
    config.finalize()
    config.save()

    saveConfig(config, devices)

def safeConfigure(driver = "vesa"):
    safedrv = driver.upper()

    dev = Device()
    dev.cardId = "0:0@%s:0:0:0" % safedrv
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
    dev.monitors = [mon]

    screen = Screen(dev, mon)
    screen.depth = 16
    screen.modes = ["800x600", "640x480"]

    config = XConfig()
    config.new()
    config.setKeyboard(XkbLayout=queryKeymap())
    config.setPrimaryScreen(screen)

    config.layout = "singleHead"
    config.finalize()
    config.save()

    saveConfig(config, [dev])

def listCards():
    zconfig = ZorgConfig()

    if not zconfig.hasOption("cards"):
        return ""

    cardNames = zconfig.get("cards").split(",")

    cards = []
    for cardName in cardNames:
        if not zconfig.hasSection(cardName):
            continue # zorg.conf is broken

        zconfig.setSection(cardName)
        #busId = zconfig.get("busid")
        vendorName = zconfig.get("vendorName")
        boardName = zconfig.get("boardName")
        cards.append("%s %s - %s" % (cardName, boardName, vendorName))

    return "\n".join(cards)

def setCardOptions(cardId, options):
    pass

def cardInfo(cardId):
    zconfig = ZorgConfig()

    if not zconfig.hasSection(cardId):
        return ""
    zconfig.setSection(cardId)

    info = []
    #info.append("identifier=%s" % zconfig.get("identifier"))

    name = "%s - %s" % (zconfig.get("boardName"), zconfig.get("vendorName"))
    info.append("name=%s" % name)
    info.append("driver=%s" % zconfig.get("driver"))

    return "\n".join(info)

def listMonitors(cardId):
    zconfig = ZorgConfig()

    if not zconfig.hasSection(cardId):
        return ""

    identifiers = zconfig.get("monitors", section=cardId).split(",")
    monitors = []

    for monId in identifiers:
        zconfig.setSection(monId)
        vendorName = zconfig.get("vendorName")
        modelName = zconfig.get("modelName")
        monitors.append("%s %s - %s" % (monId, modelName, vendorName))

    return "\n".join(monitors)

def monitorInfo(identifier):
    zconfig = ZorgConfig()

    if not zconfig.hasSection(identifier):
        return ""

    zconfig.setSection(identifier)
    info = []
    name = "%s - %s" % (zconfig.get("modelName"), zconfig.get("vendorName"))
    info.append("name=%s" % name)
    info.append("resolutions=%s" % zconfig.get("resolutions"))

    return "\n".join(info)

def addMonitor(data):
    zconfig = ZorgConfig()

    numbers = set(atoi(lremove(x, "Monitor")) for x in zconfig.cp.sections() if x.startswith("Monitor"))
    numbers = list(set(xrange(len(numbers) + 1)) - numbers)
    numbers.sort()
    number = numbers[0]

    info = dict(x.split("=", 1) for x in data.strip().splitlines())

    zconfig.setSection("Monitor%d" % number)
    keys = ("modelname", "vendorname", "probed", "eisaid", "digital", \
            "hsync_min", "hsync_max", "vref_min", "vref_max", "resolutions")

    for key, value in info.items():
        if key.lower() not in keys:
            continue

        zconfig.set(key, value)

    zconfig.write()

def removeMonitor(monitorId):
    zconfig = ZorgConfig()

    if not zconfig.hasSection(monitorId):
        return

    zconfig.cp.remove_section(monitorId)
    zconfig.write()

def probeMonitors():
    zconfig = ZorgConfig()

    cards = zconfig.get("cards").split(",")

    for card in cards:
        if not zconfig.hasSection(card):
            continue

        # Not implemented yet

def installINF(filePath):
    pass

def getScreens():
    zconfig = ZorgConfig()

    scrInfo = []

    for scr in "Screen0", "Screen1":
        if not zconfig.hasSection(scr):
            continue
        zconfig.setSection(scr)

        l = []
        for option in "card", "monitor", "resolution", "depth":
            l.append("%s=%s" % (option, zconfig.get(option)))

        scrInfo.append("\n".join(l))

    return "\n\n".join(scrInfo)

def setScreens(screens):
    zconfig = ZorgConfig()

    config = XConfig()
    config.load()
    config.removeScreens()

    index = 0
    for screen in screens.strip().split("\n\n"):
        info = dict(x.split("=", 1) for x in screen.strip().splitlines())

        cardId = info["card"]

        if not zconfig.hasSection(cardId):
            return
        zconfig.setSection(cardId)

        pciId, busId = cardId.split("@")
        vendorId, deviceId = pciId.split(":")

        dev = Device(vendorId, deviceId)
        dev.driver = zconfig.get("driver")
        dev.vendorName = zconfig.get("vendorName")
        dev.boardName = zconfig.get("boardName")

        monitorId = info["monitor"]
        if not zconfig.hasSection(monitorId):
            return
        zconfig.setSection(monitorId)

        mon = Monitor()
        mon.probed = zconfig.getBool("probed")
        mon.digital = zconfig.getBool("digital")
        mon.eisa_id= zconfig.get("eisaid")
        mon.vendorname = zconfig.get("vendorName")
        mon.modelname = zconfig.get("modelName")

        mon.hsync_min = zconfig.getFloat("hsync_min")
        mon.hsync_max = zconfig.getFloat("hsync_max")
        mon.vref_min = zconfig.getFloat("vref_min")
        mon.vref_max = zconfig.getFloat("vref_max")
        mon.res = zconfig.get("resolutions").split(",")

        scr = Screen(dev, mon)
        scr.resolution = info["resolution"]
        scr.depth = info["depth"]

        if index == 0:
            config.setPrimaryScreen(scr)
            index = 1
        else:
            config.setSecondaryScreen(scr)

    config.save()
    saveConfig(config)

if __name__ == "__main__":
    #safeConfigure()
    #autoConfigure()
    print listCards()
    print cardInfo("PCI:0:5:0")
    print listMonitors("PCI:0:5:0")
    print monitorInfo("Monitor0")
    print getScreens()
    setScreens("""
card=10de:0240@PCI:0:5:0
monitor=Monitor0
resolution=800x600
depth=24

card=10de:0240@PCI:0:5:0
monitor=Monitor0
resolution=1024x768
depth=16

""")

    addMonitor("""
hsync_min=30
hsync_max=60
vref_min=50
vref_max=75
vendorname=VENDOR
modelname=MODEL
""")

    removeMonitor("Monitor2")
