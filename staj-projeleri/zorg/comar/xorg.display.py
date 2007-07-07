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

    updateOpenGL(driver2opengl(device.driver), "false")

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
    zconfig = ZorgConfig()

    if not zconfig.hasSection(cardId):
        fail("Device ID is not correct: %s" % cardId)
    zconfig.setSection(cardId)

    opts = dict(x.split("=", 1) for x in options.strip().splitlines())

    if opts.has_key("driver"):
        driver = opts["driver"]
        if driver in listAvailableDrivers():
            zconfig.set("driver", driver)
        else:
            fail("Driver does not exist: %s" % driver)

    zconfig.write()
    updateXorgConf()

def cardInfo(cardId):
    zconfig = ZorgConfig()

    if not zconfig.hasSection(cardId):
        return ""
    zconfig.setSection(cardId)

    info = []

    info.append("vendorName=%s" % zconfig.get("vendorName"))
    info.append("boardName=%s" % zconfig.get("boardName"))
    info.append("vendorId=%s" % zconfig.get("vendorId"))
    info.append("deviceId=%s" % zconfig.get("deviceId"))
    info.append("busId=%s" % zconfig.get("busId"))
    info.append("driver=%s" % zconfig.get("driver"))
    info.append("monitors=%s" % zconfig.get("monitors"))

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
    #name = "%s - %s" % (zconfig.get("modelName"), zconfig.get("vendorName"))
    #info.append("name=%s" % name)
    info.append("vendorName=%s" % zconfig.get("vendorName"))
    info.append("modelName=%s" % zconfig.get("modelName"))
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

def screenInfo(screenNumber):
    zconfig = ZorgConfig()
    scr = "Screen%s" % screenNumber

    if not zconfig.hasSection(scr):
        return ""
    zconfig.setSection(scr)

    scrInfo = []
    for option in "card", "monitor", "resolution", "depth":
        scrInfo.append("%s=%s" % (option, zconfig.get(option)))

    return "\n".join(scrInfo)


def setScreen(screenNumber, cardId, monitorId, mode):
    if screenNumber not in ("0", "1"):
        fail("Invalid screen number: %s" % screenNumber)

    res, depth = parseMode(mode)
    if not res:
        fail("Invalid mode: %s" % mode)

    zconfig = ZorgConfig()

    config = XConfig()
    config.load()
    config.removeScreens()

    if not zconfig.hasSection(cardId):
        fail("Card ID is incorrect: %s" % cardId)
    zconfig.setSection(cardId)

    busId = zconfig.get("busId")
    vendorId = zconfig.get("vendorId")
    deviceId = zconfig.get("deviceId")

    dev = Device(busId, vendorId, deviceId)
    dev.cardId = cardId
    dev.driver = zconfig.get("driver")
    dev.vendorName = zconfig.get("vendorName")
    dev.boardName = zconfig.get("boardName")

    if not zconfig.hasSection(monitorId):
        fail("Monitor ID is incorrect: %s" % monitorId)
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
    scr.res = res
    scr.depth = depth

    if screenNumber == "0":
        config.setPrimaryScreen(scr)
    else:
        config.setSecondaryScreen(scr)

    config.save()
    saveConfig(config)

def updateXorgConf():
    for n in "0", "1":
        scrData = screenInfo(n)
        scrInfo = dict(x.split("=", 1) for x in scrData.strip().splitlines())
        mode = "%s-%s" % (scrInfo["resolution"], scrInfo["depth"])
        setScreen(n, scrInfo["card"], scrInfo["monitor"], mode)

def updateOpenGL(implementation, withHeaders):
    import zorg.opengl
    o = zorg.opengl.OpenGL()

    if withHeaders.lower() != "true" and implementation == o.current:
        return

    if withHeaders == "true":
        o.impheaders = True

    if implementation in o.available:
        o.setCurrent(implementation)
    else:
        fail("No such implementation: %s" % implementation)

