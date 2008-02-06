serviceType = "local"
serviceDesc = _({"en": "HP Printer/Scanner Services",
                 "tr": "HP Yazıcı/Tarayıcı Servisleri"})
serviceDefault = "on"

from pardus.serviceutils import *

@synchronized
def start():
    reply = startService(command="/usr/sbin/hpiod",
                         pidfile="/var/run/hpiod.pid",
                         donotify=True)
    if reply == 0:
        startService(command="/usr/share/hplip/hpssd.py",
                     pidfile="/var/run/hpssd.pid")

@synchronized
def stop():
    stopService(pidfile="/var/run/hpssd.pid",
                donotify=True)
    stopService(pidfile="/var/run/hpiod.pid")

def status():
    return isServiceRunning("/var/run/hpssd.pid")
