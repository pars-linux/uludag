# -*- coding: utf-8 -*-

from ConfigParser import RawConfigParser, ParsingError

from zorg.parser import *
from zorg.probe import touchpadDevices

xorgConf = "/etc/X11/xorg.conf"
zorgConfigDir = "/var/lib/zorg"
zorgConfig = "config"

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
            "XkbLayout" : "trq"
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
        self._parser.parseFile(xorgConf)

    def removeScreens(self):
        sections = self._parser.getSections("Device", "Monitor", "Screen")
        for sec in sections:
            self._parser.sections.remove(sec)

    def save(self):
        f = open(xorgConf, "w")
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

class ZorgConfig:
    def __init__(self):
        import os

        if not os.path.exists(zorgConfigDir):
            os.mkdir(zorgConfigDir, 0755)

        self.configFile = os.path.join(zorgConfigDir, zorgConfig)

        self.cp = RawConfigParser()
        try:
            self.cp.read(self.configFile)
        except ParsingError:
            pass

        self.setSection("General")

    def setSection(self, name):
        if not self.cp.has_section(name):
            self.cp.add_section(name)

        self.currentSection = name

    def hasSection(self, name):
        return self.cp.has_section(name)

    def hasOption(self, option, section=None):
        if section is None:
            section = self.currentSection
        return self.cp.has_option(section, option)

    def get(self, option, default = "", section=None):
        if section is None:
            section = self.currentSection
        if not self.cp.has_option(section, option):
            return default

        return self.cp.get(self.currentSection, option)

    def getBool(self, option, default = False, section=None):
        if section is None:
            section = self.currentSection
        if not self.cp.has_option(section, option):
            return default

        return self.cp.getboolean(self.currentSection, option)

    def getFloat(self, option, default = 0.0, section=None):
        if section is None:
            section = self.currentSection
        if not self.cp.has_option(section, option):
            return default

        return self.cp.getfloat(self.currentSection, option)

    def set(self, option, value, section=None):
        if section is None:
            section = self.currentSection
        self.cp.set(section, option, value)

    def write(self):
        f = file(self.configFile, "w")
        self.cp.write(f)
        f.close()

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

        zconfig.set("busId", card.busId)
        zconfig.set("vendorId", card.vendorId)
        zconfig.set("deviceId", card.deviceId)
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

