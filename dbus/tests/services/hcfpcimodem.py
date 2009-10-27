from pardus.serviceutils import *

serviceType = "script"
serviceDesc = _({"en": "HCF Modem Manager",
                 "tr": "HCF Modem Yöneticisi"})

@synchronized
def start():
    import os
    if os.path.exists("/dev/ttySHCF0") and not os.path.exists("/dev/modem"):
        os.symlink("ttySHCF0", "/dev/modem")

    startService(command="/usr/sbin/hcfpciconfig",
                 args="--rcstart",
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/sbin/hcfpciconfig",
                args="--rcstop",
                donotify=True)

def status():
    return isServiceRunning(command="/usr/sbin/hcfpciconfig")
