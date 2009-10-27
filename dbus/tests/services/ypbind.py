from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "NIS Bind Service",
                 "tr": "NIS Bağlantı Servisi"})

@synchronized
def start():
    startDependencies("portmap", "ypserv")

    startService(command="/usr/sbin/ypbind",
                 args=config.get("YPBIND_OPTS", ""),
                 donotify=True)

@synchronized
def stop():
    reply = stopService(command="/usr/sbin/ypbind",
                        donotify=True)
    run("/usr/bin/rm -rf /var/yp/binding/")

def status():
    return isServiceRunning(command="/usr/sbin/ypbind")
