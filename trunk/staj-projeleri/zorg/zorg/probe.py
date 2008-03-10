# -*- coding: utf-8 -*-

import os
import re
import dbus
import struct

from zorg.hwdata import *
from zorg.parser import *
from zorg.utils import *
from zorg import modeline

DriversDB = "/usr/lib/X11/DriversDB"
MonitorsDB = "/usr/lib/X11/MonitorsDB"

driver_path = "/usr/lib/xorg/modules/drivers"
xkb_path = "/usr/share/X11/xkb/symbols"

sysdir = "/sys/bus/pci/devices/"

# from pci/header.h
PCI_COMMAND             = 0x04
PCI_COMMAND_IO          = 0x1
PCI_COMMAND_MEMORY      = 0x2

PCI_BRIDGE_CONTROL      = 0x3e
PCI_BRIDGE_CTL_VGA      = 0x08

PCI_BASE_CLASS_DISPLAY  = 0x03

#PCI_BASE_CLASS_BRIDGE   = 0x06
PCI_CLASS_BRIDGE_PCI    = 0x0604

class PCIDevice:
    def __init__(self, name):
        self.name = name
        self.class_ = None
        self.bridge = None
        self.config = None

    def _readConfig(self, offset, size=1):
        if self.config is None:
            self.config = open(os.path.join(sysdir, self.name, "config")).read()

        return self.config[offset:offset+size]

    def readConfigWord(self, offset):
        data = self._readConfig(offset, 2)

        return struct.unpack("h", data)[0]

class VideoDevice:
    def __init__(self, deviceDir=None, busId=None):
        if deviceDir:
            self.bus = tuple(int(x, 16) for x in deviceDir.replace(".",":").split(":"))[1:4]
        else:
            self.bus = tuple(int(x) for x in busId.split(":")[1:4])
            deviceDir = "0000:%02x:%02x.%x" % self.bus

        self.vendor_id = lremove(pciInfo(deviceDir, "vendor"), "0x").lower()
        self.product_id = lremove(pciInfo(deviceDir, "device"), "0x").lower()

        self.driverlist = ["vesa"]
        #self.depthlist = ["16", "24"]
        self.driver = "vesa"
        self.package = "xorg-video"

        self.probe_result = {"flags" : "", "depths" : "16,24"}

        self.active_outputs = ["default"]
        self.modes = {"default" : "800x600"}
        self.depth = "16"
        self.desktop_setup = "single"

        self.driver_options = {}
        self.monitor_settings = {}

    def getDict(self):
        info = {
            "bus-id" : "PCI:%d:%d:%d" % self.bus,
            "driver" : self.driver,
            "depth" : self.depth,
            "desktop-setup" : self.desktop_setup,
            "active-outputs" : ",".join(self.active_outputs),
        }

        for output, mode in self.modes.items():
            info["%s-mode" % output] = mode

        return info

    def query(self):
        bus = dbus.SystemBus()

        try:
            object = bus.get_object("tr.org.pardus.comar", "/", introspect=False)
            iface = dbus.Interface(object, "tr.org.pardus.comar")

        except dbus.exceptions.DBusException, e:
            print "Error: %s" % e
            return []

        driverPackages = iface.listModelApplications("Xorg.Driver")
        availableDrivers = listAvailableDrivers()
        driver = None

        for line in loadFile(DriversDB):
            if line.startswith(self.vendor_id + self.product_id):
                self.driverlist = line.rstrip("\n").split(" ")[1:]

                for drv in self.driverlist:
                    if "@" in drv:
                        drvname, drvpackage = drv.split("@", 1)
                        if drvpackage.replace("-", "_") in driverPackages:
                            driver = drvname
                            self.package = drvpackage
                            break

                    elif drv in availableDrivers:
                        driver = drv
                        break

                break

        # if could not find driver from driverlist try X -configure
        if not driver:
            print "Running X server to query driver..."
            ret = run("/usr/bin/X", ":99", "-configure", "-logfile", "/var/log/xlog")
            if ret == 0:
                home = os.getenv("HOME", "")
                p = XorgParser()
                p.parseFile(home + "/xorg.conf.new")
                unlink(home + "/xorg.conf.new")
                sec = p.getSections("Device")
                if sec:
                    driver = sec[0].get("Driver")
                    if driver not in self.driverlist:
                        self.driverlist.append(driver)

                    print "Driver reported by X server is %s." % driver

        if driver:
            self.driver = driver

        app = self.package.replace("-", "_")
        object = bus.get_object("tr.org.pardus.comar", "/package/%s" % app, introspect=False)
        iface = dbus.Interface(object, "tr.org.pardus.comar.Xorg.Driver")

        iface.enable()
        self.probe_result = iface.probe(self.getDict())

        depthlist = self.probe_result["depths"].split(",")
        self.depth = depthlist[0]

        #flags = self.probe_result["flags"].split(",")

    def requestDriverOptions(self):
        bus = dbus.SystemBus()
        app = self.package.replace("-", "_")
        object = bus.get_object("tr.org.pardus.comar", "/package/%s" % app, introspect=False)
        iface = dbus.Interface(object, "tr.org.pardus.comar.Xorg.Driver")

        self.driver_options = iface.getOptions(self.getDict())

