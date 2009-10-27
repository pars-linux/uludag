from pardus.serviceutils import *
import os

serviceType = "local"
serviceDesc = _({"en": "Hardware Abstraction Layer",
                 "tr": "Donanım Soyutlama Katmanı (HAL)"})
serviceDefault = "on"

@synchronized
def start():
    startDependencies("acpid")

    if os.path.exists("/usr/share/hal/fdi/policy/gparted-disable-automount.fdi"):
        os.remove("/usr/share/hal/fdi/policy/gparted-disable-automount.fdi")

    startService(command="/usr/sbin/hald",
                 args="--daemon=yes --use-syslog",
                 pidfile="/var/run/hald.pid",
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/var/run/hald.pid",
                donotify=True)

def status():
    return isServiceRunning("/var/run/hald.pid")
