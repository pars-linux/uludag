# -*- coding: utf-8 -*-

import os
import dbus
import glob

import comar
from zorg import consts
from zorg.parser import *
from zorg.utils import *

sysdir = "/sys/bus/pci/devices/"

class Output:
    def __init__(self, name):
        self.name = name
        self.enabled = True
        self.ignored = False

        self.__reset()

    def __reset(self):
        self.mode = ""
        self.refresh_rate = ""
        self.rotation = ""
        self.right_of = ""
        self.below = ""

    def setEnabled(self, enabled):
        self.enabled = enabled

        if enabled:
            self.ignored = False
        else:
            self.__reset()

    def setIgnored(self, ignored):
        self.ignored = ignored

        if ignored:
            self.enabled = False
            self.__reset()

    def setMode(self, mode, rate=""):
        self.mode = mode
        self.refresh_rate = rate

    def setOrientation(self, rotation, reflection=""):
        self.rotation = rotation

    def setPosition(self, pos, arg):
        if pos == "RightOf":
            self.right_of = arg
            self.below = ""
        elif pos == "Below":
            self.right_of = ""
            self.below = arg
        else:
            self.right_of = ""
            self.below = ""

class VideoDevice:
    def __init__(self, deviceDir=None, busId=None):
        if deviceDir:
            self.bus = tuple(int(x, 16) for x in deviceDir.replace(".",":").split(":"))[1:4]
        else:
            self.bus = tuple(int(x) for x in busId.split(":")[1:4])
            deviceDir = "0000:%02x:%02x.%x" % self.bus

        self.vendor_id  = lremove(pciInfo(deviceDir, "vendor"), "0x").lower()
        self.product_id = lremove(pciInfo(deviceDir, "device"), "0x").lower()
        self.saved_vendor_id  = None
        self.saved_product_id = None

        self.driver = None
        self.package = None
        self.xorg_module = None

        self.active_outputs = []
        self.modes = {}
        self.depth = 0
        self.desktop_setup = "single"

        self.driver_options = {}
        self.monitors = {}

        self.outputs = {}

    def getDict(self):
        info = {
            "bus-id" : "PCI:%d:%d:%d" % self.bus,
            "driver" : self.driver or "",
            "depth" : str(self.depth) if self.depth else "",
            "desktop-setup" : self.desktop_setup,
            "active-outputs" : ",".join(self.active_outputs),
        }

        for output, mode in self.modes.items():
            info["%s-mode" % output] = mode
            if self.monitors.has_key(output):
                info["%s-hsync" % output] = self.monitors[output].hsync
                info["%s-vref"  % output] = self.monitors[output].vref

        return info

    def driverInfo(self, driver=None):
        if driver is None:
            driver = self.driver

        if driver is None:
            return None

        link = comar.Link()
        packages = list(link.Xorg.Driver)
        for package in packages:
            try:
                info = link.Xorg.Driver[package].getInfo()
            except dbus.DBusException:
                continue
            alias = str(info["alias"])
            if alias == self.driver:
                if "package" not in info:
                    info["package"] = package
                return info
        else:
            info = {
                    "alias":        driver,
                    "xorg-module":  driver,
                    "package":      ""
                    }
            return info

    def setDriver(self, driver):
        """
            Change driver.

            Driver name can be an alias like "nvidia173". If needed,
            the driver is enabled.
        """

        self.driver = driver

        if driver:
            info = self.driverInfo(driver)
            self.xorg_module = info["xorg-module"]
            self.package = info["package"]
        else:
            self.xorg_module = None
            self.package = None

        self.enableDriver()

    def enableDriver(self):
        oldpackage = enabledPackage()
        if self.package != oldpackage:
            link = comar.Link()
            if oldpackage and oldpackage.replace("-", "_") in list(link.Xorg.Driver):
                link.Xorg.Driver[oldpackage].disable(timeout=2**16-1)

            if self.package:
                link.Xorg.Driver[self.package].enable(timeout=2**16-1)

    def requestDriverOptions(self):
        if not self.package or self.package == "xorg-video":
            return
        link = comar.Link()
        self.driver_options = link.Xorg.Driver[self.package].getOptions(self.getDict())

    def isChanged(self):
        if self.saved_vendor_id and self.saved_product_id:
            return (self.vendor_id, self.product_id) != (self.saved_vendor_id, self.saved_product_id)
        return False

class Monitor:
    def __init__(self):
        self.vendor = ""
        self.model = "Default Monitor"
        self.hsync = "31.5-50"
        self.vref = "50-70"

def pciInfo(dev, attr):
    return sysValue(sysdir, dev, attr)

def getKeymapList():
    return os.listdir(consts.xkb_symbols_dir)

def driverExists(name):
    return os.path.exists(os.path.join(consts.drivers_dir, "%s_drv.so" % name))

def listAvailableDrivers(d = consts.drivers_dir):
    a = []
    if os.path.exists(d):
        for drv in os.listdir(d):
            if drv.endswith("_drv.so"):
                if drv[:-7] not in a:
                    a.append(drv[:-7])
    return a

def enabledPackage():
    try:
        return file("/var/lib/zorg/enabled_package").read()
    except IOError:
        return None

def getPrimaryCard():
    for boot_vga in glob.glob("%s/*/boot_vga" % sysdir):
        if open(boot_vga).read().startswith("1"):
            dev_path = os.path.dirname(boot_vga)
            return os.path.basename(dev_path)

    return None

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
    unlink("/tmp/xorg.conf")
    if ret != 0:
        return

    return file("/var/log/xlog").readlines()
