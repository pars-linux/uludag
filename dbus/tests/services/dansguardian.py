import os
from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "Dansguardian Daemon",
                 "tr": "Dansguardian Sunucusu"})

@synchronized
def start():
    startDependencies("clamav")
    startService(command="/usr/sbin/dansguardian",
                 pidfile="/var/run/dansguardian.pid",
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/sbin/dansguardian",
                pidfile="/var/run/dansguardian.pid",
                donotify=True)

def reload():
    stopService(command="/usr/sbin/dansguardian",
                args="-g")

def status():
    return isServiceRunning("/var/run/dansguardian.pid")
