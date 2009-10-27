serviceType = "server"
serviceDesc = _({"en": "SMB Network Sharing",
                 "tr": "SMB Ağ Paylaşımı"})

from pardus.serviceutils import *

@synchronized
def start():
    startService(command="/usr/sbin/smbd",
                 args="-D",
                 donotify=True)
    startService(command="/usr/sbin/nmbd",
                 args="-D")
    if config.get("winbind", "no") == "yes":
        startService(command="/usr/sbin/winbindd")

@synchronized
def stop():
    stopService(pidfile="/var/run/samba/winbindd.pid")
    stopService(pidfile="/var/run/samba/nmbd.pid")
    stopService(pidfile="/var/run/samba/smbd.pid",
                donotify=True)

def reload():
    import signal
    stopService(pidfile="/var/run/samba/winbindd.pid",
                signal=signl.SIGHUP)
    stopService(pidfile="/var/run/samba/nmbd.pid",
                signal=signl.SIGHUP)
    stopService(pidfile="/var/run/samba/smbd.pid",
                signal=signl.SIGHUP)

def status():
    return isServiceRunning("/var/run/samba/smbd.pid")
