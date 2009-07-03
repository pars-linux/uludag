# -*- coding: utf-8 -*-

import os

import piksemel

from zorg import consts
from zorg.parser import *
from zorg.probe import VideoDevice, Monitor, Output
from zorg.utils import *

def saveXorgConfig(card):
    parser = XorgParser()

    secFlags    = XorgSection("ServerFlags")
    secDevice   = XorgSection("Device")
    secScr      = XorgSection("Screen")
    secLay      = XorgSection("ServerLayout")

    parser.sections = [
        secFlags,
        secDevice,
    ]

    if card.needsScreenSection():
        parser.sections.extend([secScr, secLay])

    if jailEnabled():
        jailOpts = {
                "DontVTSwitch" : "true",
                }
        secFlags.options.update(jailOpts)

    info = card.getDict()

    secDevice.set("Identifier", "VideoCard")
    if card.driver:
        secDevice.set("Driver", card.driver)

    secDevice.options.update(card.driver_options)

    flags = card.flags()

    for name, output in card.outputs.items():
        identifier = "Monitor[%s]" % name

        monSec = XorgSection("Monitor")
        parser.sections.append(monSec)
        monSec.set("Identifier", identifier)

        if card.monitors.has_key(name):
            monSec.set("VendorName",  card.monitors[name].vendor)
            monSec.set("ModelName",   card.monitors[name].model)
            monSec.set("HorizSync",   unquoted(card.monitors[name].hsync))
            monSec.set("VertRefresh", unquoted(card.monitors[name].vref ))

        if "norandr" not in flags:
            secDevice.options["Monitor-%s" % name] = identifier

            if output.ignored:
                monSec.options["Ignore"] = "true"
                continue

            monSec.options["Enable"] = "true" if output.enabled else "false"

            if output.mode:
                monSec.options["PreferredMode"] = output.mode

            if output.refresh_rate:
                monSec.options["TargetRefresh"] = output.refresh_rate

            if output.rotation:
                monSec.options["Rotate"] = output.rotation

            if output.right_of:
                monSec.options["RightOf"] = output.right_of
            elif output.below:
                monSec.options["Below"] = output.below

    if card.needsScreenSection():
        secScr.set("Identifier", "Screen")
        secScr.set("Device", "VideoCard")
        if card.active_outputs:
            secScr.set("Monitor", "Monitor[%s]" % card.active_outputs[0])
        secScr.set("DefaultDepth", atoi(card.depth))

        subsec = XorgSection("Display")
        subsec.set("Depth", atoi(card.depth))

        if card.needsModesLine():
            output = card.active_outputs[0]
            if card.modes.has_key(output):
                subsec.set("Modes", card.modes[output], "800x600", "640x480")

            secScr.sections = [subsec]

        secLay.set("Identifier", "Layout")
        secLay.set("Screen", "Screen")

    backup(consts.xorg_conf_file)

    f = open(consts.xorg_conf_file, "w")
    f.write(parser.toString())
    f.close()

def configuredBus():
    try:
        return open(consts.configured_bus_file).read()
    except IOError:
        return ""

def addTag(p, name, data):
    t = p.insertTag(name)
    t.insertData(data)

