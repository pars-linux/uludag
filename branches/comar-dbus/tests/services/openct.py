from pardus.serviceutils import *

serviceType = "local"
serviceDefault = "on"
serviceDesc = _({"en": "OpenCT SmartCard Reader Service",
                 "tr": "OpenCT Akıllı Kart Okuyucu Servisi"})

@synchronized
def start():
    startService(command="/usr/sbin/openct-control",
                 args="init",
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/sbin/openct-control",
                args="shutdown",
                donotify=True)

def status():
    return isServiceRunning(command="/usr/sbin/openct-control")
