#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import sys
import os
import time
import subprocess


class Blacklist:
    def blacklist(self):
        blacks = set()
        # Unlike env.d and modules.d, blacklist is not generated
        # from blacklist.d, they all used together
        if os.path.exists("/etc/hotplug/blacklist"):
            for line in file("/etc/hotplug/blacklist"):
                line = line.rstrip('\n')
                if line == '' or line.startswith('#'):
                    continue
                blacks.add(line)
        if os.path.exists("/etc/hotplug/blacklist.d"):
            for name in os.listdir("/etc/hotplug/blacklist.d"):
                # skip backup and version control files
                if name.endswith("~") or name.endswith(".bak") or name.endswith(",v"):
                    continue
                # skip pisi's config file backups
                # .oldconfig is obsolete, but checked anyway cause it may still exist at old systems
                if name.endswith(".oldconfig") or name.endswith(".newconfig"):
                    continue
                for line in file(os.path.join("/etc/hotplug/blacklist.d", name)):
                    line = line.rstrip('\n')
                    if line == '' or line.startswith('#'):
                        continue
                    blacks.add(line)
        return blacks
    
    def plug(self, current, env=None):
        mods = self.blacklist()
        current.difference_update(mods)
    
    def debug(self):
        mods = self.blacklist()
        print "Blacklist: %s" % ", ".join(mods)


class Modalias:
    def coldAliases(self):
        aliases = []
        for root, dirs, files in os.walk("/sys", topdown=False):
            if "modalias" in files:
                path = os.path.join(root, "modalias")
                aliases.append(file(path).read().rstrip("\n"))
        return aliases
    
    def _match(self, match, alias, mod):
        # bu garip fonksiyon pythonun re ve fnmatch modullerinin
        # acayip yavas olmasindan turedi, 5 sn yerine 0.5 saniyede
        # islememizi sagliyor
        # C library deki fnmatch'i direk kullanabilsek daha hizli
        # ve temiz olacak bu isler
        i = 0
        while True:
            if i >= len(match):
                return alias == ""
            part = match[i]
            if not alias.startswith(part):
                return False
            alias = alias[len(part):]
            i += 1
            if i >= len(match):
                return alias == ""
            part = match[i]
            if part == "" and i + 1 == len(match):
                return True
            j = alias.find(part)
            if j == -1:
                return False
            alias = alias[j:]
    
    def aliasModules(self, aliases):
        modules = set()
        if len(aliases) == 0:
            return modules
        path = "/lib/modules/%s/modules.alias" % os.uname()[2]
        if not os.path.exists(path):
            # FIXME: log this as error somewhere
            return modules
        for line in file(path):
            try:
                cmd, match, mod = line.split()
            except ValueError:
                continue
            a = match.split("*")
            for alias in aliases:
                if self._match(a, alias, mod):
                    modules.add(mod)
        return modules
    
    def plug(self, current, env=None):
        aliases = []
        if env:
            if env.has_key("MODALIAS"):
                aliases = [env["MODALIAS"]]
            else:
                return
        else:
            aliases = self.coldAliases()
        mods = self.aliasModules(aliases)
        current.update(mods)
    
    def debug(self):
        aliases = self.coldAliases()
        mods = self.aliasModules(aliases)
        print "Modules: %s" % ", ".join(mods)


class PNP:
    def detect(self):
        path = "/sys/bus/pnp/devices"
        if os.path.exists(path):
            for dev in os.listdir(path):
                # For now, just a special case for parallel port driver
                # ISAPNP probing is trickier than it seems
                devids = file(os.path.join(path, dev, "id")).read().rstrip("\n")
                for id in devids.split("\n"):
                    if id == "PNP0400" or id == "PNP0401":
                        return [ "parport_pc" ]
        return []
    
    def plug(self, current, env=None):
        if env:
            # ISA bus doesn't support hotplugging
            return
        
        current.update(self.detect())
    
    def debug(self):
        print "ISAPNP: %s" % ", ".join(self.detect())


class SCSI:
    # Type constants from <scsi/scsi.h>
    modmap = {
        "0": ["sd_mod"],
        "1": ["st"],
        "4": ["sr_mod"],
        "5": ["sr_mod"],
        "7": ["sd_mod"],
    }
    
    def detect(self, devpath):
        path = os.path.join("/sys", devpath, "type")
        while not os.path.exists(path):
            time.sleep(0.1)
        
        # constants from scsi/scsi.h
        type = file(path).read().rstrip("\n")
        return self.modmap.get(type, [])
    
    def plug(self, current, env=None):
        if not env or env.get("ACTION", "") != "add" or env.get("SUBSYSTEM", "") != "scsi":
            return
        current.update(self.detect(env["DEVPATH"]))
    
    def debug(self):
        pass


class Firmware:
    def plug(self, current, env=None):
        if not env or env.get("SUBSYSTEM", "") != "firmware":
            return
        # FIXME: lame code, almost copied directly from firmware.agent
        devpath = "/sys" + env["DEVPATH"]
        firm = "/lib/firmware/" + env["FIRMWARE"]
        loading = devpath + "/loading"
        if not os.path.exists(loading):
            time.sleep(1)
        
        f = file(loading, "w")
        if not os.path.exists(firm):
            f.write("-1\n")
            f.close()
            return
        f.write("1\n")
        f.close()
        import shutil
        shutil.copy(firm, devpath + "/data")
        f = file(loading, "w")
        f.write("0\n")
        f.close()
    
    def debug(self):
        pass


