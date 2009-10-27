serviceType = "local"
serviceDesc = _({"en": "ATI Events Daemon",
                 "tr": "ATI Events Sunucusu"})
serviceConf = "atieventsd"

from pardus.serviceutils import *

@synchronized
def start():
    startService(command="/opt/ati/sbin/atieventsd",
                 args=config.get("ATIEVENTSDOPTS", ""),
                 donotify=True)

@synchronized
def stop():
    stopService(command="/opt/ati/sbin/atieventsd",
                donotify=True)

def status():
    return isServiceRunning(command="/opt/ati/sbin/atieventsd")
