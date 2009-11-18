# -*- coding: utf-8 -*-

import os
import dbus
import glob

import comar
from zorg import consts
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
        if rotation not in ("inverted", "left", "right"):
            rotation = ""
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

        self.bus_id = "PCI:%d:%d:%d" % self.bus

        self.vendor_id  = lremove(pciInfo(deviceDir, "vendor"), "0x").lower()
        self.product_id = lremove(pciInfo(deviceDir, "device"), "0x").lower()
        self.saved_vendor_id  = None
        self.saved_product_id = None

        self.driver = None
        self.depth = 0
        self.outputs = {}
        self.monitors = {}

    def driverInfo(self, driver=None):
        if driver is None:
            driver = self.driver

        if driver is None:
            return {}

        link = comar.Link()
        packages = list(link.Xorg.Driver)
        for package in packages:
            try:
                info = link.Xorg.Driver[package].getInfo()
            except dbus.DBusException:
                continue
            alias = str(info["alias"])
            if alias == driver:
                info["package"] = package
                return info
        else:
            if driverExists(driver):
                info = {
                        "alias":        driver,
                        "xorg-module":  driver,
                        }
                return info
            else:
                return {}

    def setDriver(self, driver):
        """
            Change driver.

            Driver name can be an alias like "nvidia173". If needed,
            the driver is enabled.
        """

        self.driver = driver
        self.outputs = {}
        self.enableDriver()

    def enableDriver(self):
        package = self.driverInfo().get("package")
        oldpackage = enabledPackage()
        if package != oldpackage:
            link = comar.Link()
            if oldpackage and oldpackage.replace("-", "_") in list(link.Xorg.Driver):
                link.Xorg.Driver[oldpackage].disable(timeout=2**16-1)

            if package:
                link.Xorg.Driver[package].enable(timeout=2**16-1)

    def preferredDriver(self, installed=True):
        if isVirtual():
            return "fbdev" if os.path.exists("/dev/fb0") else None

        cardId = self.vendor_id + self.product_id
        for line in loadFile(consts.drivers_file):
            if line.startswith(cardId):
                driver = line.split()[1]
                if installed:
                    drvInfo = self.driverInfo(driver)
                    if not drvInfo:
                        return None
                return driver

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