def pciInfo(dev, attr):
    return sysValue(sysdir, dev, attr)

def getKeymapList():
    return os.listdir(xkb_path)

def listAvailableDrivers(d = driver_path):
    a = []
    if os.path.exists(d):
        for drv in os.listdir(d):
            if drv.endswith("_drv.so"):
                if drv[:-7] not in a:
                    a.append(drv[:-7])
    return a

def listDriverPackages():
    import dbus

    try:
        bus = dbus.SystemBus()
        object = bus.get_object("tr.org.pardus.comar", "/", introspect=False)
        iface = dbus.Interface(object, "tr.org.pardus.comar")

    except dbus.exceptions.DBusException, e:
        print "Error: %s" % e
        return []

    return iface.listModelApplications("Xorg.Driver")

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

def getPrimaryCard():
    devices = []
    bridges = []

    for dev in os.listdir(sysdir):
        device = PCIDevice(dev)
        device.class_ = int(pciInfo(dev, "class")[:6], 16)
        devices.append(device)

        if device.class_ == PCI_CLASS_BRIDGE_PCI:
            bridges.append(device)

    for dev in devices:
        for bridge in bridges:
            dev_path = os.path.join(sysdir, bridge.name, dev.name)
            if os.path.exists(dev_path):
                dev.bridge = bridge

    primaryBus = None
    for dev in devices:
        if (dev.class_ >> 8) != PCI_BASE_CLASS_DISPLAY:
            continue

        vga_routed = True
        bridge = dev.bridge
        while bridge:
            bridge_ctl = bridge.readConfigWord(PCI_BRIDGE_CONTROL)

            if not (bridge_ctl & PCI_BRIDGE_CTL_VGA):
                vga_routed = False
                break

            bridge = bridge.bridge

        if vga_routed:
            pci_cmd = dev.readConfigWord(PCI_COMMAND)

            if pci_cmd & (PCI_COMMAND_IO | PCI_COMMAND_MEMORY):
                primaryBus = dev.name
                break

    # Just to ensure that we have picked a device. Normally,
    # primaryBus might not be None here.
    if primaryBus is None:
        for dev in devices:
            if (dev.class_ >> 8) == PCI_BASE_CLASS_DISPLAY:
                primaryBus = dev.name
                break

    return primaryBus

