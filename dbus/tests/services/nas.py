serviceType = "server"
serviceDesc = _({"en": "Network Audio System", 
                 "tr": "Ağ Ses Sistemi"})
serviceConf = "nas"

from pardus.serviceutils import *

@synchronized
def start():
    startService(command="/usr/bin/nasd",
                 args=config.get("NAS_OPTIONS", ""),
                 pidfile="/var/run/nasd.pid",
                 makepid=True,
                 detach=True,
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/var/run/nasd.pid",
                donotify=True)

def status():
    return isServiceRunning("/var/run/nasd.pid")
