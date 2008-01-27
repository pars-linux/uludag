# -*- coding: utf-8 -*-

from zorg.config import *
from zorg.probe import *
from zorg.utils import *

def initialConfig():
    bus = getPrimaryCard()

    if bus:
        device = VideoDevice(bus)
    else:
        return

    device.query()

    saveXorgConfig(device)
    saveDeviceInfo(device)

def safeConfig():
    bus = getPrimaryCard()

    if bus:
        device = VideoDevice(bus)
    else:
        return

    device.monitor_settings["default-hsync"] = "31.5-50"
    device.monitor_settings["default-vref"] = "50-70"

    saveXorgConfig(device)
    saveDeviceInfo(device)
