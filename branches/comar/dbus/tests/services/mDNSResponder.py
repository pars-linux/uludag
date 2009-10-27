from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "Zeroconf Daemon",
                 "tr": "Zeroconf İstemcisi"})
serviceDefault = "on"

@synchronized
def start():
    startDependencies("sysklogd")
    startService(command="/usr/sbin/mdnsd",
                 pidfile="/var/run/mdnsd.pid",
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/var/run/mdnsd.pid",
                donotify=True)

def status():
    return isServiceRunning("/var/run/mdnsd.pid")
