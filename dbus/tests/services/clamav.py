import os
from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "Clam Anti-Virus Daemon",
                 "tr": "Clam Anti-Virüs Sunucusu"})

@synchronized
def start():
    reply = startService(command="/usr/sbin/clamd",
                         pidfile="/var/run/clamav/clamd.pid",
                         donotify=True)
    if reply == 0:
        startService(command="/usr/bin/freshclam",
                     args="-d")

@synchronized
def stop():
    reply = stopService(pidfile="/var/run/clamav/clamd.pid",
                        donotify=True)
    if reply == 0:
        stopService(command="/usr/bin/freshclam")

def status():
    return isServiceRunning("/var/run/clamav/clamd.pid")
