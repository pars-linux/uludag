#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import sys
import time

from qt import *
from kdecore import *
from kdeui import *

import zorg.config
from zorg.utils import *

import randriface
from handler import CallHandler

all_modes = [
    "2048x1536",
    "1920x1440",
    "1920x1200",
    "1680x1050",
    "1600x1024",
    "1440x900",
    "1400x1050",
    "1280x1024",
    "1280x960",
    "1280x800",
    "1280x768",
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
        return ch

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
        self._rriface = randriface.RandRIface()

        self._bus = comlink.call("zorg", "Xorg.Display", "activeDeviceID")
        self._info = zorg.config.getDeviceInfo(self._bus)

        self.outputs = self._info.probe_result["outputs"].split(",")
        self.modes = {}
        self.current_modes = {}

        self._flags = self._info.probe_result.get("flags", "").split(",")
        #self._randr12 = "randr12" in self._flags
        self._randr12 = len(self._rriface.outputs) > 1

        if self._randr12:
            for output in self.outputs:
                modes = self._rriface.getResolutions(output)
                self.modes[output] = modes if modes else all_modes

                current = self._rriface.currentResolution(output)
                self.current_modes[output] = current if current else self.modes[output][0]

        else:
            if self._info.driver == "fglrx":
                connected_outputs, enabled_outputs = fglrxOutputInfo()

                for out in connected_outputs:
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

        self.primaryScr = self._info.active_outputs[0]
        self.secondaryScr = None

        if len(self._info.active_outputs) > 1:
            self.secondaryScr = self._info.active_outputs[1]

        self.desktop_setup = self._info.desktop_setup
        self.depths = self._info.probe_result.get("depths", "16,24").split(",")
        self.true_color = self._info.depth == "24"

    def apply(self):
        options = {
                "depth":            "24" if self.true_color else "16",
                "desktop-setup":    self.desktop_setup
                }

        firstScreen = {
                "output":   self.primaryScr,
                "mode":     self.current_modes[self.primaryScr],
                }

        secondScreen = {"output":   ""}
        if self.desktop_setup != "single":
            secondScreen["output"] = self.secondaryScr
            secondScreen["mode"] = self.current_modes[self.secondaryScr]

        ch = comlink.callHandler("zorg", "Xorg.Display", "setupScreens", "tr.org.pardus.comar.xorg.display.set")
        ch.registerDone(self.done)
        ch.call(self._bus, options, firstScreen, secondScreen)

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
            run("aticonfig", "--dtop", self.desktop_setup)

    def done(self):
        KMessageBox.information(None, i18n("Saved your configuration."))