def queryRandrOutputs(device):
    lines = xserverProbe(device)
    if not lines:
        return

    findOutput = re.compile("^.*: Output (\S+) (.*)$")
    outStates = ("connected", "disconnected", "enabled by config file")

    parsingModesFor = ""

    for line in lines:
        if "Output" in line:
            matched = findOutput.match(line)
            if matched:
                name, state = matched.groups()
                if device.outputs.has_key(name) or not state in outStates:
                    continue
                else:
                    device.outputs[name] = []

        elif "Printing probed modes for output" in line:
            name = line.rsplit(None, 1)[-1]
            if device.outputs.has_key(name) and not device.outputs[name]:
                parsingModesFor = name

        elif parsingModesFor:
            fields = line.split()
            if "Modeline" in fields:
                modeWithRate = fields[fields.index("Modeline") + 1]
                mode, rate = modeWithRate.rsplit("x", 1)
                mode = mode.strip('"')

                if not mode in device.outputs[parsingModesFor]:
                    device.outputs[parsingModesFor].append(mode)
            else:
                parsingModesFor = ""

        elif "TV standards supported by chip:" in line:
            device.tvStandards = line.strip().rsplit(": ", 1)[1].split()

def queryNvidiaOutputs(device):
    lines = xserverProbe(device)
    if not lines:
        return

    device.tvStandards = [
            "PAL-B",  "PAL-D",  "PAL-G",   "PAL-H",
            "PAL-I",  "PAL-K1", "PAL-M",   "PAL-N",
            "PAL-NC", "NTSC-J", "NTSC-M",  "HD480i",
            "HD480p", "HD720p", "HD1080i", "HD1080p",
            "HD576i", "HD576p"
        ]

    # This is for nvidia-old drivers
    modeFormat = re.compile('.+ "(.+)": .+ MHz, .+ kHz, .+ Hz.*')
    oldFormat = False

    parsingModesFor = ""

    for line in lines:
        if "Supported display device(s): " in line:
            outs = line.rsplit(":", 1)[-1].split(",")
            for out in outs:
                out = out.strip()
                device.outputs[out] = []

        elif "--- Modes in ModePool for " in line:
            for key in device.outputs.keys():
                if key in line:
                    parsingModesFor = key
                    break

        elif "Validated modes for display device " in line:
            oldFormat = True
            for key in device.outputs.keys():
                if key in line:
                    parsingModesFor = key
                    break

        elif parsingModesFor:
            if not oldFormat:
                if "--- End of ModePool for " in line:
                    parsingModesFor = ""
                    continue

                mode = line.split(":")[2].split("@", 1)[0].replace(" ", "")

                if not mode in device.outputs[parsingModesFor]:
                    device.outputs[parsingModesFor].append(mode)

            else:
                matched = modeFormat.match(line)
                if matched:
                    mode = matched.groups()[0]

                    if not mode in device.outputs[parsingModesFor]:
                        device.outputs[parsingModesFor].append(mode)

                else:
                    parsingModesFor = ""

def queryFglrxOutputs(device):
    lines = xserverProbe(device)
    if not lines:
        return

    device.tvStandards = [
            "NTSC-M",       "NTSC-JPN", "NTSC-N",      "PAL-B",
            "PAL-COMB-N",   "PAL-D",    "PAL-G",       "PAL-H",
            "PAL-I",        "PAL-K",    "PAL-K1",      "PAL-L",
            "PAL-M",        "PAL-N",    "PAL-SECAM-D", "PAL-SECAM-K",
            "PAL-SECAM-K1", "PAL-SECAM-L"
        ]

    outInfo = re.compile(r".*: Connected Display\d+: (.+) \[(.+)\].*")
    modeCount = re.compile(r".*: Total of \d+ modes found for .* display.*")
    modeLine = re.compile(r".*: Modeline \"(.*)\" *.*")

    primary = ""
    secondary = ""
    outs = []
    parsingModesFor = ""

    for line in lines:
        if "Connected Display" in line:
            matched = outInfo.match(line)
            if matched:
                info = matched.groups()
                outs.append(info)
                device.outputs[info[1]] = []

        elif "Primary Controller - " in line:
            for out in outs:
                if out[0] in line:
                    primary = out[1]

        elif "Secondary Controller - " in line:
            for out in outs:
                if out[0] in line:
                    secondary = out[1]

        elif "modes found for primary display" in line:
            matched = modeCount.match(line)
            if matched:
                parsingModesFor = primary

        elif "modes found for secondary display" in line:
            matched = modeCount.match(line)
            if matched:
                parsingModesFor = secondary

        elif parsingModesFor:
            if "Display dimensions" in line \
                    or "DPI" in line:
                parsingModesFor = ""
                continue

            matched = modeLine.match(line)
            if matched:
                mode = matched.groups()[0]
                if not mode in device.outputs[parsingModesFor]:
                    device.outputs[parsingModesFor].append(mode)

