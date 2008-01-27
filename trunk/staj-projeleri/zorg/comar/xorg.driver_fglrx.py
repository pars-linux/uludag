#!/usr/bin/python
# -*- coding: utf-8 -*-

def supportsDevice(vendorID, deviceID):
    import re
    from zorg.utils import capture

    out, err = capture("/sbin/modinfo", "-F", "alias", "fglrx")
    idlist = re.findall(r"pci:v0000(.{4})d0000(.{4})s", out)

    if (vendorID.upper(), deviceID.upper()) in idlist:
        return True

    return False

def probe(device):
    import re
    import zorg.probe

    device["depth"] = "24"

    lines = zorg.probe.XProbe(device)
    if not lines:
        return

    tvStandards = [
            "NTSC-M",       "NTSC-JPN", "NTSC-N",      "PAL-B",
            "PAL-COMB-N",   "PAL-D",    "PAL-G",       "PAL-H",
            "PAL-I",        "PAL-K",    "PAL-K1",      "PAL-L",
            "PAL-M",        "PAL-N",    "PAL-SECAM-D", "PAL-SECAM-K",
            "PAL-SECAM-K1", "PAL-SECAM-L"
        ]

    outInfo = re.compile(r".*: Connected Display\d+: (.+) \[(.+)\].*")
    modeCount = re.compile(r".*: Total of \d+ modes found for .* display.*")
    modeLine = re.compile(r".*: Modeline \"(.*)\" *.*")

    primary = ""
    secondary = ""
    outs = []
    parsingModesFor = ""
    outputs = {}

    for line in lines:
        if "Connected Display" in line:
            matched = outInfo.match(line)
            if matched:
                info = matched.groups()
                outs.append(info)
                outputs[info[1]] = []

        elif "Primary Controller - " in line:
            for out in outs:
                if out[0] in line:
                    primary = out[1]

        elif "Secondary Controller - " in line:
            for out in outs:
                if out[0] in line:
                    secondary = out[1]

        elif "modes found for primary display" in line:
            matched = modeCount.match(line)
            if matched:
                parsingModesFor = primary

        elif "modes found for secondary display" in line:
            matched = modeCount.match(line)
            if matched:
                parsingModesFor = secondary

        elif parsingModesFor:
            if "Display dimensions" in line \
                    or "DPI" in line:
                parsingModesFor = ""
                continue

            matched = modeLine.match(line)
            if matched:
                mode = matched.groups()[0]
                if not mode in outputs[parsingModesFor]:
                    outputs[parsingModesFor].append(mode)

    result = {
            "outputs":      ",".join(outputs.keys()),
            "TVStandards":  ",".join(tvStandards)
            }

    for output, modes in outputs.items():
        result["%s-modes" % output] = ",".join(modes)
        result["%s-enabled" % output] = "1"

    return result
