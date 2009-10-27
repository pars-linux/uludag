from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "Nessus Daemon",
                 "tr": "Nessus Sunucusu"})

@synchronized
def start():
    startService(command="/usr/sbin/nessusd",
                 args="-D",
                 pidfile="/var/lib/nessus/nessusd.pid",
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/var/lib/nessus/nessusd.pid",
                donotify=True)

def status():
    return isServiceRunning("/var/lib/nessus/nessusd.pid")