def getDeviceInfo(busId):
    if not os.path.exists(consts.config_file):
        return

    doc = piksemel.parse(consts.config_file)

    cardTag = None
    for tag in doc.tags("Card"):
        if tag.getAttribute("busId") == busId:
            cardTag = tag
            break

    if not cardTag:
        return

    device = VideoDevice(busId=busId)

    device.saved_vendor_id  = cardTag.getTagData("VendorId")
    device.saved_product_id = cardTag.getTagData("ProductId")

    probeResultTag = cardTag.getTag("ProbeResult")
    probeResult = {}
    for tag in probeResultTag.tags("Value"):
        key = tag.getAttribute("key")
        child = tag.firstChild()
        if child:
            value = child.data()
        else:
            value = ""
        probeResult[key] = value

    activeConfigTag = cardTag.getTag("ActiveConfig")

    driverTag = activeConfigTag.getTag("Driver")
    if driverTag:
        device.driver = driverTag.firstChild().data()
        device.package = driverTag.getAttribute("package")
    else:
        device.driver = None

    initial = activeConfigTag.getAttribute("initial")
    if initial and initial == "true":
        return device

    device.depth = activeConfigTag.getTagData("Depth")

    activeOutputs = []
    modes = {}

    def addMonitor(output, tag):
        mon = Monitor()
        mon.vendor = tag.getTagData("Vendor") or ""
        mon.model  = tag.getTagData("Model") or "Unknown Monitor"
        mon.hsync  = tag.getTagData("HorizSync") or mon.hsync
        mon.vref   = tag.getTagData("VertRefresh") or mon.vref
        device.monitors[output] = mon

    outputTag = activeConfigTag.getTag("Output")
    name = outputTag.firstChild().data()
    activeOutputs.append(name)
    mode = outputTag.getAttribute("mode")
    if mode:
        modes[name] = mode

    monitorTag = activeConfigTag.getTag("Monitor")
    if monitorTag:
        addMonitor(name, monitorTag)

    outputTag = activeConfigTag.getTag("SecondOutput")
    if outputTag:
        name = outputTag.firstChild().data()
        activeOutputs.append(name)
        mode = outputTag.getAttribute("mode")
        if mode:
            modes[name] = mode

        monitorTag = activeConfigTag.getTag("SecondMonitor")
        if monitorTag:
            addMonitor(name, monitorTag)

    # Get output info
    outputsTag = cardTag.getTag("Outputs")
    for outputTag in outputsTag.tags("Output"):
        name = outputTag.getAttribute("name")
        output = Output(name)
        device.outputs[name] = output

        enabledTag = outputTag.getTag("Enabled")
        if enabledTag:
            output.setEnabled(enabledTag.firstChild().data() == "true")
        ignoredTag = outputTag.getTag("Ignored")
        if ignoredTag:
            output.setIgnored(ignoredTag.firstChild().data() == "true")

        mode = ""
        rate = ""
        modeTag = outputTag.getTag("Mode")
        if modeTag:
            mode = modeTag.firstChild().data()
        rateTag = outputTag.getTag("RefreshRate")
        if rateTag:
            rate = rateTag.firstChild().data()
        output.setMode(mode, rate)

        rotationTag = outputTag.getTag("Rotation")
        if rotationTag:
            output.setOrientation(rotationTag.firstChild().data())

        rightOfTag = outputTag.getTag("RightOf")
        belowTag = outputTag.getTag("Below")
        if rightOfTag:
            output.setPosition("RightOf", rightOfTag.firstChild().data())
        elif belowTag:
            output.setPosition("Below", belowTag.firstChild().data())

        monitorTag = outputTag.getTag("Monitor")
        if monitorTag:
            addMonitor(name, monitorTag)

    device.desktop_setup = activeConfigTag.getTagData("DesktopSetup")

    device.probe_result = probeResult
    device.active_outputs = activeOutputs
    device.modes = modes

    return device