def xserverProbe(card):
    dev = {
            "driver":   card.driver,
            "bus-id":    card.busId
        }

    # Old nvidia driver does not enable this option
    # by default. We need it to get possible modes
    # supported by monitors.
    if card.driver == "nvidia":
        dev["driver-options"] = {
                "UseEdidFreqs" : "1"
            }

    if card.driver == "fglrx":
        dev["depth"] = "24"

    return XProbe(dev)

def XProbe(dev):
    p = XorgParser()
    sec = XorgSection("Device")
    sec.set("Identifier", "Card0")
    sec.set("Driver", dev["driver"])
    sec.set("BusId", dev["bus-id"])

    if dev.has_key("driver-options"):
        sec.options.update(dev["driver-options"])

    p.sections.append(sec)

    sec = XorgSection("Screen")
    sec.set("Identifier", "Screen0")
    sec.set("Device", "Card0")

    if dev.has_key("depth"):
        sec.set("DefaultDepth", unquoted(dev["depth"]))

    p.sections.append(sec)

    open("/tmp/xorg.conf", "w").write(p.toString())

    ret = run("/usr/bin/X", ":99", "-probeonly", "-allowMouseOpenFail", \
            "-config", "/tmp/xorg.conf", \
            "-logfile", "/var/log/xlog", \
            "-logverbose", "6")
    if ret != 0:
        return

    return file("/var/log/xlog").readlines()

def queryDDC(adapter=0):
    mon = Monitor()

    from zorg import ddc
    edid = ddc.query(adapter)

    if not edid or not edid["eisa_id"]:
        #mon.probed = False
        #return mon
        return DefaultMonitor()
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

    open("/tmp/xorg.conf", "w").write(p.toString())

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
    a = run("/usr/bin/X", ":99", "-probeonly", "-allowMouseOpenFail", \
            "-config", "/tmp/xorg.conf", \
            "-logfile", "/var/log/xlog")
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
    digitalMonitor = None

    for adapter in adapters:
        mon = queryDDC(adapter)

        # defaults for the case where ddc fails
        if mon.hsync_min == 0 or mon.vref_min == 0:
            mon.hsync_min = 31.5
            mon.hsync_max = 50
            mon.vref_min = 50
            mon.vref_max = 70

        if mon.eisaid:
            mon.id = "EISA_%s" % mon.eisaid
            for line in loadFile(MonitorsDB):
                l = line.split(";")
                if mon.eisaid == l[2].strip().upper():
                    mon.vendorname = l[0].lstrip()
                    mon.modelname = l[1].lstrip()
                    mon.hsync_min, mon.hsync_max = map(float, l[3].strip().split("-"))
                    mon.vref_min, mon.vref_max = map(float, l[4].strip().split("-"))

        # check lcd panel
        #if mon.digital and (card.driver in lcd_drivers):
        if card.driver in lcd_drivers:
            digitalMonitor = mon

        card.monitors.append(mon)
        monitors.append(mon)

    if digitalMonitor:
        queryPanel(digitalMonitor, card)

    return monitors
