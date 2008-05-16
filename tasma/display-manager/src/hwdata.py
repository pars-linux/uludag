# -*- coding: utf-8 -*-

import zorg.consts
from zorg.utils import *

drivers = {
    "apm":          "Alliance ProMotion cards, including AT24, AT3D, and AT25",
    "ark":          "ARK Logic chipsets",
    "ast":          "ASpeedTech chipsets",
    "ati":          "ATI Mach8, Mach32, Mach64, and RageXL cards",
    "chips":        "Chips and Technologies chipsets, including CT655xx, CT64xxx, CT68xxx, and CT690x0",
    "cirrus":       "Cirrus CL-GD54xx/7548 cards",
    "cyrix":        "Cyrix MediaGX, MediaGXi, and MediaGXm processors",
    "fbdev":        "Linux FrameBuffer",
    "fglrx/ati-drivers":
                    "Drivers written by AMD(ATI) for ATI graphics cards",
    "glint":        "3DLabs/Texas Instruments GLINT and Permedia cards",
    "i128":         "Number 9 Imagine 128 cards",
    "i740":         "Intel I740 chipset",
    "intel":        "Intel Integrated Graphics Chipsets, including i810, i815, 830M, 845G, 852GM, 855GM, 865G, 915G, 915GM, and 945GM",
    "imstt":        "Integrated Micro Solutions Twin Turbo 128",
    "mga":          "Matrox Millennium, Mystique, Millennium II, G100, G200, G400, G450, G550",
    "neomagic":     "NeoMagic MagicGraph 128, 256",
    "newport":      "SGI Indy/Indigo2 Newport card",
    "nsc":          "National Semiconductors Geode Processor",
    "nv":           "nVidia Riva 128, RIVA TNT, GeForce, nForce, and QUADRO cards",
    "nvidia/nvidia-drivers-old":
                    "nVIDIA kernel and glx drivers for old nVIDIA cards like TNT2",
    "nvidia/nvidia-drivers":
                    "nvidia-drivers package contains nVIDIA kernel and glx drivers giving optimized 2d/3d performance",
    "nvidia/nvidia-drivers-new":
                    "nVIDIA kernel and glx drivers for NV3 or better cards (Geforce FX or better)",
    "openchrome":   "VIA/S3G UniChrome, UniChrome Pro and Chrome9 graphics chipsets",
    "r128":         "ATI Rage128 cards, including Rage Fury, XPERT 128, and XPERT 99",
    "radeon":       "ATI Radeon cards, including Radeon Mobility and FireGL",
    "radeonhd":     "AMD GPG r5xx/r6xx Chipsets",
    "rendition":    "Rendition/Micron Verite cards, including Diamond Stealth II S220",
    "s3":           "S3 964, 968, Trio, Aurora64, and Trio64 cards",
    "s3virge":      "S3 ViRGE and Trio3D cards",
    "savage":       "S3 Savage, SuperSavage, Twister, and ProSavage chipsets",
    "siliconmotion":"Silicon Motion Lynx and Cougar chipsets",
    "sis":          "Silicon Integrated Systems SiS chipsets",
    "sisusb":       "Silicon Integrated Systems SiS315E/PRO USB adpater",
    "sunbw2":       "Sun BW2 framebuffer",
    "suncg14":      "Sun CG14 framebuffer",
    "suncg3":       "Sun CG3 framebuffer",
    "suncg6":       "Sun GX/Turbo GX (cgsix) framebuffer",
    "sunffb":       "Sun Creator, Creator 3D, Elite 3D framebuffer",
    "sunleo":       "Sun Leo (ZX) framebuffer",
    "suntcx":       "Sun TCX framebuffer",
    "tdfx":         "3Dfx Voodoo Banshee, Voodoo 3, Voodoo 4, Voodoo 5 cards",
    "tga":          "DEC TGA chipset",
    "trident":      "Trident Blade, CyberBlade, 3DImage, ProVidia, TGUI, and Cyber9xxx cards",
    "tseng":        "Tseng Labs ET4000, ET6000, and ET6100 cards",
    "vesa":         "Generic VESA-compliant video cards",
    "vga":          "Generic VGA video cards",
    "via":          "VIA Unichrome (CLE266, KM400/KN400, K8M800/K8N800, PM8X0, CN400) chipsets",
    "vmware":       "VMWare virtual video cards",
    "voodoo":       "Voodoo1 and Voodoo2 cards"
}

def getCompatibleDriverNames(vendor_id, product_id):
    pci_id = vendor_id + product_id
    drvlist = []
    for line in loadFile(zorg.consts.DriversDB):
        if line.startswith(pci_id):
            drvlist = line.rstrip("\n").split(" ")[1:]
            break

    if "vesa" not in drvlist:
        drvlist.append("vesa")

    if "fbdev" not in drvlist:
        drvlist.append("fbdev")

    return drvlist

def getAvailableDrivers():
    availableDriverList = {}

    for d in zorg.probe.listAvailableDrivers():
        if not drivers.has_key(d):
            availableDriverList[d] = ""
        else:
            availableDriverList[d] = drivers[d]

    return availableDriverList

def getMonitorInfos():
    vendor = {}

    for line in loadFile(zorg.consts.MonitorsDB):
        monitor = line.split(";")

        if len(monitor) == 5:
            monitor.append('0')

        if len(monitor) == 6:
            if not monitor[0] in vendor:
                vendor[monitor[0]] = [{ "model":    monitor[1],
                                        "eisa_id":  monitor[2],
                                        "hsync":    monitor[3],
                                        "vref":     monitor[4],
                                        "is_dpms":  monitor[5]
                                        }]
            else:
                vendor[monitor[0]].extend([{"model":    monitor[1],
                                            "eisa_id":  monitor[2],
                                            "hsync":    monitor[3],
                                            "vref":     monitor[4],
                                            "is_dpms":  monitor[5]
                                            }])

    return vendor