def saveDeviceInfo(card):
    if not os.path.exists(consts.config_dir):
        os.mkdir(consts.config_dir, 0755)

    try:
        doc = piksemel.parse(consts.config_file)
    except OSError:
        doc = piksemel.newDocument("ZORG")

    info = card.getDict()

    for tag in doc.tags("Card"):
        if tag.getAttribute("busId") == info["bus-id"]:
            tag.hide()
            break

    cardTag = doc.insertTag("Card")
    cardTag.setAttribute("busId", info["bus-id"])

    addTag(cardTag, "VendorId", card.vendor_id)
    addTag(cardTag, "ProductId", card.product_id)

    probeResult = cardTag.insertTag("ProbeResult")
    for key, value in card.probe_result.items():
        t = probeResult.insertTag("Value")
        t.setAttribute("key", key)
        if value:
            t.insertData(value)

    config = cardTag.insertTag("ActiveConfig")

    if card.driver:
        driver = config.insertTag("Driver")
        driver.setAttribute("package", card.package)
        driver.insertData(card.driver)

    if card.initial:
        config.setAttribute("initial", "true")
    else:
        if card.depth:
            addTag(config, "Depth", card.depth)
        addTag(config, "DesktopSetup", card.desktop_setup)

        def addMonitor(output, tagName):
            mon = card.monitors[output]
            monitor = config.insertTag(tagName)
            monitor.insertTag("Vendor").insertData(mon.vendor)
            monitor.insertTag("Model" ).insertData(mon.model )
            monitor.insertTag("HorizSync"  ).insertData(mon.hsync)
            monitor.insertTag("VertRefresh").insertData(mon.vref)

        outName = card.active_outputs[0]
        outMode = card.modes.get(outName)
        output = config.insertTag("Output")
        if outMode:
            output.setAttribute("mode", outMode)
        output.insertData(outName)

        if card.monitors.has_key(outName):
            addMonitor(outName, "Monitor")

        if card.desktop_setup != "single":
            outName = card.active_outputs[1]
            outMode = card.modes.get(outName)
            output = config.insertTag("SecondOutput")
            if outMode:
                output.setAttribute("mode", outMode)
            output.insertData(outName)

            if card.monitors.has_key(outName):
                addMonitor(outName, "SecondMonitor")

    # Save output info
    outputs = cardTag.insertTag("Outputs")
    for name, output in card.outputs.items():
        out = outputs.insertTag("Output")
        out.setAttribute("name", name)
        addTag(out, "Enabled", "true" if output.enabled else "false")
        addTag(out, "Ignored", "true" if output.ignored else "false")
        if output.mode:
            addTag(out, "Mode", output.mode)
        if output.refresh_rate:
            addTag(out, "RefreshRate", output.refresh_rate)
        if output.rotation:
            addTag(out, "Rotation", output.rotation)
        if output.right_of:
            addTag(out, "RightOf", output.right_of)
        if output.below:
            addTag(out, "Below", output.below)

        if name in card.monitors:
            mon = card.monitors[name]
            monitor = out.insertTag("Monitor")
            addTag(monitor, "Vendor", mon.vendor)
            addTag(monitor, "Model", mon.model)
            addTag(monitor, "HorizSync", mon.hsync)
            addTag(monitor, "VertRefresh", mon.vref)

    f = open(consts.config_file, "w")
    f.write(doc.toPrettyString().replace("\n\n", ""))

    f = open(consts.configured_bus_file, "w")
    f.write(info["bus-id"])

def getKeymap():
    layout = None
    variant = ""

    try:
        doc = piksemel.parse(consts.config_file)

        keyboard = doc.getTag("Keyboard")
        if keyboard:
            layoutTag = keyboard.getTag("Layout")
            if layoutTag:
                layout = layoutTag.firstChild().data()

            variantTag = keyboard.getTag("Variant")
            if variantTag:
                variant = variantTag.firstChild().data()

    except OSError:
        pass

    if not layout:
        from pardus.localedata import languages

        try:
            language = file("/etc/mudur/language").read().strip()
        except IOError:
            language = "en"

        if not languages.has_key(language):
            language = "en"

        keymap = languages[language].keymaps[0]
        layout = keymap.xkb_layout
        variant = keymap.xkb_variant

    return layout, variant

def saveKeymap(layout, variant=""):
    if not os.path.exists(consts.config_dir):
        os.mkdir(consts.config_dir, 0755)

    try:
        doc = piksemel.parse(consts.config_file)
    except OSError:
        doc = piksemel.newDocument("ZORG")

    keyboardTag = doc.getTag("Keyboard")

    if keyboardTag:
        keyboardTag.hide()

    keyboardTag = doc.insertTag("Keyboard")
    keyboardTag.insertTag("Layout").insertData(layout)
    if variant:
        keyboardTag.insertTag("Variant").insertData(variant)

    f = file(consts.config_file, "w")
    f.write(doc.toPrettyString().replace("\n\n", ""))
