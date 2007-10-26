# -*- coding: utf-8 -*-

import os
import re
import struct

from zorg.hwdata import *
from zorg.parser import *
from zorg.utils import *
from zorg import modeline

xdriverlist = "/usr/lib/X11/xdriverlist"
MonitorsDB = "/usr/lib/X11/MonitorsDB"

driver_path = "/usr/lib/xorg/modules/drivers"
xkb_path = "/usr/share/X11/xkb/symbols/pc"

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

def pciInfo(dev, attr):
    return sysValue(sysdir, dev, attr)

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

def queryDevice(dev):
    dev.vendorName, dev.boardName = queryPCI(dev.vendorId, dev.deviceId)

    if not dev.driver:
        availableDrivers = listAvailableDrivers()

        for line in loadFile(xdriverlist):
            if line.startswith(dev.vendorId + dev.deviceId):
                drv = line.rstrip("\n").split(" ")[1]
                if drv in availableDrivers:
                    dev.driver = drv

    # if could not find driver from driverlist try X -configure
    if not dev.driver:
        print "Running X server to query driver..."
        ret = run("/usr/bin/X", ":99", "-configure", "-logfile", "/var/log/xlog")
        if ret == 0:
            home = os.getenv("HOME", "")
            p = XorgParser()
            p.parseFile(home + "/xorg.conf.new")
            unlink(home + "/xorg.conf.new")
            sec = p.getSections("Device")
            if sec:
                dev.driver = sec[0].get("Driver")
                print "Driver reported by X server is %s." % dev.driver

    # use nvidia if nv is found
    if (dev.driver == "nv") and ("nvidia" in availableDrivers):
        dev.driver = "nvidia"

    # In case we can't parse or find xorg.conf.new
    if not dev.driver:
        dev.driver = "vesa"

    # If driver supports RandR 1.2, we will use a different probe method.
    if dev.driver in randr12_drivers:
        dev.randr12 = True

def findVideoCards():
    """ Finds video cards. Result is a list of Device objects. """
    cards = []

    pbus = getPrimaryBus()
    if pbus:
        vendorId = lremove(pciInfo(pbus, "vendor"), "0x")
        deviceId = lremove(pciInfo(pbus, "device"), "0x")
        busId = tuple(int(x, 16) for x in pbus.replace(".",":").split(":"))[1:4]

        card = Device("PCI:%d:%d:%d" % busId, vendorId, deviceId)
        cards.append(card)

    if len(cards):
        return cards
    else:
        # This machine might be a terminal server with no video cards.
        # We start X and leave the decision to the user.
        return None

def getPrimaryBus():
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

def queryOutputs(device):
    if device.randr12:
        queryRandrOutputs(device)
    elif device.driver == "nvidia":
        queryNvidiaOutputs(device)
    elif device.driver == "fglrx":
        queryFglrxOutputs(device)
    else:
        device.monitors = findMonitors(device, 0, 1)

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

        if "Primary Controller - " in line:
            for out in outs:
                if out[0] in line:
                    primary = out[1]

        if "Secondary Controller - " in line:
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
    p = XorgParser()
    sec = XorgSection("Device")
    sec.set("Identifier", "Card0")
    sec.set("Driver", card.driver)
    sec.set("BusId", card.busId)

    # Old nvidia driver does not enable this option
    # by default. We need it to get possible modes
    # supported by monitors.
    if card.driver == "nvidia":
        sec.options["UseEdidFreqs"] = xBool[True]

    p.sections.append(sec)

    sec = XorgSection("Screen")
    sec.set("Identifier", "Screen0")
    sec.set("Device", "Card0")

    if card.driver == "fglrx":
        sec.set("DefaultDepth", unquoted("24"))

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
