#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import subprocess

class Output:
    def __init__(self, name):
        self.name = name
        self.connected = False
        self.modes = []
        self.preferred = ""
        self.current = ""
        self.primary = False

class RandRIface:
    def __init__(self):
        self.detect()

    def detect(self):
        self.outputs = []

        output_pattern = re.compile("(.*) (.*connected) *(\d+x\d+\+\d+\+\d+)?")
        mode_pattern = re.compile("   (\S*) .+")

        p = subprocess.Popen(["xrandr"], stdout=subprocess.PIPE)
        out, err = p.communicate()

        output = None
        for line in out.splitlines():
            if "connected" in line:
                matched = output_pattern.match(line)
                if matched:
                    name, status, geometry = matched.groups()
                    output = Output(name)
                    self.outputs.append(output)
                    output.connected = (status == "connected")
                    if geometry and geometry.endswith("+0+0"):
                        output.primary = True

            elif output:
                matched = mode_pattern.match(line)
                if matched:
                    mode = matched.groups()[0]
                    output.modes.append(mode)

                    if "+" in line:
                        output.preferred = mode

                    if "*" in line:
                        output.current = mode

    def getResolutions(self, output):
        for out in self.outputs:
            if out.name == output:
                return out.modes

    def currentResolution(self, output):
        for out in self.outputs:
            if out.name == output:
                return out.current

    def setResolution(self, output):
        pass
