#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import sys
import time

from qt import *
from kdecore import *
from kdeui import *

import zorg.config
from zorg.consts import *
from zorg.utils import *

import randriface
from handler import CallHandler

all_modes = [
    "2048x1536",
    "1920x1440",
    "1920x1200",
    "1680x1050",
    "1600x1200",
    "1600x1024",
    "1440x900",
    "1400x1050",
    "1366x768",
    "1360x1024",
    "1360x768",
    "1280x1024",
    "1280x960",
    "1280x800",
    "1280x768",
    "1280x720", # 720p
    "1152x864",
    "1152x768",
    "1024x768",
    "800x600",
    "640x480"
]

class DBusInterface:
    def __init__(self):
        self.dia = None
        self.busSys = None
        self.busSes = None

        self.winID = 0

        self.openBus()
        #if self.openBus():
        #    self.setup()

    def openBus(self):
        try:
            self.busSys = dbus.SystemBus()
            self.busSes = dbus.SessionBus()
        except dbus.DBusException, exception:
            self.errorDBus(exception)
            return False
        return True

    def callHandler(self, script, model, method, action):
        ch = CallHandler(script, model, method, action, self.winID, self.busSys, self.busSes)
        ch.registerError(self.error)
        ch.registerDBusError(self.errorDBus)
        ch.registerAuthError(self.errorDBus)
        ch.registerCancel(self.cancelError)
        return ch

    def cancelError(self):
        message = i18n("You are not authorized for this operation.")
        KMessageBox.sorry(None, message, i18n("Error"))

    def call(self, script, model, method, *args):
        try:
            obj = self.busSys.get_object("tr.org.pardus.comar", "/package/%s" % script)
            iface = dbus.Interface(obj, dbus_interface="tr.org.pardus.comar.%s" % model)
        except dbus.DBusException, exception:
            self.errorDBus(exception)
        try:
            func = getattr(iface, method)
            return func(*args)
        except dbus.DBusException, exception:
            self.error(exception)

    def callSys(self, method, *args):
        try:
            obj = self.busSys.get_object("tr.org.pardus.comar", "/")
            iface = dbus.Interface(obj, dbus_interface="tr.org.pardus.comar")
        except dbus.DBusException, exception:
            self.errorDBus(exception)
            return
        try:
            func = getattr(iface, method)
            return func(*args)
        except dbus.DBusException, exception:
            self.error(exception)

    def error(self, exception):
        if "Access denied" in exception.message:
            message = i18n("You are not authorized for this operation.")
            KMessageBox.sorry(None, message, i18n("Error"))
        else:
            KMessageBox.error(None, str(exception), i18n("COMAR Error"))

    def errorDBus(self, exception):
        if self.dia:
            return
        self.dia = KProgressDialog(None, "lala", i18n("Waiting DBus..."), i18n("Connection to the DBus unexpectedly closed, trying to reconnect..."), True)
        self.dia.progressBar().setTotalSteps(50)
        self.dia.progressBar().setTextEnabled(False)
        self.dia.show()
        start = time.time()
        while time.time() < start + 5:
            if self.openBus():
                self.dia.close()
                #self.setup()
                return
            if self.dia.wasCancelled():
                break
            percent = (time.time() - start) * 10
            self.dia.progressBar().setProgress(percent)
            qApp.processEvents(100)
        self.dia.close()
        KMessageBox.sorry(None, i18n("Cannot connect to the DBus! If it is not running you should start it with the 'service dbus start' command in a root console."))
        sys.exit()

comlink = DBusInterface()

def fglrxOutputInfo():
    connected_outputs = []
    enabled_outputs = []

    out, err = capture("aticonfig", "--query-monitor")

    lines = out.splitlines()
    for line in lines:
        if "Connected monitors" in line:
            outputs = line.split(": ")[1]
            connected_outputs = outputs.split(", ")
        elif "Enabled monitors" in line:
            outputs = line.split(": ")[1]
            enabled_outputs = outputs.split(", ")

    return connected_outputs, enabled_outputs

