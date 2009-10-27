from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "XEN Daemon",
                 "tr": "XEN Sunucusu"})
serviceDefault = "off"

@synchronized
def start():
    startService(command="/usr/sbin/xend",
                 args="start",
                 pidfile="/var/run/xenstore.pid",
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/sbin/xm",
                args="shutdown --all --wait")
    stopService(command="/usr/sbin/xend",
                args="stop",
                donotify=True)

def status():
    return isServiceRunning("/var/run/xenstore.pid")
