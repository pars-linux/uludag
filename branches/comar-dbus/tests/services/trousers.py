from pardus.serviceutils import *
import comar

serviceType="server"
serviceDesc = _({"en": "TrouSers",
                 "tr": "TrouSers"})

def unlink():
    import os
    try:
        os.unlink("/var/run/tcsd.pid")
    except:
        pass

def load_module():
    run("/sbin/modprobe tpm")

@synchronized
def start():
    load_module()
    startService(command="/usr/sbin/tcsd",
                 pidfile="/var/run/tcsd.pid",
                 chuid="tss",
                 makepid=True,
                 detach=True,
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/var/run/tcsd.pid",
                user="tss",
                donotify=True)

def status():
    return isServiceRunning("/var/run/tcsd.pid")
