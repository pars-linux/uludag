from pardus.serviceutils import *

serviceType = "server"
serviceDefault = "on"
serviceDesc = _({"en": "CUPS Printer Server",
                 "tr": "CUPS Yazıcı Sunucusu"})

@synchronized
def start():
    startDependencies("hplib")
    startService(command="/usr/sbin/cupsd",
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/sbin/cupsd",
                donotify=True)

def status():
    import os.path
    if os.path.exists("/var/run/cups/cups.sock"):
        return True
    else:
        return False
