import os
from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "BIND Daemon",
                 "tr": "BIND DNS Sunucusu"})
serviceConf = "named"

@synchronized
def start():
    startService(command="/usr/sbin/named",
                 args="-u named -n %s %s" % (config.get("CPU", "1"), config.get("OPTIONS", "")),
                 pidfile="/var/run/named/named.pid",
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/var/run/named/named.pid",
                donotify=True)

def status():
    return isServiceRunning("/var/run/named/named.pid")
