#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import zorg.config

import randriface

class ComarLink:
    def __init__(self):
        self.bus = None
        self.iface = None

    def __getattr__(self, method):
        if not self.iface:
            self._connect()

        return getattr(self.iface, method)

    def _connect(self):
        self.bus = dbus.SystemBus()
        object = self.bus.get_object("tr.org.pardus.comar", "/package/zorg", introspect=False)
        self.iface = dbus.Interface(object, "tr.org.pardus.comar.Xorg.Display")

link = ComarLink()

class DisplayConfig:
    def __init__(self):
        self._rriface = randriface.RandRIface()

        self._bus = link.activeDeviceID()
        self._info = zorg.config.getDeviceInfo(self._bus)

        self._flags = self._info.probe_result.get("flags", "").split(",")
        self._randr12 = "randr12" in self._flags

        self.outputs = self._info.probe_result["outputs"].split(",")
        self.modes = {}
        self.current_modes = {}

        if self._randr12:
            for output in self.outputs:
                modes = self._rriface.getResolutions(output)
                self.modes[output] = modes if modes else ["800x600", "640x480"]

                current = self._rriface.currentResolution(output)
                self.current_modes[output] = current if current else self.modes[output][0]

        else:
            for output in self.outputs:
                pass

        self.primaryScr = self._info.active_outputs[0]
        self.secondaryScr = None

        if len(self._info.active_outputs) > 1:
            self.secondaryScr = self._info.active_outputs[1]

        self.desktop_setup = self._info.desktop_setup
        self.true_color = self._info.depth == "24"

    def setScreens(self, primary, secondary=None):
        self.primaryScr = primary
        if secondary:
            self.secondaryScr = secondary

    def setResolution(self, output, resolution):
        self.current_modes[output] = resolution

    def apply(self):
        options = {
                "depth":            "24" if self.true_color else "16",
                "desktop-setup":    self.desktop_setup
                }

        firstScreen = {
                "output":   self.primaryScr,
                "mode":     self.current_modes[self.primaryScr],
                }

        secondScreen = {}
        if self.desktop_setup != "single":
            secondScreen["output"] = self.secondaryScr
            secondScreen["mode"] = self.current_modes[self.secondaryScr]

        link.setScreens(self._bus, options, firstScreen, secondScreen)
