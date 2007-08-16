# -*- coding: utf-8 -*-

import piksemel
from csapi import atoi

from zorg.parser import *
from zorg.hwdata import *

xorgConf = "/etc/X11/xorg.conf"

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

        modules = ("dbe", "type1", "freetype", "record", "xtrap",
                   "glx", "dri", "v4l", "extmod")

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
        sec.set("BusId", dev.busId)

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

def addTag(p, name, data):
    t = p.insertTag(name)
    t.insertData(data)

class ZorgConfig:
    zorgConfigDir = "/var/lib/zorg"
    zorgConfig = "config.xml"

    def __init__(self):
        import os

        if not os.path.exists(self.zorgConfigDir):
            os.mkdir(self.zorgConfigDir, 0755)

        self.configFile = os.path.join(self.zorgConfigDir, self.zorgConfig)

        try:
            self.doc = piksemel.parse(self.configFile)
        except OSError:
            self.doc = piksemel.newDocument("ZORG")

    def __getCard(self, tag):
        busId = tag.getTagData("BusId")
        vendorId = tag.getTagData("VendorId")
        deviceId = tag.getTagData("DeviceId")
        
        card = Device(busId, vendorId, deviceId)
        
        card.driver = tag.getTagData("Driver")
        card.vendorName = tag.getTagData("Vendor")
        card.boardName = tag.getTagData("Board")
        
        monitorsTag = tag.getTag("Monitors")
        for mon in monitorsTag.tags("Monitor"):
            monitorId = mon.firstChild().data()
            monitor = self.getMonitor(monitorId)
            if monitor:
                card.monitors.append(monitor)
        
        return card
    
    def __getMonitor(self, tag):
        mon = Monitor()
        
        mon.id = tag.getAttribute("id")
        mon.eisaid = tag.getTagData("EISAID")
        
        hsync = tag.getTagData("HorizSync").split("-")
        vref = tag.getTagData("VertRefresh").split("-")
        mon.hsync_min, mon.hsync_max = map(atoi, hsync)
        mon.vref_min, mon.vref_max = map(atoi, vref)
        
        digital = tag.getTagData("Digital")
        mon.digital = digital.lower() == "true"
        
        mon.vendorname = tag.getTagData("Vendor")
        mon.modelname = tag.getTagData("Model")
        
        mon.res = []
        resTag = tag.getTag("Resolutions")
        for res in resTag.tags("Resolution"):
            mon.res.append(res.firstChild().data())
            #TODO: Check if res is preferred
        
        return mon

    def cards(self):
        cardList = []
        for tag in self.doc.tags("Card"):
            cardList.append(self.__getCard(tag))
        
        return cardList
            
    def getCard(self, ID):
        for tag in self.doc.tags("Card"):
            if tag.getAttribute("id") == ID:
                return self.__getCard(tag)
    
    def addCard(self, card):
        for tag in self.doc.tags("Card"):
            if tag.getAttribute("id") == card.id:
                tag.hide()
                break
        
        tag = self.doc.insertTag("Card")
        tag.setAttribute("id", card.id)
        
        tags = {
            "BusId" : card.busId,
            "VendorId" : card.vendorId,
            "DeviceId" : card.deviceId,
            "Driver" : card.driver,
            "Vendor" : card.vendorName,
            "Board" : card.boardName
        }
        
        for k, v in tags.items():
            addTag(tag, k, v)
        
        mons = tag.insertTag("Monitors")
        for mon in card.monitors:
            addTag(mons, "Monitor", mon.id)
    
    def monitors(self):
        monitorList = []
        for tag in self.doc.tags("Monitor"):
            monitorList.append(self.__getMonitor(tag))
        
        return monitorList

    def getMonitor(self, ID):
        for tag in self.doc.tags("Monitor"):
            if tag.getAttribute("id") == ID:
                return self.__getMonitor(tag)
    
    def addMonitor(self, monitor):
        self.removeMonitor(monitor.id)

        tag = self.doc.insertTag("Monitor")
        tag.setAttribute("id", monitor.id)
        
        hsync = "%s-%s" % (monitor.hsync_min, monitor.hsync_max)
        vref = "%s-%s" % (monitor.vref_min, monitor.vref_max)
        
        tags = {
            "EISAID" : monitor.eisaid,
            "HorizSync" : hsync,
            "VertRefresh" : vref,
            "Digital" : str(monitor.digital),
            "Vendor" : monitor.vendorname,
            "Model" : monitor.modelname
        }
        
        for k, v in tags.items():
            addTag(tag, k, v)
        
        resTag = tag.insertTag("Resolutions")
        for res in monitor.res:
            addTag(resTag, "Resolution", res)
            #TODO: Check if it is preferred
    
    def removeMonitor(self, ID):
        for tag in self.doc.tags("Monitor"):
            if tag.getAttribute("id") == ID:
                tag.hide()
                break
    
    def getScreen(self, number):
        nr = str(number)
        for tag in self.doc.tags("Screen"):
            if tag.getAttribute("number") == nr:
                card = self.getCard(tag.getTagData("Card"))
                monitor = self.getMonitor(tag.getTagData("Monitor"))
                
                scr = Screen(card, monitor)
                
                scr.number = nr
                scr.res = tag.getTagData("Resolution")
                scr.depth = atoi(tag.getTagData("Depth"))
                # is scr.modes needed?
                # scr.enabled ?
                
                return scr
    
    def setScreen(self, screen):
        nr = str(screen.number)
        for tag in self.doc.tags("Screen"):
            if tag.getAttribute("number") == nr:
                tag.hide()
                break
        
        tag = self.doc.insertTag("Screen")
        tag.setAttribute("number", nr)
        #TODO: set also enabled attribute
        
        tags = {
            "Card" : screen.device.id,
            "Monitor" : screen.monitor.id,
            "Resolution" : screen.res,
            "Depth" : str(screen.depth)
        }
        
        for k, v in tags.items():
            addTag(tag, k, v)
    
    def enableScreen(self, number, enable=True):
        nr = str(screen.number)
        for tag in self.doc.tags("Screen"):
            if tag.getAttribute("number") == nr:
                tag.setAttribute("enabled", str(enable))
                break
        
    def save(self):
        f = file(self.configFile, "w")
        f.write(self.doc.toPrettyString())
        f.close()
