from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "NTP Daemon",
                 "tr": "NTP Sunucusu"})

@synchronized
def start():
    startDependencies("portmap")
    # Capabilities needed to drop root privileges
    run("/sbin/modprobe capability")
    startService(command="/usr/sbin/ntpd",
                 args="-p /var/run/ntpd.pid -u ntp:ntp",
                 pidfile="/var/run/ntpd.pid",
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/var/run/ntpd.pid",
                donotify=True)

def status():
    return isServiceRunning("/var/run/ntpd.pid")
