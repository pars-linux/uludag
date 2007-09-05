# -*- coding: utf-8 -*-

from zorg.config import XConfig, ZorgConfig
from zorg.probe import *
from zorg.utils import *

def autoConfigure():
    # detect graphic cards and find monitor of first card
    devices = findVideoCards()
    if devices:
        device = devices[0]
    else:
        return

    for dev in devices:
        queryDevice(dev)

    monitor = None
    if device.monitors:
        if len(device.monitors) > 1 and not device.monitors[0].probed:
            monitor = device.monitors[1]
        else:
            monitor = device.monitors[0]

    screen = Screen(device, monitor)
    #screen.number = 0
    if monitor:
        screen.res = monitor.res[0]
    #screen.setup()

    config = XConfig()
    config.new()
    config.setKeyboard(XkbLayout=queryKeymap())
    config.setTouchpad(queryTouchpad())
    config.setPrimaryScreen(screen)

    config.layout = "singleHead"
    config.finalize()
    config.save()

    z = ZorgConfig()
    for dev in devices:
        z.addCard(dev)
        for mon in dev.monitors:
            z.addMonitor(mon)

    z.setScreen(screen)
    z.save()

    updateOpenGL(driver2opengl(device.driver), "false")

def safeConfigure(driver = "vesa"):
    safedrv = driver.upper()

    dev = Device()
    dev.cardId = "%s_CONFIGURED_CARD" % safedrv
    dev.boardName = "%s Configured Board" % safedrv
    dev.vendorName = "%s Configured Vendor" % safedrv
    dev.driver = driver

    # set failsafe monitor stuff
    mon = DefaultMonitor()
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

    z = ZorgConfig()
    z.addCard(dev)
    z.addMonitor(mon)
    z.setScreen(screen)
    z.save()

def setCardOptions(cardId, options):
    z = ZorgConfig()

    card = z.getCard(cardId)

    if not card:
        fail("Device ID is not correct: %s" % cardId)

    opts = dict(x.split("=", 1) for x in options.strip().splitlines())

    if opts.has_key("driver"):
        driver = opts["driver"]
        if driver in listAvailableDrivers():
            card.driver = driver
        else:
            fail("Driver does not exist: %s" % driver)

    z.addCard(card)
    updateXorgConf(z)
    z.save()

def addMonitor(monitorData):
    z = ZorgConfig()

    info = dict(x.split("=", 1) for x in monitorData.strip().splitlines())
    flags = info.get("flags", "")

    mon = Monitor()
    defmon = DefaultMonitor()

    mon.eisaid = info.get("eisaid", "")
    mon.probed = "probed" in flags
    mon.digital = "digital" in flags
    mon.hsync_min = info.get("hsync_min", defmon.hsync_min)
    mon.hsync_max = info.get("hsync_max", defmon.hsync_max)
    mon.vref_min = info.get("vref_min", defmon.vref_min)
    mon.vref_max = info.get("vref_max", defmon.vref_max)
    mon.vendorname = info.get("vendorname", "UNKNOWN")
    mon.modelname = info.get("modelname", "UNKNOWN")
    mon.res = info.get("resolutions", "800x600,640x480").split(",")

    if mon.eisaid:
        mon.id = "EISA_%s" % mon.eisaid
    else:
        if mon.modelname:
            prefix = "MODEL_%s" % mon.modelname.replace(" ", "_")
        else:
            prefix = "MONITOR"

        ID = prefix
        index = 0
        while z.getMonitor(ID):
            ID = "%s_%s" % (prefix, index)
            index += 1

        mon.id = ID

    z.addMonitor(mon)
    z.save()

def removeMonitor(monitorId):
    z = ZorgConfig()
    z.removeMonitor(monitorId)
    z.save()

def probeMonitors():
    # We need to find a way to get primary device first.
    pass

def installINF(filePath):
    pass

def setScreen(screenNumber, cardId, monitorId, mode):
    if screenNumber not in ("0", "1"):
        fail("Invalid screen number: %s" % screenNumber)

    res, depth = parseMode(mode)
    if not res:
        fail("Invalid mode: %s" % mode)

    z = ZorgConfig()

    config = XConfig()
    config.load()
    config.removeScreens()

    dev = z.getCard(cardId)
    if not dev:
        fail("Card ID is incorrect: %s" % cardId)

    mon = z.getMonitor(monitorId)
    if not mon:
        fail("Monitor ID is incorrect: %s" % monitorId)

    scr = Screen(dev, mon)
    scr.number = int(screenNumber)
    scr.res = res
    scr.depth = depth

    if screenNumber == "0":
        config.setPrimaryScreen(scr)
        scr1 = z.getScreen(1)
        if scr1:
            config.setSecondaryScreen(scr1)
    else:
        scr0 = z.getScreen(0)
        if scr0:
            config.setPrimaryScreen(scr0)
        config.setSecondaryScreen(scr)

    config.save()
    z.setScreen(scr)
    z.save()

def updateXorgConf(z):
    scr0 = z.getScreen(0)
    scr1 = z.getScreen(1)

    config = XConfig()
    config.load()
    config.removeScreens()

    # Do z.setScreen against possible changes.
    # e.g. depth can be set to 24 if fglrx is used.
    config.setPrimaryScreen(scr0)
    z.setScreen(scr0)
    if scr1:
        config.setSecondaryScreen(scr1)
        z.setScreen(scr1)

    config.save()

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
