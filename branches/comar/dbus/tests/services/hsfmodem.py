from pardus.serviceutils import *

serviceType = "script"
serviceDesc = _({"en": "HSF Modem Manager",
                 "tr": "HSF Modem Yöneticisi"})

@synchronized
def start():
    import os
    if os.path.exists("/dev/ttySHSF0") and not os.path.exists("/dev/modem"):
        os.symlink("ttySHSF0", "/dev/modem")

    startService(command="/usr/sbin/hsfconfig",
                 args="--rcstart",
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/sbin/hsfconfig",
                args="--rcstop",
                donotify=True)

def status():
    return isServiceRunning(command="/usr/sbin/hsfconfig")