class DisplayConfig:
    def __init__(self):
        self._bus = comlink.call("zorg", "Xorg.Display", "activeDeviceID")
        self._info = zorg.config.getDeviceInfo(self._bus)

        if not self._info:
            answer = KMessageBox.questionYesNo(None, i18n("Display manager cannot get configuration information. Configuration file may be corrupted or modified by another tool. If you want to use display manager to configure your video hardware, you must create a new configuration file.\nWould you like to create a new configuration at the next boot?"))
            if answer == KMessageBox.Yes:
                ch = comlink.callHandler("zorg", "Xorg.Display", "setPendingConfig", "tr.org.pardus.comar.xorg.display.set")
                ch.registerDone(self.startupProbe)
                ch.call({"":""})
            return

        self.card_vendor_id = self._info.vendor_id
        self.card_product_id = self._info.product_id

        self.desktop_setup = self._info.desktop_setup
        self.outputs = self._info.probe_result.get("outputs", "default").split(",")
        self.monitors = self._info.monitors

        self._flags = self._info.probe_result.get("flags", "").split(",")

        self.detect()

        self.primaryScr = self._info.active_outputs[0]
        self.secondaryScr = None

        if len(self._info.active_outputs) > 1:
            self.secondaryScr = self._info.active_outputs[1]

        self.currentPrimaryScr = self.primaryScr
        self.currentSecondaryScy = self.secondaryScr

        if self.desktop_setup != "single" and self.secondaryScr is None:
            self.desktop_setup = "single"

        self.depths = self._info.probe_result.get("depths", "16,24").split(",")
        self.true_color = self._info.depth == "24"

        self.driver_changed = False

    def detect(self):
        self._rriface = randriface.RandRIface()
        #self._randr12 = "randr12" in self._flags
        self._randr12 = self._rriface.outputs[0].name != "default"

        self.modes = {}
        self.current_modes = {}

        if self._randr12:
            self.outputs = [output.name for output in self._rriface.outputs]

            for output in self.outputs:
                modes = self._rriface.getResolutions(output)
                if modes:
                    self.modes[output] = modes
                else:
                    self.modes[output] = all_modes

                current = self._rriface.currentResolution(output)
                if current:
                    self.current_modes[output] = current
                else:
                    modes = self.modes[output]
                    for mode in ("1024x768", "800x600", "640x480"):
                        if mode in modes:
                            self.current_modes[output] = mode
                            break
                    else:
                        self.current_modes[output] = modes[0]

            enabled_outputs = filter(lambda x: x.current, self._rriface.outputs)
            active_outputs = map(lambda x: x.name, enabled_outputs)
            self._info.active_outputs = active_outputs if enabled_outputs[0].primary else active_outputs[::-1]

        else:
            if self._info.driver == "fglrx":
                connected_outputs, enabled_outputs = fglrxOutputInfo()
                outputs = connected_outputs + enabled_outputs
                self._info.active_outputs = enabled_outputs

                for out in outputs:
                    if out not in self.outputs:
                        self.outputs.append(out)

            for output in self.outputs:
                if self._info.probe_result.has_key("%s-modes" % output):
                    modes = self._info.probe_result["%s-modes" % output].split(",")
                    if "" in modes:
                        modes = all_modes
                else:
                    modes = all_modes

                self.modes[output] = modes
                self.current_modes[output] = self._info.modes.get(output, "800x600")

            if self.desktop_setup == "single":
                out = self._info.active_outputs[0]
                if not self._info.modes.has_key(out):
                    self.current_modes[out] = self._rriface.currentResolution("default")

        for output in self.outputs:
            if self.monitors.has_key(output):
                for mode in all_modes:
                    if mode not in self.modes[output]:
                        self.modes[output].append(mode)

    def apply(self):
        if self.true_color or self._info.driver == "fglrx":
            depth = "24"
        else:
            depth = "16"

        if self.driver_changed:
            config = {
                    "driver":   self._info.driver + package_sep + self._info.package,
                    "depth":    depth
                    }

            if self.monitors.has_key(self.primaryScr):
                mon = self.monitors[self.primaryScr]
                config["monitor-vendor"] = mon.vendor
                config["monitor-model"]  = mon.model
                config["monitor-hsync"]  = mon.hsync
                config["monitor-vref"]   = mon.vref

            ch = comlink.callHandler("zorg", "Xorg.Display", "setPendingConfig", "tr.org.pardus.comar.xorg.display.set")
            ch.registerDone(self.done)
            ch.call(config)
            return

        options = {
                "depth":            depth,
                "desktop-setup":    self.desktop_setup
                }

        def screenInfo(output):
            screen = {
                    "output":   output,
                    "mode":     self.current_modes[output]
                    }

            if self.monitors.has_key(output):
                mon = self.monitors[output]
                opts = {
                    "monitor-vendor":   mon.vendor,
                    "monitor-model":    mon.model,
                    "monitor-hsync":    mon.hsync,
                    "monitor-vref":     mon.vref
                    }
                screen.update(opts)

            return screen

        firstScreen = screenInfo(self.primaryScr)

        if self.desktop_setup == "single":
            secondScreen = {"output":   ""}
        else:
            secondScreen = screenInfo(self.secondaryScr)

        ch = comlink.callHandler("zorg", "Xorg.Display", "setupScreens", "tr.org.pardus.comar.xorg.display.set")
        ch.registerCancel(self.cancelled)
        ch.registerDone(self.done)
        ch.call(self._bus, options, firstScreen, secondScreen)

    def applyNow(self):
        if self._randr12:
            if self.desktop_setup == "single":
                run("xrandr", "--output", self.primaryScr, "--mode", self.current_modes[self.primaryScr])

                for out in self.outputs:
                    if out != self.primaryScr:
                        run("xrandr", "--output", out, "--off")

            elif self.desktop_setup == "clone":
                run("xrandr",
                        "--output", self.primaryScr,
                        "--mode",   self.current_modes[self.primaryScr],
                        "--output", self.secondaryScr,
                        "--mode",   self.current_modes[self.secondaryScr],
                        "--same-as", self.primaryScr
                    )

            elif self.desktop_setup == "horizontal":
                run("xrandr",
                        "--output", self.primaryScr,
                        "--mode",   self.current_modes[self.primaryScr],
                        "--output", self.secondaryScr,
                        "--mode",   self.current_modes[self.secondaryScr],
                        "--right-of", self.primaryScr
                    )

        elif self._info.driver == "fglrx":
            outputs = self.primaryScr

            tempFile = KTempFile()
            tempFile.setAutoDelete(True)

            cmd = ["aticonfig",
                    "--effective", "startup",
                    "--nobackup", "--output", tempFile.name(),
                    "--dtop", self.desktop_setup,
                    ]

            if self.desktop_setup != "single":
                outputs += "," + self.secondaryScr
                cmd += ["--mode2", self.current_modes[self.secondaryScr]]

            cmd += ["--enable-monitor", outputs]

            run(*cmd)

        if not self._randr12:
            if self.desktop_setup == "single" and \
                self.currentPrimaryScr == self.primaryScr:
                run("xrandr", "-s", self.current_modes[self.primaryScr])

        run("xrefresh")

    def driverName(self):
        return self._info.driver or "auto"

    def changeDriver(self, driver):
        self.driver_changed = True
        if package_sep in driver:
            drv, pkg = driver.split(package_sep, 1)
        else:
            drv, pkg = driver, "xorg-video"

        self._info.driver = drv
        self._info.package = pkg

    def cancelled(self):
        self.applyNow()

    def done(self):
        self.applyNow()
        KMessageBox.information(None, i18n("Configuration has been saved. Some changes may take effect after restarting your computer."))

    def startupProbe(self):
        KMessageBox.information(None, i18n("Your hardware will be probed after restarting your computer."))