class CPU:
    def __init__(self):
        self.vendor = "unknown"
        self.family = None
        self.model = None
        self.name = ""
        self.flags = []
        for line in file("/proc/cpuinfo"):
            if line.startswith("vendor_id"):
                self.vendor = line.split(":")[1].strip()
            elif line.startswith("cpu family"):
                self.family = int(line.split(":")[1].strip())
            elif line.startswith("model") and not line.startswith("model name"):
                self.model = int(line.split(":")[1].strip())
            elif line.startswith("model name"):
                self.name = line.split(":")[1].strip()
            elif line.startswith("flags"):
                self.flags = line.split(":", 1)[1].strip().split()
    
    def _find_pci(self, vendor, device):
        path = "/sys/bus/pci/devices"
        for item in os.listdir(path):
            ven = file(os.path.join(path, item, "vendor")).read().rstrip("\n")
            dev = file(os.path.join(path, item, "device")).read().rstrip("\n")
            if ven == vendor and dev == device:
                return item
        return None
    
    def _detect_ich(self):
        ich = 0
        if self._find_pci("0x8086", "0x24cc"):
            # ICH4-M
            ich = 4
        if self._find_pci("0x8086", "0x248c"):
            # ICH3-M
            ich = 3
        if self._find_pci("0x8086", "0x244c"):
            # ICH2-M
            # has trouble with old 82815 host bridge revisions
            if not self._find_pci("0x8086", "0x"):
                ich = 2
        return ich
    
    def _detect_acpi_pps(self):
        # NOTE: This may not be a correct way to detect this
        if os.path.exists("/proc/acpi/processor/CPU0/info"):
            for line in file("/proc/acpi/processor/CPU0/info"):
                if line.startswith("power management"):
                    if line.split(":")[1].strip() == "yes":
                        return True
        return False
    
    def detect(self):
        modules = set()
        if self.vendor == "GenuineIntel":
            # Pentium M, Enhanced SpeedStep
            if "est" in self.flags:
                modules.add("speedstep-centrino")
            # Some kind of Mobile Pentium
            elif self.name.find("Mobile") != -1:
                # ACPI Processor Performance States
                if self._detect_acpi_pps():
                    modules.add("acpi-cpufreq")
                # SpeedStep ICH, PIII-M and P4-M with ICH2/3/4 southbridges
                elif self._detect_ich():
                    modules.add("speedstep-ich")
                # P4 and XEON processors with thermal control
                # NOTE: Disabled for now, I'm not sure if this does more
                # harm than good
                #elif "acpi" in self.flags and "tm" in self.flags:
                #    modules.add("p4-clockmod")
        
        elif self.vendor == "AuthenticAMD":
            # Mobile K6-1/2 CPUs
            if self.family == 5 and (self.model == 12 or self.model == 13):
                modules.add("powernow-k6")
            # Mobile Athlon/Duron
            elif self.family == 6:
                modules.add("powernow-k7")
            # AMD Opteron/Athlon64
            #elif lala:
            #    modules.add("powernow-k8")
        
        elif self.vendor == "CentaurHauls":
            # VIA Cyrix III Longhaul
            if self.family == 6:
                if self.model >= 6 and self.model <= 9:
                    modules.add("longhaul")
        
        elif self.vendor == "GenuineTMx86":
            # Transmeta LongRun
            if "longrun" in self.flags:
                modules.add("longrun")
        
        return modules
    
    def isLaptop(self):
        if os.path.exists("/usr/sbin/dmidecode"):
            cmd = subprocess.Popen(
                [ "/usr/sbin/dmidecode", "-s", "chassis-type" ],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            a = cmd.communicate()
            if a[0].startswith("Notebook"):
                return True
        return False
    
    def plug(self, current, env=None):
        if env:
            return
        if os.path.exists("/sys/devices/system/cpu/cpu0/cpufreq/"):
            # User already specified a frequency module in
            # modules.autoload.d or compiled it into the kernel
            return
        if self.isLaptop():
            current.update(self.detect())
    
    def debug(self):
        print "CPU: %s" % ", ".join(self.detect())


#
# Main functions
#

# Order of pluggers is important!
pluggers = (
    CPU,
    PNP,
    Modalias,
    SCSI,
    Firmware,
    Blacklist,  # Blacklist should be at the end
)

def tryModule(modname):
    f = file("/dev/null", "w")
    ret = subprocess.call(["/sbin/modprobe", "-n", modname], stdout=f, stderr=f)
    if ret == 0:
        ret = subprocess.call(["/sbin/modprobe", "-q", modname], stdout=f, stderr=f)

def plug(env=None):
    modules = set()
    for plugger in pluggers:
        p = plugger()
        p.plug(modules, env)
    for mod in modules:
        tryModule(mod)

def debug():
    for plugger in pluggers:
        p = plugger()
        p.debug()


#
# Command line driver
#

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--debug":
        debug()
    
    elif len(sys.argv) == 2 and sys.argv[1] == "--coldplug":
        plug()
    
    else:
        # This file is written by mudur, after loading of modules in the
        # modules.autoload.d finishes, thus preventing udevtrigger events
        # from loading of other modules first. Triggered events are
        # needed to populate /dev way before module loading phase.
        if os.path.exists("/dev/.muavin"):
            plug(os.environ)
