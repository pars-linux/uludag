# -*- coding: utf-8 -*-

truecolor_cards = ["i810", "intel", "nv", "nvidia", "radeon", "fglrx"]
lcd_drivers = ["nv", "nvidia", "ati", "via", "i810",
               "intel", "sis", "savage", "neomagic"]
randr12_drivers = ["ati", "intel"]

opengl_impl = {
    "fglrx"     : "ati",
    "nvidia"    : "nvidia"
}

default_kmap = "trq"

synapticsOptions = {
    "Protocol" : "auto-dev",
    # "Device" : "/dev/input/mouse0",
    "LeftEdge" : "1700",
    "RightEdge" : "5300",
    "TopEdge" : "1700",
    "BottomEdge" : "4200",
    "FingerLow" : "25",
    "FingerHigh" : "30",
    "MaxTapTime" : "180",
    "MaxTapMove" : "220",
    "VertScrollDelta" : "100",
    "MinSpeed" : "0.09",
    "MaxSpeed" : "0.18",
    "AccelFactor" : "0.0015",
    "SHMConfig" : "true",
    # Option     "ClickTime" : "0"
}

alpsOptions = {
    "Protocol" : "auto-dev",
    "LeftEdge" : "130",
    "RightEdge" : "840",
    "TopEdge" : "130",
    "BottomEdge" : "640",
    "FingerLow" : "7",
    "FingerHigh" : "8",
    "MaxTapTime" : "300",
    "MaxTapMove" : "110",
    "EmulateMidButtonTime" : "75",
    "VertScrollDelta" : "20",
    "HorizScrollDelta" : "20",
    "MinSpeed" : "0.60",
    "MaxSpeed" : "1.10",
    "AccelFactor" : "0.030",
    "EdgeMotionMinSpeed" : "200",
    "EdgeMotionMaxSpeed" : "200",
    "UpDownScrolling" : "1",
    "CircularScrolling" : "1",
    "CircScrollDelta" : "0.1",
    "CircScrollTrigger" : "2",
    "SHMConfig" : "true",
    "Emulate3Buttons" : "true",
    # "ClickTime" : "0"
}

touchpadDevices = {"synaptics" : synapticsOptions,
                   "alps"      : alpsOptions}

class Device:
    def __init__(self, busId="", vendorId="", deviceId=""):
        self.identifier = None

        self.busId = busId
        self.vendorId = vendorId
        self.deviceId = deviceId

        self.id = "%s:%s@%s" % (self.vendorId, self.deviceId, self.busId)

        self.driver = None
        self.vendorName = "Unknown Vendor"
        self.boardName = "Unknown Board"

        self.outputs = {}
        self.monitors = []

        self.randr12 = False

class Monitor:
    def __init__(self):
        self.id = None
        self.identifier = None
        self.probed = False
        self.wide = False
        self.digital = False
        self.panel_w = 0
        self.panel_h = 0
        self.hsync_min = 0
        self.hsync_max = 0
        self.vref_min = 0
        self.vref_max = 0
        self.modelines = []
        self.res = ["800x600", "640x480"]
        self.vendorname = "Unknown Vendor"
        self.modelname = "Unknown Model"
        self.eisaid = ""
        self.depth = "16"

class DefaultMonitor(Monitor):
    def __init__(self):
        Monitor.__init__(self)

        self.id = "DefaultMonitor"
        #self.identifier = "DefaultMonitor"
        self.vendorname = ""
        self.modelname = "Default Monitor"

        self.hsync_min = 31.5
        self.hsync_max = 50
        self.vref_min = 50
        self.vref_max = 70

class Screen:
    def __init__(self, device=None, monitor=None):
        self.number = None
        self.enabled = True
        self.identifier = None
        self.device = device
        self.monitor = monitor
        self.depth = None
        self.modes = ["800x600", "640x480"]
        self.res = "800x600"

    def setup(self):
        self.identifier = "Screen%d" % self.number
        self.monitor.identifier = "Monitor%d" % self.number
        self.device.identifier = "VideoCard%d" % self.number

        if not self.depth or self.device.driver == "fglrx":
            if self.device.driver in truecolor_cards:
                self.depth = 24
            else:
                self.depth = 16

        print "Supported modes are %s" % self.monitor.res
        print "Requested mode is %s" % self.res
        if self.res in self.monitor.res:
            i = self.monitor.res.index(self.res)
            self.modes = self.monitor.res[i:]
        else:
            self.modes[:0] = [self.res]

def driver2opengl(driver):
    return opengl_impl.get(driver, "xorg-x11")
