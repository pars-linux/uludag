from pardus.serviceutils import *

serviceType = "local"
serviceDesc = _({"en": "Portmap Daemon",
                 "tr": "Portmap Sunucusu"})

@synchronized
def start():
    startService(command="/sbin/portmap",
                 args=config.get("PORTMAP_OPTS", ""),
                 pidfile="/var/run/portmap.pid",
                 makepid=True,
                 donotify=True)

@synchronized
def stop():
    stopService(command="/sbin/portmap")

    import os
    os.unlink("/var/run/portmap.pid")

def status():
    return isServiceRunning("/var/run/portmap.pid")
