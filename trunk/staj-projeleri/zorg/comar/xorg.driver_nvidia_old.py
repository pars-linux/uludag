#!/usr/bin/python
# -*- coding: utf-8 -*-

pciIDs = {
        "1092": (
            "0550", # Viper V550
            "1092", # Viper V330
            ),
        "10de": (
            "0020", # RIVA TNT
            "0028", # RIVA TNT2/TNT2 Pro
            "0029", # RIVA TNT2 Ultra
            "002c", # Vanta/Vanta LT
            "002d", # RIVA TNT2 Model 64/Model 64 Pro
            "00a0", # Aladdin TNT2
            "0100", # GeForce 256
            "0101", # GeForce DDR
            "0103", # Quadro
            "0150", # GeForce2 GTS/GeForce2 Pro
            "0151", # GeForce2 Ti
            "0152", # GeForce2 Ultra
            "0153", # Quadro2 Pro'
            ),
        "12d2": (
            "0008",
            "0009",
            "0018",
            "0019",
            "0020",
            "0028",
            "0029",
            "002c",
            "00a0",
            )
    }

def supportsDevice(vendorID, deviceID):
    return deviceID.lower() in pciIDs.get(vendorID.lower(), [])

def probe(device):
    import re
    import zorg.probe

    device["driver-options"] = {
            "UseEdidFreqs" : "1"
        }

    lines = zorg.probe.XProbe(device)
    if not lines:
        return

    #TODO: Remove new standards
    tvStandards = [
            "PAL-B",  "PAL-D",  "PAL-G",   "PAL-H",
            "PAL-I",  "PAL-K1", "PAL-M",   "PAL-N",
            "PAL-NC", "NTSC-J", "NTSC-M",  "HD480i",
            "HD480p", "HD720p", "HD1080i", "HD1080p",
            "HD576i", "HD576p"
        ]

    modePattern = re.compile('.+ "(.+)": .+ MHz, .+ kHz, .+ Hz.*')

    parsingModesFor = ""
    outputs = {}

    for line in lines:
        if "Supported display device(s): " in line:
            outs = line.rsplit(":", 1)[-1].split(",")
            for out in outs:
                out = out.strip()
                outputs[out] = []

        elif "Validated modes for display device " in line:
            for key in outputs.keys():
                if key in line:
                    parsingModesFor = key
                    break

        elif parsingModesFor:
            matched = modePattern.match(line)
            if matched:
                mode = matched.groups()[0]

                if not mode in outputs[parsingModesFor]:
                    outputs[parsingModesFor].append(mode)

            else:
                parsingModesFor = ""

    result = {
            "outputs":      ",".join(outputs.keys()),
            "TVStandards":  ",".join(tvStandards)
            }

    for output, modes in outputs.items():
        result["%s-modes" % output] = ",".join(modes)
        result["%s-enabled" % output] = "1"

    return result
