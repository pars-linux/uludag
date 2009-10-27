from pardus.serviceutils import *

serviceType = "local"
serviceConf = "irqbalance"
serviceDesc = _({"en": "Irqbalance Daemon",
                 "tr": "Irqbalance Servisi"})

@synchronized
def start():
    startService(command="/usr/sbin/irqbalance",
                 args = config.get("args",""),
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/sbin/irqbalance",
                donotify=True)

@synchronized
def status():
    return isServiceRunning(command="/usr/sbin/irqbalance")
