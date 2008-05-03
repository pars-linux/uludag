#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import zorg.config
from zorg.utils import *

import randriface

class ComarLink:
    def __init__(self):
        self.bus = dbus.SystemBus()

    def __getattr__(self, method):
        object = self.bus.get_object("tr.org.pardus.comar", "/package/zorg", introspect=False)
        iface = dbus.Interface(object, "tr.org.pardus.comar.Xorg.Display")

        return getattr(iface, method)

link = ComarLink()

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

        self._bus = link.activeDeviceID()
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
                self.modes[output] = modes if modes else ["800x600", "640x480"]

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
                else:
                    modes = ["1024x768", "800x600", "640x480"]

                self.modes[output] = modes
                self.current_modes[output] = self._info.modes.get(output, "800x600")

        self.primaryScr = self._info.active_outputs[0]
        self.secondaryScr = None

        if len(self._info.active_outputs) > 1:
            self.secondaryScr = self._info.active_outputs[1]

        self.desktop_setup = self._info.desktop_setup
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

        link.setupScreens(self._bus, options, firstScreen, secondScreen)

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
