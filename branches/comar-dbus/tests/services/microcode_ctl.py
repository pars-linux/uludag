serviceConf = "microcode_ctl"
serviceType = "script"
serviceDefault = "on"
serviceDesc = _({"en": "Intel IA32 CPU Microcode Updater",
                 "tr": "Intel IA32 CPU Microcode Güncelleyici"})

from pardus.serviceutils import *
import time

def start():
    run("/sbin/modprobe -q microcode")
    # wait for the device node
    time.sleep(3)
    ret = run("/usr/sbin/microcode_ctl -qu -d %s" % config.get("MICROCODE_DEV", "/dev/cpu/microcode"))
    if ret == 0:
        if config.get("MODULE_UNLOAD", "yes") == "yes":
            run("/sbin/rmmod microcode")
        notify("System.Service.changed", "started")
    else:
        fail("Unable to start service")

def stop():
    notify("System.Service.changed", "stopped")
