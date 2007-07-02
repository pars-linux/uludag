#!/usr/bin/python
# -*- coding: utf-8 -*-

from zorg.config import *
from zorg.probe import *
from zorg.utils import *

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
        print "Could not detect a monitor on the first controller. Trying next..."
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
    dev.cardId = "%s_CONFIGURED_CARD" % safedrv
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

    cardIds = zconfig.get("cards").split(",")

    cards = []
    for cardId in cardIds:
        if not zconfig.hasSection(cardId):
            continue # zorg.conf is broken

        zconfig.setSection(cardId)
        vendorName = zconfig.get("vendorName")
        boardName = zconfig.get("boardName")
        cards.append("%s %s - %s" % (cardId, boardName, vendorName))

    return "\n".join(cards)

def setCardOptions(cardId, options):
    pass

def cardInfo(cardId):
    zconfig = ZorgConfig()

    if not zconfig.hasSection(cardId):
        return ""
    zconfig.setSection(cardId)

    info = []

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

def monitorInfo(monitorId):
    zconfig = ZorgConfig()

    if not zconfig.hasSection(monitorId):
        return ""

    zconfig.setSection(monitorId)
    info = []
    name = "%s - %s" % (zconfig.get("modelName"), zconfig.get("vendorName"))
    info.append("name=%s" % name)
    info.append("resolutions=%s" % zconfig.get("resolutions"))

    return "\n".join(info)

def addMonitor(monitorData):
    zconfig = ZorgConfig()

    numbers = set(atoi(lremove(x, "Monitor")) for x in zconfig.cp.sections() if x.startswith("Monitor"))
    numbers = list(set(xrange(len(numbers) + 1)) - numbers)
    numbers.sort()
    number = numbers[0]

    info = dict(x.split("=", 1) for x in monitorData.strip().splitlines())

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

        busId = zconfig.get("busId")
        vendorId = zconfig.get("vendorId")
        deviceId = zconfig.get("deviceId")

        dev = Device(busId, vendorId, deviceId)
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
        scr.res = info["resolution"]
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
    autoConfigure()
    print listCards()
    print cardInfo("PCI:0:5:0")
    print listMonitors("PCI:0:5:0")
    print monitorInfo("Monitor0")
    print getScreens()

    setScreens("""
card=10de:0240@PCI:0:5:0
monitor=Monitor0
resolution=1024x768
depth=24

card=10de:0240@PCI:0:5:0
monitor=Monitor0
resolution=800x600
depth=16

""")
    print getScreens()

    addMonitor("""
hsync_min=30
hsync_max=60
vref_min=50
vref_max=75
vendorname=VENDOR
modelname=MODEL
""")
    removeMonitor("Monitor2")
