# -*- coding: utf-8 -*-

import os
import dbus

import comar
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
        secScr,
        secLay
    ]

    if jailEnabled():
        jailOpts = {
                "DontVTSwitch" : "true",
                }
        secFlags.options.update(jailOpts)

    # Device section
    secDevice.set("Identifier", "VideoCard")
    drvInfo = card.driverInfo()
    if drvInfo:
        secDevice.set("Driver", drvInfo["xorg-module"])

    if card.driver == "fglrx":
        card.depth = 24

    # Monitor sections
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

    # Screen section
    secScr.set("Identifier", "Screen")
    secScr.set("Device", "VideoCard")
    if card.depth:
        secScr.set("DefaultDepth", card.depth)

    if "default" in card.outputs:
        output = card.outputs["default"]
        secScr.set("Monitor", "Monitor[default]")

        if output.mode:
            subsec = XorgSection("Display")
            if card.depth:
                subsec.set("Depth", card.depth)
            subsec.set("Modes", output.mode, "800x600", "640x480")
            secScr.sections = [subsec]

    # Layout section
    secLay.set("Identifier", "Layout")
    secLay.set("Screen", "Screen")

    # If this driver has an Xorg.Driver script,
    # call its methods to update sections.
    pkg = drvInfo.get("package")
    if pkg:
        link = comar.Link()
        opts = dbus.Dictionary(secDevice.options, signature="ss")
        try:
            secDevice.options = link.Xorg.Driver[pkg].getDeviceOptions(
                                    card.bus_id, opts)
        except dbus.DBusException:
            pass

    # Backup and save xorg.conf
    backup(consts.xorg_conf_file)

    f = open(consts.xorg_conf_file, "w")
    f.write(parser.toString())

    f = open(consts.configured_bus_file, "w")
    f.write(card.bus_id)

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

    driver = cardTag.getTagData("Driver")
    activeConfigTag = cardTag.getTag("ActiveConfig")

    if driver:
        device.driver = driver
    elif activeConfigTag:
        driver = activeConfigTag.getTagData("Driver")
        if driver:
            device.driver = driver

    depth = cardTag.getTagData("Depth")
    if depth:
        device.depth = int(depth)

    def addMonitor(output, tag):
        mon = Monitor()
        mon.vendor = tag.getTagData("Vendor") or ""
        mon.model  = tag.getTagData("Model") or "Unknown Monitor"
        mon.hsync  = tag.getTagData("HorizSync") or mon.hsync
        mon.vref   = tag.getTagData("VertRefresh") or mon.vref
        device.monitors[output] = mon

    # Get output info
    outputsTag = cardTag.getTag("Outputs")
    if outputsTag:
        for outputTag in outputsTag.tags("Output"):
            name = outputTag.getAttribute("name")
            output = Output(name)
            device.outputs[name] = output

            enabled = outputTag.getTagData("Enabled")
            if enabled:
                output.setEnabled(enabled == "true")
            ignored = outputTag.getTagData("Ignored")
            if ignored:
                output.setIgnored(ignored == "true")

            mode = outputTag.getTagData("Mode") or ""
            rate = outputTag.getTagData("RefreshRate") or ""
            output.setMode(mode, rate)

            rotation = outputTag.getTagData("Rotation")
            if rotation:
                output.setOrientation(rotation)

            rightOf = outputTag.getTagData("RightOf")
            below = outputTag.getTagData("Below")
            if rightOf:
                output.setPosition("RightOf", rightOf)
            elif below:
                output.setPosition("Below", below)

            monitorTag = outputTag.getTag("Monitor")
            if monitorTag:
                addMonitor(name, monitorTag)

    return device

def saveDeviceInfo(card):
    if not os.path.exists(consts.config_dir):
        os.mkdir(consts.config_dir, 0755)

    try:
        doc = piksemel.parse(consts.config_file)
    except OSError:
        doc = piksemel.newDocument("ZORG")

    for tag in doc.tags("Card"):
        if tag.getAttribute("busId") == card.bus_id:
            tag.hide()
            break

    cardTag = doc.insertTag("Card")
    cardTag.setAttribute("busId", card.bus_id)

    addTag(cardTag, "VendorId", card.vendor_id)
    addTag(cardTag, "ProductId", card.product_id)

    if card.driver:
        addTag(cardTag, "Driver", card.driver)

    if card.depth:
        addTag(cardTag, "Depth", str(card.depth))

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

def getKeymap():
    layout = None
    variant = ""

    try:
        doc = piksemel.parse(consts.config_file)

        keyboard = doc.getTag("Keyboard")
        if keyboard:
            layout = keyboard.getTagData("Layout")
            variant = keyboard.getTagData("Variant") or ""

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
