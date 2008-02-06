from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "HylaFax Daemon",
                 "tr": "HylaFax Sunucusu"})

@synchronized
def start():
    reply = startService(command="/usr/sbin/faxq",
                         pidfile="/var/run/faxq.pid",
                         makepid=True,
                         donotify=True)
    if reply == 0:
        startService(command="/usr/sbin/hfaxd",
                     args="-i hylafax -o 4557 -s 444")

@synchronized
def stop():
    stopService(pidfile="/var/run/faxq.pid",
                donotify=True)
    stopService(command="/usr/sbin/hfaxd")

def status():
    return isServiceRunning(command="/usr/sbin/hfaxd")
