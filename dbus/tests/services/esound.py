serviceType = "server"
serviceDesc = _({"en": "Enlightened Sound Daemon",
                 "tr": "Enlightened Ses Sunucusu"})
serviceConf = "esound"

from pardus.serviceutils import *

@synchronized
def start():
    startService(command="/usr/bin/esd",
                 args="%s %s" % (config.get("ESD_START", ""), config.get("ESD_OPTIONS", "")),
                 detach=True,
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/bin/esd",
                donotify=True)

def status():
    return isServiceRunning(command="/usr/bin/esd")
