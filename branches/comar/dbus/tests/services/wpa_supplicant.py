from pardus.serviceutils import *

serviceType = "local"
serviceDesc = _({"en": "WPA Daemon",
                 "tr": "WPA Sunucusu"})

pidfile = "/var/run/wpa_supplicant.pid"

@synchronized
def start():
    startService(command="/usr/sbin/wpa_supplicant",
                 args="-wuB -P%s %s" % (pidfile, config.get("OPTS", "")),
                 pidfile=pidfile,
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile=pidfile,
                donotify=True)

def status():
    return isServiceRunning(pidfile)
